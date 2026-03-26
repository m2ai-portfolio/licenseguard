"""Tests for policy loading and evaluation."""

import json
import tempfile
from pathlib import Path

import pytest

from licenseguard.policy import load_policy
from licenseguard.models import Policy


def test_load_policy_none():
    """Test loading policy with no file returns empty policy."""
    policy = load_policy(None)
    assert policy.allowed is None
    assert policy.denied is None


def test_load_policy_allowed_list(tmp_path):
    """Test loading policy with allowed list."""
    policy_file = tmp_path / "policy.json"
    policy_file.write_text(
        json.dumps(
            {
                "allowed": ["MIT", "ISC", "BSD-3-Clause"]
            }
        )
    )

    policy = load_policy(str(policy_file))
    assert policy.allowed == ["MIT", "ISC", "BSD-3-Clause"]
    assert policy.denied is None


def test_load_policy_denied_list(tmp_path):
    """Test loading policy with denied list."""
    policy_file = tmp_path / "policy.json"
    policy_file.write_text(
        json.dumps(
            {
                "denied": ["GPL-2.0", "GPL-3.0", "AGPL-3.0"]
            }
        )
    )

    policy = load_policy(str(policy_file))
    assert policy.allowed is None
    assert policy.denied == ["GPL-2.0", "GPL-3.0", "AGPL-3.0"]


def test_load_policy_both_lists(tmp_path):
    """Test loading policy with both allowed and denied lists."""
    policy_file = tmp_path / "policy.json"
    policy_file.write_text(
        json.dumps(
            {
                "allowed": ["MIT", "ISC"],
                "denied": ["GPL-3.0"]
            }
        )
    )

    policy = load_policy(str(policy_file))
    assert policy.allowed == ["MIT", "ISC"]
    assert policy.denied == ["GPL-3.0"]


def test_load_policy_file_not_found():
    """Test that loading non-existent policy raises FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        load_policy("/nonexistent/policy.json")


def test_load_policy_invalid_json(tmp_path):
    """Test that invalid JSON raises ValueError."""
    policy_file = tmp_path / "policy.json"
    policy_file.write_text("{ invalid json }")

    with pytest.raises(ValueError, match="Invalid JSON"):
        load_policy(str(policy_file))


def test_policy_is_allowed_no_restrictions():
    """Test that empty policy allows all licenses."""
    policy = Policy()

    assert policy.is_allowed("MIT")
    assert policy.is_allowed("GPL-3.0")
    assert policy.is_allowed("UNKNOWN")


def test_policy_is_allowed_with_allowlist():
    """Test policy with allow list."""
    policy = Policy(allowed=["MIT", "ISC"])

    assert policy.is_allowed("MIT")
    assert policy.is_allowed("ISC")
    assert not policy.is_allowed("GPL-3.0")
    assert not policy.is_allowed("UNKNOWN")


def test_policy_is_allowed_with_denylist():
    """Test policy with deny list."""
    policy = Policy(denied=["GPL-2.0", "GPL-3.0"])

    assert policy.is_allowed("MIT")
    assert policy.is_allowed("ISC")
    assert not policy.is_allowed("GPL-2.0")
    assert not policy.is_allowed("GPL-3.0")
    assert policy.is_allowed("UNKNOWN")


def test_policy_is_allowed_both_lists():
    """Test policy with both allow and deny lists - deny takes precedence."""
    policy = Policy(allowed=["MIT", "ISC", "GPL-3.0"], denied=["GPL-3.0"])

    assert policy.is_allowed("MIT")
    assert policy.is_allowed("ISC")
    assert not policy.is_allowed("GPL-3.0")  # Denied even though in allowed
    assert not policy.is_allowed("BSD-3-Clause")  # Not in allowed list
