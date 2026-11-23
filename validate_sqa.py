import json
from collections import Counter, defaultdict
from pathlib import Path

EVIDENCE_DIR = Path("evidence")

EXPECTED_FUNCTIONS = {
    "parser.checkIfWeirdYAML",
    "parser.keyMiner",
    "parser.getKeyRecursively",
    "parser.getValuesRecursively",
    "parser.getValsFromKey",
    "scanner.isValidUserName",
    "scanner.isValidPasswordName",
    "scanner.isValidKey",
    "scanner.checkIfValidSecret",
    "scanner.checkIfValidKeyValue"
}


def validate():
    with (EVIDENCE_DIR / "bug_reports.json").open() as file:
        report = json.load(file)

    with (EVIDENCE_DIR / "forensic_logs.jsonl").open() as file:
        records = [json.loads(line) for line in file]

    functions = Counter(
        record["function"]
        for record in records
        if record["event"] == "ENTRY"
    )

    statuses = Counter(
        record["status"]
        for record in records
        if record["event"] == "EXIT"
    )

    executions = defaultdict(list)

    for record in records:
        executions[record["execution_id"]].append(
            record["event"]
        )

    unmatched = sum(
        events != ["ENTRY", "EXIT"]
        for events in executions.values()
    )

    findings = Counter(
        (bug["function"], bug["exception_type"])
        for bug in report["findings"]
    )

    expected_findings = Counter({
        ("parser.checkIfWeirdYAML", "TypeError"): 19,
        ("parser.getKeyRecursively", "AssertionError"): 1
    })

    checks = {
        "Ten functions tested":
            report["functions_tested"] == 10,

        "1001 test cases executed":
            report["total_tests"] == 1001,

        "Correct random seed":
            report["random_seed"] == 6710,

        "All expected functions instrumented":
            set(functions) == EXPECTED_FUNCTIONS,

        "All forensic executions matched":
            unmatched == 0,

        "Expected runtime exceptions":
            report["total_exception_occurrences"] == 19,

        "Expected logical failures":
            report["total_logical_failures"] == 1,

        "Expected total findings":
            report["total_findings"] == 20,

        "No unexpected bug categories":
            findings == expected_findings,

        "Forensic error count matches bug report":
            statuses["ERROR"] ==
            report["total_exception_occurrences"],

        "All executions have valid exit statuses":
            statuses["SUCCESS"] + statuses["ERROR"]
            == len(executions)
    }

    lines = [
        "SLIKUBE SQA VALIDATION REPORT",
        "=" * 50,
        f"Test cases: {report['total_tests']}",
        f"Functions instrumented: {len(functions)}",
        f"Total findings: {report['total_findings']}",
        f"Forensic records: {len(records)}",
        f"Function executions: {len(executions)}",
        f"Successful executions: {statuses['SUCCESS']}",
        f"Error executions: {statuses['ERROR']}",
        f"Unmatched executions: {unmatched}",
        "",
        "VALIDATION CHECKS",
        "=" * 50
    ]

    for name, passed in checks.items():
        status = "PASS" if passed else "FAIL"
        lines.append(f"[{status}] {name}")

    all_passed = all(checks.values())

    lines.append("")
    lines.append(
        "Overall result: PASSED"
        if all_passed
        else "Overall result: FAILED"
    )

    output = "\n".join(lines)

    print(output)

    (EVIDENCE_DIR / "sqa_validation.txt").write_text(
        output + "\n",
        encoding="utf-8"
    )

    return 0 if all_passed else 1


if __name__ == "__main__":
    raise SystemExit(validate())