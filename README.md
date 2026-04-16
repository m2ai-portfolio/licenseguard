

<p align="center">
  <img src="assets/infographic.png" alt="LicenseGuard" width="800">
</p>

<h3 align="center">Pre-install license risk scanner for JavaScript/npm projects that catches incompatible licenses before they enter your codebase, with CI/CD integration and policy enforcement.</h3>

<p align="center">
  <a href="#quick-start">Quick Start</a> &bull;
  <a href="#features">Features</a> &bull;
  <a href="#examples">Examples</a> &bull;
  <a href="#contributing">Contributing</a>
</p>

## What is this?
LicenseGuard is a command‑line tool that inspects the `node_modules` folder of a JavaScript/npm project, checks each package’s license against a user‑defined policy, and reports any violations before they are committed. It is aimed at legal/compliance teams and senior engineers who need to keep their supply chain clean.

Example:
```
$ licenseguard check
✅ All 18 dependencies are compliant with policy.
Exit code: 0
```

## Problem
Development teams using npm often discover license compliance issues late in the development cycle or during security audits, when packages with restrictive licenses have already been deeply integrated. Checking licenses manually before each install is impractical with modern dependency chains. Organizations need proactive license scanning that prevents problematic dependencies from being added in the first place.

## Features
| Feature | Description |
|---------|-------------|
| Dependency license extraction | Walks `node_modules`, reads each `package.json`, and records name, version, and license (SPDX or raw string). |
| Duplicate‑package skipping | Skips repeated name/version pairs to avoid redundant checks. |
| Unknown‑license handling | Treats missing or malformed license fields as `"UNKNOWN"` unless explicitly allowed. |
| Policy loading | Reads a JSON policy with optional `allowed` and `denied` lists; missing keys mean no restriction for that list. |
| License evaluation | Determines if a license passes the policy; returns reason `DENIED` or `NOT_ALLOWED`. |
| Reporting & exit codes | Prints a human‑readable table, supports `--format json`, exits `0` on success, `1` on any failure. |
| Color‑aware output | Uses `colorama` for colored output; respects `LICENSEGUARD_NO_COLOR` to disable ANSI codes. |
| Offline operation | Operates entirely on the local filesystem; makes no network calls. |

## Quick Start
1. Clone the repository:  
   ```bash
   git clone https://github.com/your-org/LicenseGuard.git
   cd LicenseGuard
   ```
2. Install the package in editable mode:  
   ```bash
   pip install -e .
   ```
3. Run a compliance check on an npm project:  
   ```bash
   licenseguard check --path ./my-js-project
   ```
4. View JSON output for CI consumption:  
   ```bash
   licenseguard check --format json
   ```

## Examples
**Basic compliance check**  
```
$ licenseguard check
✅ All 17 dependencies are compliant with policy.
Exit code: 0
```

**Detecting a denied license with JSON output**  
```
$ licenseguard check --format json
{
  "total": 17,
  "passed": 16,
  "failed": 1,
  "details": [
    {"name":"jsdom","version":"20.0.0","license":"GPL-3.0","reason":"DENIED"}
  ]
}
Exit code: 1
```

**Using a custom policy file**  
```
$ LICENSEGUARD_POLICY=./policy.json licenseguard check
✅ All dependencies comply with the custom policy.
Exit code: 0
```

## File Structure
```
LicenseGuard/
├── src/                     # Core source code
│   ├── __init__.py
│   ├── cli.py               # Click command group and subcommands
│   ├── scanner.py           # Extracts licenses from node_modules
│   ├── policy.py            # Loads and evaluates license policies
│   ├── models.py            # Pydantic models for Dependency and Policy
│   └── reporter.py          # Formats output and handles exit codes
├── tests/                   # Test suite
│   ├── __init__.py
│   ├── test_scanner.py
│   ├── test_policy.py
│   └── test_reporter.py
├── pyproject.toml           # Project metadata and dependencies
├── README.md
└── LICENSE
```

## Tech Stack
| Technology | Purpose |
|------------|---------|
| Python 3.11+ | Core language |
| click | Minimal CLI framework |
| colorama | Optional colored terminal output |
| pytest | Testing framework |

## Contributing
Fork the repository, make your changes, run the test suite, and submit a pull request.

## License
MIT

## Author
Matthew Snow -- [M2AI](https://m2ai.co) | [@m2ai-portfolio](https://github.com/m2ai-portfolio)