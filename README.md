# LicenseGuard

A command-line tool that scans the installed dependencies of a JavaScript/npm project and verifies that each package's license complies with a user-defined policy. Designed for CI pipelines and local pre-commit checks.

## Features
- **Dependency License Extraction** -- Walks `node_modules`, reads each `package.json`, and collects SPDX license identifiers (handles both string and object-style `license` fields).
- **Policy Loading and Evaluation** -- Checks every dependency against an allowed/denied license list loaded from a JSON policy file. Supports allowlist-only, denylist-only, or combined modes.
- **Reporting and Exit Code** -- Outputs results as JSON lines or a human-readable summary. Returns non-zero exit codes for policy violations, suitable for CI gating.
- **Deduplication** -- Automatically deduplicates packages by `(name, version)` so nested `node_modules` trees don't inflate results.

## Tech Stack
- Python 3.11+
- click (CLI framework)
- colorama (colored output)
- pydantic (data models)
- pytest (testing)

## Project Structure
```
licenseguard/
  __init__.py
  cli.py          # Click CLI with `scan` subcommand
  scanner.py      # Walks node_modules, extracts license from package.json
  policy.py       # Loads and validates JSON policy files
  models.py       # Pydantic models: Dependency, Policy
  reporter.py     # JSON-lines and summary formatters
tests/
  test_scanner.py
  test_policy.py
  test_reporter.py
sample-project/   # Example node_modules for testing
pyproject.toml    # Package metadata and dependencies
init.sh           # Bootstrap script
```

## Quick Start
```bash
git clone https://github.com/m2ai-portfolio/licenseguard.git
cd licenseguard
./init.sh          # Install dependencies and set up environment
licenseguard scan  # Scan current project's node_modules
```

## Usage
```bash
# Scan dependencies and output as JSON lines
licenseguard scan --path ./my-project --format json

# Scan with human-readable summary
licenseguard scan --path ./my-project --format summary
```

## Policy Files

Policy files are JSON documents with two optional fields: `allowed` and `denied`. Each is a list of SPDX license identifiers.

```json
{
  "allowed": ["MIT", "Apache-2.0", "BSD-2-Clause", "BSD-3-Clause", "ISC"],
  "denied": ["GPL-3.0", "AGPL-3.0"]
}
```

**Evaluation rules:**
- If `denied` is set and a dependency's license appears in it, the dependency **fails**.
- If `allowed` is set and a dependency's license does **not** appear in it, the dependency **fails**.
- If both are set, `denied` is checked first; then `allowed` is checked.
- If neither is set (empty policy), all licenses pass.

Set the policy file path via the `LICENSEGUARD_POLICY` environment variable or pass it directly to the `evaluate` command.

## Environment Variables
- `LICENSEGUARD_POLICY` -- Path to JSON policy file (default: `.licenseguardrc`)
- `LICENSEGUARD_NO_COLOR` -- Disable colored output

## Running Tests
```bash
pip install -e ".[dev]"
pytest tests/
```

## License
MIT
