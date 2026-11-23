"""
Data Loading and Integrity Verification Module.
Provides robust schema validation and input verification for Domain B datasets.
"""

import os
import hashlib
import pandas as pd


def compute_sha256(filepath):
    """Compute cryptographic SHA-256 hash of a file."""
    h = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def load_dataset(filepath, expected_sha256=None, expected_rows=None):
    """
    Load a CSV dataset with optional cryptographic hash and row count verification.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Dataset not found at: {filepath}")

    if expected_sha256:
        actual_sha = compute_sha256(filepath)
        if actual_sha.lower() != expected_sha256.lower():
            raise ValueError(
                f"Cryptographic hash mismatch for {filepath}:\n"
                f"  Expected: {expected_sha256}\n"
                f"  Actual:   {actual_sha}"
            )

    df = pd.read_csv(filepath)

    if expected_rows is not None and len(df) != expected_rows:
        raise ValueError(
            f"Row count mismatch for {filepath}: expected {expected_rows}, got {len(df)}"
        )

    return df
