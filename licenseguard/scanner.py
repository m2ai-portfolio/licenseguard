"""Dependency scanner for extracting license information from node_modules."""

import json
import os
from pathlib import Path
from typing import List, Set, Tuple

from .models import Dependency


def scan_dependencies(project_path: str) -> List[Dependency]:
    """
    Scan node_modules directory and extract license information from each package.

    Args:
        project_path: Path to the project directory containing node_modules

    Returns:
        List of Dependency objects with name, version, and license information
    """
    project_dir = Path(project_path).resolve()
    node_modules = project_dir / "node_modules"

    if not node_modules.exists():
        return []

    dependencies = []
    seen: Set[Tuple[str, str]] = set()  # Track (name, version) to deduplicate

    # Walk through node_modules directory
    for root, dirs, files in os.walk(node_modules):
        # Check if this directory contains a package.json
        if "package.json" in files:
            package_json_path = Path(root) / "package.json"

            try:
                with open(package_json_path, "r", encoding="utf-8") as f:
                    package_data = json.load(f)

                # Extract package information
                name = package_data.get("name", "UNKNOWN")
                version = package_data.get("version", "UNKNOWN")

                # Handle license field - can be string or object
                license_field = package_data.get("license", "UNKNOWN")

                if isinstance(license_field, dict):
                    # License can be an object with "type" key
                    license_str = license_field.get("type", "UNKNOWN")
                elif isinstance(license_field, str):
                    license_str = license_field
                else:
                    license_str = "UNKNOWN"

                # Deduplicate by (name, version)
                dep_key = (name, version)
                if dep_key not in seen:
                    seen.add(dep_key)
                    dependencies.append(
                        Dependency(
                            name=name,
                            version=version,
                            license=license_str
                        )
                    )

            except (json.JSONDecodeError, OSError, UnicodeDecodeError):
                # Skip malformed or unreadable package.json files
                continue

    return dependencies
