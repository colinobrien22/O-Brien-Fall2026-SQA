# Software Quality Assurance Project

## COMP 6710 – Fall 2026

**Auburn University**

### Team Information

**Team Name:** O-Brien

**Team Member:** Colin O'Brien

### Project Description

This project was completed for COMP 6710 – Software Quality Assurance at Auburn University during Fall 2026.

The objective of this project was to integrate software quality assurance activities into the existing Slikube Python application through automated software fuzzing, forensic instrumentation, and continuous integration.

### Project Completion Status

| Project Requirement | Status |
|---|---|
| Extract and upload the original Slikube project | Complete |
| Register team information | Complete |
| Create GitHub repository and README | Complete |
| Implement automated fuzzing of 10 Python methods | Complete |
| Integrate forensic instrumentation into 10 Python methods | Complete |
| Implement continuous integration using GitHub Actions | Complete |
| Document discovered bugs and experimental results | Complete |
| Complete the final project report | Complete |

### Project Results

| Metric | Result |
|---|---:|
| Python methods fuzzed | 10 |
| Python methods instrumented | 10 |
| Total test cases executed | 1,001 |
| Runtime exception occurrences | 19 |
| Logical failures | 1 |
| Total reported findings | 20 |
| Forensic records generated | 2,444 |
| Function executions recorded | 1,222 |
| Successful function executions | 1,203 |
| Error executions | 19 |
| Unmatched forensic executions | 0 |
| Automated validation checks passed | 11/11 |
| GitHub Actions execution | Successful |

The automated fuzzing process identified two underlying issues:

1. A potential input-validation robustness defect in `parser.checkIfWeirdYAML()`.
2. A logical defect involving recursive depth calculation in `parser.getKeyRecursively()`.

The original defects were preserved to support reproducible testing, forensic analysis, and documentation.

### Project Structure

| File or Directory | Description |
|---|---|
| [fuzz.py](fuzz.py) | Automated fuzz testing and bug reporting |
| [forensics.py](forensics.py) | Reusable forensic instrumentation decorator |
| [validate_sqa.py](validate_sqa.py) | Automated validation of fuzzing and forensic evidence |
| [parser.py](parser.py) | Original parser module with five instrumented methods |
| [scanner.py](scanner.py) | Original scanner module with five instrumented methods |
| [requirements-sqa.txt](requirements-sqa.txt) | Pinned Python dependencies |
| [.github/workflows/sqa-ci.yml](.github/workflows/sqa-ci.yml) | GitHub Actions continuous integration workflow |
| [evidence/](evidence/) | Experimental results, logs, and screenshots |
| [SQA-REPO.md](SQA-REPO.md) | Final project report |

### Running the Project

Python 3.11 is recommended.

Clone the repository:

```bash
git clone https://github.com/colinobrien22/O-Brien-Fall2026-SQA.git
cd O-Brien-Fall2026-SQA
```

Create and activate a Python virtual environment on Linux or macOS:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
```

Install the required dependencies:

```bash
python -m pip install -r requirements-sqa.txt
```

Prepare a clean forensic log:

```bash
python -c "from pathlib import Path; p = Path('evidence/forensic_logs.jsonl'); p.parent.mkdir(exist_ok=True); p.write_text('')"
```

Execute automated fuzzing:

```bash
python fuzz.py
```

Validate the generated results:

```bash
python validate_sqa.py
```

The expected validation result is:

```text
Overall result: PASSED
```

A successful validation indicates that the generated findings and forensic evidence match the established testing baseline. It does not indicate that the application is defect-free.

### Continuous Integration

[![Slikube SQA Continuous Integration](https://github.com/colinobrien22/O-Brien-Fall2026-SQA/actions/workflows/sqa-ci.yml/badge.svg?branch=main)](https://github.com/colinobrien22/O-Brien-Fall2026-SQA/actions/workflows/sqa-ci.yml)

GitHub Actions automatically executes the fuzzing framework and validates the generated forensic evidence when changes are pushed to the main branch or pull requests target the main branch.

The workflow also supports manual execution and uploads the generated evidence as a downloadable artifact.

[View GitHub Actions workflow runs](https://github.com/colinobrien22/O-Brien-Fall2026-SQA/actions)

### Supporting Evidence

- [Baseline fuzzing results](evidence/baseline_fuzz_results.txt)
- [Enhanced fuzzing results](evidence/enhanced_fuzz_results.txt)
- [Instrumented fuzzing results](evidence/instrumented_fuzz_results.txt)
- [Automated bug reports](evidence/bug_reports.json)
- [Forensic execution logs](evidence/forensic_logs.jsonl)
- [Forensic analysis summary](evidence/forensic_summary.txt)
- [Automated validation results](evidence/sqa_validation.txt)
- [GitHub Actions screenshots](evidence/screenshots/)

### Final Project Report

The complete project report contains the implementation methodology, task completion status, discovered defects, root cause analysis, forensic instrumentation design, continuous integration results, replication instructions, supporting screenshots, and lessons learned.

**[View the Final Project Report — SQA-REPO.md](SQA-REPO.md)**

### Project Status

All required technical activities have been implemented, tested, and documented. The automated fuzzing framework, forensic instrumentation, and continuous integration pipeline have been successfully executed and validated.
