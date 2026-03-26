"""Policy loading and evaluation logic."""

import json
from pathlib import Path
from typing import Optional

from .models import Policy


def load_policy(policy_path: Optional[str] = None) -> Policy:
    """
    Load a policy from a JSON file.

    Args:
        policy_path: Path to the policy JSON file. If None, returns an empty policy.

    Returns:
        Policy object with allowed and denied lists
    """
    if policy_path is None:
        return Policy()

    policy_file = Path(policy_path)

    if not policy_file.exists():
        raise FileNotFoundError(f"Policy file not found: {policy_path}")

    try:
        with open(policy_file, "r", encoding="utf-8") as f:
            policy_data = json.load(f)
            return Policy(**policy_data)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in policy file: {e}")
    except Exception as e:
        raise ValueError(f"Failed to load policy: {e}")
