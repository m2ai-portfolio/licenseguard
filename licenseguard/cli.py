"""CLI interface for LicenseGuard."""

import click
import sys
from pathlib import Path

from .scanner import scan_dependencies
from .reporter import report_json, report_summary


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """LicenseGuard - Dependency License Compliance Scanner."""
    pass


@cli.command()
@click.option(
    "--path",
    type=click.Path(exists=True, file_okay=False, dir_okay=True),
    default=".",
    help="Path to the project directory (default: current directory)",
)
@click.option(
    "--format",
    type=click.Choice(["json", "summary"]),
    default="json",
    help="Output format (default: json)",
)
def scan(path: str, format: str):
    """
    Scan node_modules and extract license information.

    Outputs JSON lines by default, one per dependency.
    """
    dependencies = scan_dependencies(path)

    if format == "json":
        report_json(dependencies)
    else:
        report_summary(dependencies)


def main():
    """Entry point for the CLI."""
    cli()


if __name__ == "__main__":
    main()
