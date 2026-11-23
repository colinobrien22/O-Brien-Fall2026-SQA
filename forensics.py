import json
import time
import inspect
import uuid
from functools import wraps
from datetime import datetime, timezone
from pathlib import Path

LOG_FILE = Path(__file__).resolve().parent / "evidence" / "forensic_logs.jsonl"


def write_event(event):
    """Write a machine-readable forensic event."""

    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

    event["timestamp"] = datetime.now(timezone.utc).isoformat()

    with LOG_FILE.open("a", encoding="utf-8") as file:
        file.write(json.dumps(event) + "\n")


def forensic(function):
    """Record function execution and exceptions."""

    def start_event(args, kwargs):
        event = {
            "execution_id": str(uuid.uuid4()),
            "function": f"{function.__module__}.{function.__name__}",
            "input_types": [
                type(arg).__name__ for arg in args
            ],
            "keyword_input_types": {
                key: type(value).__name__
                for key, value in kwargs.items()
            }
        }

        write_event({**event, "event": "ENTRY"})

        return event, time.perf_counter()

    def finish_event(event, start, status, error=None):
        result = {
            **event,
            "event": "EXIT",
            "status": status,
            "duration_ms": round(
                (time.perf_counter() - start) * 1000, 4
            )
        }

        if error is not None:
            result["exception_type"] = type(error).__name__

        write_event(result)

    if inspect.isgeneratorfunction(function):

        @wraps(function)
        def generator_wrapper(*args, **kwargs):
            event, start = start_event(args, kwargs)

            try:
                yield from function(*args, **kwargs)

            except GeneratorExit:
                finish_event(event, start, "CLOSED")
                raise

            except Exception as error:
                finish_event(event, start, "ERROR", error)
                raise

            else:
                finish_event(event, start, "SUCCESS")

        return generator_wrapper

    @wraps(function)
    def wrapper(*args, **kwargs):
        event, start = start_event(args, kwargs)

        try:
            result = function(*args, **kwargs)

        except Exception as error:
            finish_event(event, start, "ERROR", error)
            raise

        finish_event(event, start, "SUCCESS")

        return result

    return wrapper
