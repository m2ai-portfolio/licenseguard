"""Tests for the reporter module."""

import json
from io import StringIO
import sys

import pytest

from licenseguard.models import Dependency
from licenseguard.reporter import report_json, report_summary


@pytest.fixture
def sample_dependencies():
    """Create sample dependencies for testing."""
    return [
        Dependency(name="left-pad", version="1.3.0", license="MIT"),
        Dependency(name="jsdom", version="20.0.0", license="ISC"),
        Dependency(name="unknown-pkg", version="1.0.0", license="UNKNOWN"),
    ]


def test_report_json(sample_dependencies, capsys):
    """Test JSON output format."""
    report_json(sample_dependencies)

    captured = capsys.readouterr()
    lines = captured.out.strip().split("\n")

    assert len(lines) == 3

    # Parse and verify each JSON line
    dep1 = json.loads(lines[0])
    assert dep1["name"] == "left-pad"
    assert dep1["version"] == "1.3.0"
    assert dep1["license"] == "MIT"

    dep2 = json.loads(lines[1])
    assert dep2["name"] == "jsdom"
    assert dep2["version"] == "20.0.0"
    assert dep2["license"] == "ISC"

    dep3 = json.loads(lines[2])
    assert dep3["name"] == "unknown-pkg"
    assert dep3["version"] == "1.0.0"
    assert dep3["license"] == "UNKNOWN"


def test_report_json_empty(capsys):
    """Test JSON output with no dependencies."""
    report_json([])

    captured = capsys.readouterr()
    assert captured.out == ""


def test_report_summary(sample_dependencies, capsys):
    """Test summary output format."""
    report_summary(sample_dependencies)

    captured = capsys.readouterr()
    output = captured.out

    assert "Scanned 3 dependencies" in output
    assert "left-pad@1.3.0: MIT" in output
    assert "jsdom@20.0.0: ISC" in output
    assert "unknown-pkg@1.0.0: UNKNOWN" in output


def test_report_summary_empty(capsys):
    """Test summary output with no dependencies."""
    report_summary([])

    captured = capsys.readouterr()
    assert "Scanned 0 dependencies" in captured.out
