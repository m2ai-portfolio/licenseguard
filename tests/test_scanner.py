"""Tests for the dependency scanner."""

import json
import os
import tempfile
from pathlib import Path

import pytest

from licenseguard.scanner import scan_dependencies
from licenseguard.models import Dependency


@pytest.fixture
def sample_project(tmp_path):
    """Create a sample project with node_modules for testing."""
    # Create node_modules directory structure
    node_modules = tmp_path / "node_modules"
    node_modules.mkdir()

    # Create a package with MIT license
    left_pad = node_modules / "left-pad"
    left_pad.mkdir()
    (left_pad / "package.json").write_text(
        json.dumps(
            {
                "name": "left-pad",
                "version": "1.3.0",
                "license": "MIT"
            }
        )
    )

    # Create a package with ISC license
    jsdom = node_modules / "jsdom"
    jsdom.mkdir()
    (jsdom / "package.json").write_text(
        json.dumps(
            {
                "name": "jsdom",
                "version": "20.0.0",
                "license": "ISC"
            }
        )
    )

    # Create a package with license as object
    some_pkg = node_modules / "some-pkg"
    some_pkg.mkdir()
    (some_pkg / "package.json").write_text(
        json.dumps(
            {
                "name": "some-pkg",
                "version": "1.0.0",
                "license": {"type": "BSD-3-Clause"}
            }
        )
    )

    # Create a package without license field
    no_license = node_modules / "no-license"
    no_license.mkdir()
    (no_license / "package.json").write_text(
        json.dumps(
            {
                "name": "no-license",
                "version": "2.0.0"
            }
        )
    )

    # Create a scoped package
    scoped_dir = node_modules / "@babel"
    scoped_dir.mkdir()
    core = scoped_dir / "core"
    core.mkdir()
    (core / "package.json").write_text(
        json.dumps(
            {
                "name": "@babel/core",
                "version": "7.20.0",
                "license": "MIT"
            }
        )
    )

    return tmp_path


@pytest.fixture
def empty_project(tmp_path):
    """Create a project without node_modules."""
    return tmp_path


@pytest.fixture
def project_with_malformed_json(tmp_path):
    """Create a project with malformed package.json."""
    node_modules = tmp_path / "node_modules"
    node_modules.mkdir()

    bad_pkg = node_modules / "bad-pkg"
    bad_pkg.mkdir()
    (bad_pkg / "package.json").write_text("{ invalid json }")

    # Also add a valid package
    good_pkg = node_modules / "good-pkg"
    good_pkg.mkdir()
    (good_pkg / "package.json").write_text(
        json.dumps(
            {
                "name": "good-pkg",
                "version": "1.0.0",
                "license": "MIT"
            }
        )
    )

    return tmp_path


def test_scan_basic_dependencies(sample_project):
    """Test scanning a project with various dependency types."""
    deps = scan_dependencies(str(sample_project))

    assert len(deps) == 5

    # Convert to dict for easier testing
    deps_dict = {dep.name: dep for dep in deps}

    # Check MIT licensed package
    assert "left-pad" in deps_dict
    assert deps_dict["left-pad"].version == "1.3.0"
    assert deps_dict["left-pad"].license == "MIT"

    # Check ISC licensed package
    assert "jsdom" in deps_dict
    assert deps_dict["jsdom"].version == "20.0.0"
    assert deps_dict["jsdom"].license == "ISC"

    # Check package with license object
    assert "some-pkg" in deps_dict
    assert deps_dict["some-pkg"].license == "BSD-3-Clause"

    # Check package without license
    assert "no-license" in deps_dict
    assert deps_dict["no-license"].license == "UNKNOWN"

    # Check scoped package
    assert "@babel/core" in deps_dict
    assert deps_dict["@babel/core"].license == "MIT"


def test_scan_empty_project(empty_project):
    """Test scanning a project without node_modules."""
    deps = scan_dependencies(str(empty_project))
    assert len(deps) == 0


def test_scan_malformed_json(project_with_malformed_json):
    """Test that malformed package.json files are skipped gracefully."""
    deps = scan_dependencies(str(project_with_malformed_json))

    # Should only get the good package
    assert len(deps) == 1
    assert deps[0].name == "good-pkg"


def test_deduplication(tmp_path):
    """Test that duplicate packages are deduplicated."""
    node_modules = tmp_path / "node_modules"
    node_modules.mkdir()

    # Create same package twice (simulating nested node_modules)
    pkg1 = node_modules / "pkg"
    pkg1.mkdir()
    (pkg1 / "package.json").write_text(
        json.dumps(
            {
                "name": "duplicate-pkg",
                "version": "1.0.0",
                "license": "MIT"
            }
        )
    )

    # Create nested node_modules with same package
    nested = pkg1 / "node_modules"
    nested.mkdir()
    pkg2 = nested / "duplicate-pkg"
    pkg2.mkdir()
    (pkg2 / "package.json").write_text(
        json.dumps(
            {
                "name": "duplicate-pkg",
                "version": "1.0.0",
                "license": "MIT"
            }
        )
    )

    deps = scan_dependencies(str(tmp_path))

    # Should only get one instance of duplicate-pkg
    assert len(deps) == 1
    assert deps[0].name == "duplicate-pkg"


def test_different_versions_not_deduplicated(tmp_path):
    """Test that same package with different versions are not deduplicated."""
    node_modules = tmp_path / "node_modules"
    node_modules.mkdir()

    pkg1 = node_modules / "pkg-v1"
    pkg1.mkdir()
    (pkg1 / "package.json").write_text(
        json.dumps(
            {
                "name": "same-pkg",
                "version": "1.0.0",
                "license": "MIT"
            }
        )
    )

    pkg2 = node_modules / "pkg-v2"
    pkg2.mkdir()
    (pkg2 / "package.json").write_text(
        json.dumps(
            {
                "name": "same-pkg",
                "version": "2.0.0",
                "license": "MIT"
            }
        )
    )

    deps = scan_dependencies(str(tmp_path))

    # Should get both versions
    assert len(deps) == 2
    versions = {dep.version for dep in deps}
    assert "1.0.0" in versions
    assert "2.0.0" in versions
