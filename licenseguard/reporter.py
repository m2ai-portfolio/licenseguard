"""Formatting output and exit code handling."""

import json
import sys
from typing import List

from .models import Dependency


def report_json(dependencies: List[Dependency]) -> None:
    """
    Output dependencies as JSON lines (one per dependency).

    Args:
        dependencies: List of Dependency objects to report
    """
    for dep in dependencies:
        print(json.dumps(dep.model_dump()))


def report_summary(dependencies: List[Dependency]) -> None:
    """
    Output a human-readable summary of scanned dependencies.

    Args:
        dependencies: List of Dependency objects to report
    """
    print(f"Scanned {len(dependencies)} dependencies")
    print()
    for dep in dependencies:
        print(f"  {dep.name}@{dep.version}: {dep.license}")
