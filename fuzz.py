import random
import string
import scanner
import parser
import copy
import json
import traceback
from datetime import datetime, timezone
from pathlib import Path 



def generate_random_input():
    """Generate random inputs, including edge cases."""
    edge_cases = [
        None,
        "",
        " ",
        0,
        -1,
        12345,
        True,
        False,
        [],
        {},
        "admin",
        "root",
        "username",
        "A" * 10000,
    ]

    if random.random() < 0.5:
        return random.choice(edge_cases)

    length = random.randint(0, 100)
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choices(characters, k=length))

bug_reports = []


def record_bug(function_name, iteration, test_input, error):
    """Record exception evidence discovered during fuzzing."""

    bug = {
        "bug_id": f"BUG-{len(bug_reports) + 1:03d}",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "function": function_name,
        "iteration": iteration,
        "input_value": repr(test_input),
        "input_type": type(test_input).__name__,
        "exception_type": type(error).__name__,
        "exception_message": str(error),
        "stack_trace": traceback.format_exc()
    }

    bug_reports.append(bug)


def save_bug_reports():
    """Save fuzzing findings as structured JSON evidence."""

    evidence_dir = Path("evidence")
    evidence_dir.mkdir(exist_ok=True)

    report_path = evidence_dir / "bug_reports.json"

    report = {
        "random_seed": 6710,
        "functions_tested": 10,
        "total_tests": 1001,
        "total_findings": len(bug_reports),
        "total_exception_occurrences": sum(
            bug["exception_type"] != "AssertionError"
            for bug in bug_reports
),
"total_logical_failures": sum(
    bug["exception_type"] == "AssertionError"
    for bug in bug_reports
),
        "findings": bug_reports
    }

    with report_path.open("w", encoding="utf-8") as file:
        json.dump(report, file, indent=4)

    print(f"\nBug report saved to: {report_path}")

def fuzz_scanner(iterations=100):
    """Fuzz five scanner validation functions."""

    functions = [
        scanner.isValidUserName,
        scanner.isValidPasswordName,
        scanner.isValidKey,
        scanner.checkIfValidSecret,
        scanner.checkIfValidKeyValue,
    ]

    for function in functions:
        print(f"\nFuzzing scanner.{function.__name__}()")

        exceptions = 0

        for i in range(iterations):
            test_input = generate_random_input()

            try:
                function(test_input)
            except Exception as error:
                exceptions += 1
                record_bug(
                    f"scanner.{function.__name__}",
                    i,
                    test_input,
                    error
                )
                print(f"Iteration {i}: {type(error).__name__}: {error}")
                print(f"Input: {test_input!r}")

        print(f"Completed {iterations} tests. Exceptions: {exceptions}")

def fuzz_parser(iterations=100):
    """Fuzz five parser functions."""

    functions = [
        (
            "checkIfWeirdYAML",
            lambda data: parser.checkIfWeirdYAML(data)
        ),
        (
            "keyMiner",
            lambda data: parser.keyMiner(data, "password")
        ),
        (
            "getKeyRecursively",
            lambda data: parser.getKeyRecursively(data, [])
        ),
        (
            "getValuesRecursively",
            lambda data: list(parser.getValuesRecursively(data))
        ),
        (
            "getValsFromKey",
            lambda data: parser.getValsFromKey(data, "password", [])
        ),
    ]

    structured_inputs = [
        {},
        [],
        None,
        123,
        "",
        {"password": "test123"},
        {"username": "admin"},
        {"metadata": {"name": "test"}},
        {"a": {"password": "secret"}},
        {"items": [{"password": "test"}]},
        {"a": [1, 2, 3]},
        {1: "numeric key", "a": "string key"},
        {"a": {"b": {"c": "password"}}},
        {"password": None},
        {"password": ["one", "two"]},
    ]

    for name, function in functions:
        print(f"\nFuzzing parser.{name}()")

        exceptions = 0

        for i in range(iterations):
            if i < len(structured_inputs):
                test_input = copy.deepcopy(structured_inputs[i])
            elif random.random() < 0.5:
                test_input = copy.deepcopy(
                    random.choice(structured_inputs)
                )
            else:
                test_input = generate_random_input()

            try:
                function(test_input)
            except Exception as error:
                exceptions += 1

                record_bug(
                    f"parser.{name}",
                    i,
                    test_input,
                    error
                )

                print(f"Iteration {i}: {type(error).__name__}: {error}")
                print(f"Input: {test_input!r}")
        print(f"Completed {iterations} tests. Exceptions: {exceptions}")

def fuzz_logical_defects():
    """Detect incorrect results using expected outputs."""

    print("\nTesting parser.getKeyRecursively() logic")

    test_input = {
        "a": {"x": 1},
        "b": {"y": 2},
        "c": 3
    }

    expected = [
        ("a", 0),
        ("x", 1),
        ("b", 0),
        ("y", 1),
        ("c", 0)
    ]

    actual = []

    try:
        parser.getKeyRecursively(test_input, actual)

        if actual != expected:
            raise AssertionError(
                f"Incorrect recursion depth. "
                f"Expected: {expected}. Actual: {actual}"
            )

        print("Logical test: PASSED")

    except Exception as error:
        record_bug(
            "parser.getKeyRecursively",
            0,
            test_input,
            error
        )

        print("Logical test: FAILED")
        print(f"Expected: {expected}")
        print(f"Actual: {actual}")


if __name__ == "__main__":
    random.seed(6710)

    fuzz_scanner()
    fuzz_parser()
    fuzz_logical_defects()
    save_bug_reports()
