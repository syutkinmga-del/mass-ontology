#!/usr/bin/env python3
"""Fail-closed audit of GitHub generated ZIP/TAR source archives at v0.4.0.

This validates the *actual downloaded GitHub-generated* archives, not just a
checkout. Every archived file must match its exact blob in the owner-approved
Git tree. The publisher snapshots have additional frozen SHA-256 checks.
Never creates a tag or release.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path, PurePosixPath
import subprocess
import sys
import tarfile
import zipfile

EXPECTED_TAG = "v0.4.0"
EXPECTED_COMMIT = "d0f2368df4268cfe3c6079a1681502cad0b867fb"
EXPECTED_NOTICES = "7387ce9b98911917bb02ea9f3228fad2942fe65c8c7974d2f9890e01620f8ce5"
EXPECTED_LICENSE = "cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30"
MAX_ENTRY_BYTES = 30_000_000
MAX_ARCHIVE_BYTES = 90_000_000
MANDATORY = (
    "VERSION", "pyproject.toml", "README.md", "LICENSE",
    "THIRD_PARTY_NOTICES.md", "CHANGELOG.md",
    "docs/releases/v0.4.0-release-notes.md",
    "docs/standards/T04-external-rdf-lock.json",
    "docs/licenses/third-party/OGC-1.0-LICENSE.txt",
    "docs/licenses/third-party/W3C-20150513-LICENSE.txt",
    "docs/governance/DEC-P04-07-RR05-2026-02-chat-approval.md",
    "docs/governance/DEC-P04-07-rights-approval.json",
    "scripts/review_release_p04_candidate.py",
    "docs/evidence/P04-06/ci-acceptance.json",
    "baselines/sysml/MASS-SK-1.0/MASSKernel_v1.0.sysml",
)
PROHIBITED_IN_TAG = (
    "docs/governance/DEC-P04-07-R10-2026-02-chat-approval.md",
    "docs/governance/P04-07-R10-2026-02-release-target.json",
)


def git(*args: str) -> bytes:
    p = subprocess.run(["git", *args], stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE, check=False, timeout=45)
    if p.returncode:
        raise ValueError(f"git {' '.join(args)} failed: {p.stderr[-700:]!r}")
    return p.stdout


def git_blobs(target: str) -> dict[str, tuple[str, str]]:
    out = {}
    for line in git("ls-tree", "-rz", "--full-tree", target).split(b"\0"):
        if not line:
            continue
        hdr, pathname = line.split(b"\t", 1)
        mode, kind, sha = hdr.decode("ascii").split()
        if kind != "blob" or mode not in ("100644", "100755", "120000"):
            raise ValueError(f"Unsupported tagged Git entry {mode} {kind}: {pathname!r}")
        name = pathname.decode("utf-8")
        out[name] = (mode, sha)
    return out


def blob_sha1(payload: bytes) -> str:
    hdr = b"blob " + str(len(payload)).encode("ascii") + b"\0"
    return hashlib.sha1(hdr + payload).hexdigest()


def safe_name(full: str, prefix: str) -> str | None:
    if not full.startswith(prefix + "/"):
        raise ValueError("Archive contains unexpected top-level prefix: " + full)
    name = full[len(prefix) + 1:]
    if not name:
        return None
    parts = PurePosixPath(name).parts
    if not parts or name.startswith("/") or any(x in (".", "..") for x in parts):
        raise ValueError("Archive has unsafe entry: " + full)
    return name


def read_zip(path: Path) -> dict[str, bytes]:
    results = {}
    with zipfile.ZipFile(path) as z:
        names = z.namelist()
        top = {name.split("/", 1)[0] for name in names}
        if len(top) != 1:
            raise ValueError("ZIP must have exactly one top-level folder")
        prefix = next(iter(top))
        for entry in z.infolist():
            rel = safe_name(entry.filename, prefix)
            if rel is None or entry.is_dir():
                continue
            if entry.file_size > MAX_ENTRY_BYTES:
                raise ValueError("ZIP entry exceeds limit: " + rel)
            if rel in results:
                raise ValueError("Duplicate ZIP entry: " + rel)
            with z.open(entry) as f:
                body = f.read(MAX_ENTRY_BYTES + 1)
            if len(body) != entry.file_size or len(body) > MAX_ENTRY_BYTES:
                raise ValueError("ZIP entry size mismatch: " + rel)
            results[rel] = body
    return results


def read_tar(path: Path) -> dict[str, bytes]:
    results = {}
    with tarfile.open(path, "r:gz") as t:
        members = t.getmembers()
        top = {m.name.split("/", 1)[0] for m in members}
        if len(top) != 1:
            raise ValueError("TAR must have exactly one top-level folder")
        prefix = next(iter(top))
        for m in members:
            rel = safe_name(m.name, prefix)
            if rel is None or m.isdir():
                continue
            if not (m.isfile() or m.issym()):
                raise ValueError("Unexpected TAR type: " + m.name)
            if m.size > MAX_ENTRY_BYTES:
                raise ValueError("TAR entry exceeds limit: " + rel)
            if rel in results:
                raise ValueError("Duplicate TAR entry: " + rel)
            if m.issym():
                body = m.linkname.encode("utf-8")
            else:
                source = t.extractfile(m)
                if source is None:
                    raise ValueError("Cannot read TAR entry: " + rel)
                body = source.read(MAX_ENTRY_BYTES + 1)
                if len(body) != m.size:
                    raise ValueError("TAR entry size mismatch: " + rel)
            if len(body) > MAX_ENTRY_BYTES:
                raise ValueError("TAR uncompressed entry too large")
            results[rel] = body
    return results


def verify_payload(label: str, files: dict[str, bytes],
                   expected: dict[str, tuple[str, str]]) -> dict:
    missing = sorted(set(expected) - set(files))
    unexpected = sorted(set(files) - set(expected))
    if missing or unexpected:
        raise ValueError(f"{label} differs from approved Git tree: missing={missing!r}, extra={unexpected!r}")
    mismatches = [name for name, value in files.items()
                  if blob_sha1(value) != expected[name][1]]
    if mismatches:
        raise ValueError(f"{label} contents differ from Git blob SHAs: {mismatches!r}")
    return {
        "format": label,
        "all_files_match_approved_git_blobs": True,
        "file_count": len(files),
        "uncompressed_bytes": sum(len(b) for b in files.values()),
    }


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--zip", type=Path, required=True)
    p.add_argument("--tar", type=Path, required=True)
    p.add_argument("--report", type=Path, required=True)
    args = p.parse_args()
    outcome = {
        "schema_version": "P04-07-publication-archive-validation-v1",
        "reviewed_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "tag": EXPECTED_TAG,
        "approved_commit_sha": EXPECTED_COMMIT,
        "status": "FAIL",
        "failures": [],
        "publisher_rdf_checked": 0,
        "release_created_by_verifier": False,
    }
    try:
        actual_commit = git("rev-parse", f"refs/tags/{EXPECTED_TAG}^{{commit}}").decode().strip()
        actual_kind = git("cat-file", "-t", f"refs/tags/{EXPECTED_TAG}").decode().strip()
        if actual_commit != EXPECTED_COMMIT or actual_kind != "tag":
            raise ValueError("v0.4.0 must be an annotated tag at the exactly approved commit")
        expected = git_blobs(EXPECTED_COMMIT)
        paths = (args.zip, args.tar)
        if not all(x.is_file() and 0 < x.stat().st_size <= MAX_ARCHIVE_BYTES for x in paths):
            raise ValueError("Missing/empty/oversized downloaded GitHub source archive")

        zip_files = read_zip(args.zip)
        tar_files = read_tar(args.tar)
        results = [verify_payload("zip", zip_files, expected),
                   verify_payload("tar.gz", tar_files, expected)]
        if zip_files.keys() != tar_files.keys() or any(
            tar_files[name] != data for name, data in zip_files.items()
        ):
            raise ValueError("GitHub ZIP and TAR source archive contents differ")
        for x in MANDATORY:
            if x not in zip_files:
                raise ValueError("Mandatory redistributable file absent: " + x)
        for x in PROHIBITED_IN_TAG:
            if x in zip_files:
                raise ValueError("Post-target approval registration leaked into frozen tag: " + x)

        if zip_files["VERSION"] != b"0.4.0\n":
            raise ValueError("Unexpected VERSION in tagged archive")
        if b'version = "0.4.0"' not in zip_files["pyproject.toml"]:
            raise ValueError("Unexpected Python package version")
        for path, approved_sha in (
            ("LICENSE", EXPECTED_LICENSE),
            ("THIRD_PARTY_NOTICES.md", EXPECTED_NOTICES)
        ):
            digest = hashlib.sha256(zip_files[path]).hexdigest()
            if digest != approved_sha:
                raise ValueError(f"Approved {path} SHA-256 mismatch: {digest}")
        lock = json.loads(zip_files["docs/standards/T04-external-rdf-lock.json"])
        inventory = lock.get("files", [])
        if len(inventory) != 8:
            raise ValueError("T-04 lock does not list precisely eight external RDF artifacts")
        if len({x["repo_path"] for x in inventory}) != 8:
            raise ValueError("Duplicate external RDF artifact lock entries")
        observed = {p for p in zip_files if p.startswith("vendor/external-rdf/T04-2026/") and p.endswith(".ttl")}
        expected_rdf = {x["repo_path"] for x in inventory}
        if observed != expected_rdf:
            raise ValueError("Third-party RDF archive inventory differs from pinned T-04 lock")
        for entry in inventory:
            rel = entry["repo_path"]
            body = zip_files[rel]
            if hashlib.sha256(body).hexdigest() != entry["sha256"]:
                raise ValueError("T-04 RDF SHA-256 mismatch: " + rel)
            if len(body) != entry["file_size_bytes"]:
                raise ValueError("T-04 RDF byte size differs from pinned lock: " + rel)
        rights = json.loads(zip_files["docs/governance/DEC-P04-07-rights-approval.json"])
        if rights.get("third_party_notices_sha256") != EXPECTED_NOTICES:
            raise ValueError("RR-05 rights approval does not match archived THIRD_PARTY_NOTICES.md")
        if rights.get("project_license_sha256") != EXPECTED_LICENSE:
            raise ValueError("RR-04 rights approval does not match archived LICENSE")
        if not (
            b"W3C" in zip_files["docs/licenses/third-party/W3C-20150513-LICENSE.txt"]
            and b"OGC" in zip_files["docs/licenses/third-party/OGC-1.0-LICENSE.txt"]
        ):
            raise ValueError("Third-party license text missing or incomplete")
        outcome.update({
            "status": "PASS",
            "inventory_counts": results,
            "publisher_rdf_checked": len(inventory),
            "tree_file_count": len(expected),
            "source_archive_formats_match": True,
            "git_tag_object_type": actual_kind,
            "license_sha256": EXPECTED_LICENSE,
            "notices_sha256": EXPECTED_NOTICES,
            "zip_sha256": hashlib.sha256(args.zip.read_bytes()).hexdigest(),
            "tar_sha256": hashlib.sha256(args.tar.read_bytes()).hexdigest(),
        })
    except Exception as exc:
        outcome["failures"].append(f"{type(exc).__name__}: {exc}")

    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(outcome, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(outcome, indent=2, ensure_ascii=False), flush=True)
    return 0 if outcome["status"] == "PASS" else 2


if __name__ == "__main__":
    sys.exit(main())
