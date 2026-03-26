"""Data models for LicenseGuard."""

from __future__ import annotations
from typing import List, Optional
from pydantic import BaseModel


class Dependency(BaseModel):
    """Represents a scanned npm dependency with its license information."""

    name: str
    version: str
    license: str  # SPDX identifier or raw string; may be "UNKNOWN"


class Policy(BaseModel):
    """Represents a license compliance policy."""

    allowed: Optional[List[str]] = None
    denied: Optional[List[str]] = None

    def is_allowed(self, lic: str) -> bool:
        """
        Check if a license is allowed by the policy.

        Args:
            lic: License identifier to check

        Returns:
            False if the license is denied or not in the allowed list (when specified)
            True otherwise
        """
        if self.denied and lic in self.denied:
            return False
        if self.allowed and lic not in self.allowed:
            return False
        return True
