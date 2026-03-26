# LicenseGuard

A command-line tool that scans the installed dependencies of a JavaScript/npm project and verifies that each package's license complies with a user-defined policy. Designed for CI pipelines and local pre-commit checks.

## Features
- Dependency License Extraction: Scan node_modules and collect license info
- Policy Loading and Evaluation: Check dependencies against allowed/denied license lists
- Reporting and Exit Code: Human-readable and JSON output with proper exit codes

## Tech Stack
- Python 3.11+
- click (CLI framework)
- colorama (colored output)
- pytest (testing)

## Quick Start
```bash
./init.sh          # Install dependencies and set up environment
licenseguard check # Run license check on current project
```

## Usage
```bash
# Scan dependencies
licenseguard scan --path ./my-project

# Evaluate against a policy
licenseguard evaluate --policy ./policy.json --deps ./deps.json

# Full check with report
licenseguard check --format json
```

## Environment Variables
- `LICENSEGUARD_POLICY`: Path to JSON policy file (default: `.licenseguardrc`)
- `LICENSEGUARD_NO_COLOR`: Disable colored output
