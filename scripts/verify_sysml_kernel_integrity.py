#!/usr/bin/env python3
"""Verify the immutable MASS-SK-1.0 archived source and companion documents.

This is a byte-integrity check, NOT a SysML parser or semantic validation.
"""

import argparse
import hashlib
import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BASELINE_DIR = REPO_ROOT / "baselines" / "sysml" / "MASS-SK-1.0"
EXPECTED_SOURCE_SHA256 = "1701bbb86e24588660ef717f2ff7f276b63c938d8569d4511dc19c42033aa788"
SOURCE_NAME = "MASSKernel_v1.0.sysml"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verify(directory: Path) -> list[str]:
    errors = []
    source = directory / SOURCE_NAME
    checksum = directory / "MASSKernel_v1.0.sha256"
    manifest_file = directory / "artifact-integrity-manifest.json"
    for path in (source, checksum, manifest_file):
        if not path.is_file():
            errors.append(f"Missing required archive file: {path}")
        elif path.is_symlink():
            errors.append(f"Symlinks prohibited for controlled file: {path}")
    if errors:
        return errors

    actual = sha256(source)
    if actual != EXPECTED_SOURCE_SHA256:
        errors.append(f"Released source hash mismatch: {actual} != {EXPECTED_SOURCE_SHA256}")

    raw = checksum.read_text(encoding="utf-8")
    m = re.fullmatch(r"([0-9a-f]{64})  MASSKernel_v1\.0\.sysml\n?", raw)
    if m is None:
        errors.append("Source checksum file must contain exactly the canonical sha256sum line")
    elif m.group(1) != EXPECTED_SOURCE_SHA256:
        errors.append("Source checksum file does not match pinned SHA-256")

    try:
        meta = json.loads(manifest_file.read_text(encoding="utf-8"))
        if meta.get("baseline_id") != "MASS-SK-1.0":
            errors.append("Baseline identifier mismatch")
        if meta.get("released_source_sha256") != EXPECTED_SOURCE_SHA256:
            errors.append("Manifest's released source SHA-256 is incorrect")
        entries = meta.get("files", [])
        names = [x.get("path") for x in entries]
        if len(names) != len(set(names)) or len(entries) < 6:
            errors.append("Duplicate or missing manifest records")
        for entry in entries:
            name = entry.get("path", "")
            if not isinstance(name, str) or name != Path(name).name:
                errors.append(f"Non-local artifact name: {name!r}")
                continue
            path = directory / name
            if not path.is_file() or path.is_symlink():
                errors.append(f"Missing/non-regular archived artifact: {name}")
                continue
            if sha256(path) != entry.get("sha256"):
                errors.append(f"Artifact checksum mismatch: {name}")
            if path.stat().st_size != entry.get("bytes"):
                errors.append(f"Artifact byte-length mismatch: {name}")
        if SOURCE_NAME not in names or "MASSKernel_v1.0.sha256" not in names:
            errors.append("Essential files missing from integrity manifest")
    except (OSError, ValueError, TypeError, AttributeError) as e:
        errors.append(f"Invalid integrity manifest: {e}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline-dir", type=Path, default=DEFAULT_BASELINE_DIR)
    args = parser.parse_args()
    issues = verify(args.baseline_dir)
    if issues:
        print("MASS-SK-1.0 SOURCE INTEGRITY: FAIL")
        for issue in issues:
            print(f"- {issue}")
        return 1
    print("MASS-SK-1.0 SOURCE INTEGRITY: PASS")
    print(f"Baseline: MASS-SK-1.0; SHA-256: {EXPECTED_SOURCE_SHA256}")
    print("Checks: released source bytes, checksum line, archive manifest and companion document hashes")
    print("Note: does not execute a SysML parser or claim current Pilot Implementation validation")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
