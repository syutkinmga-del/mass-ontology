#!/usr/bin/env python3
"""Create and verify GitHub Release only for the owner-approved v0.4.0 tag.

Invoked on main after the real ZIP/TAR source archive and R10 authorization
passed. Uses GitHub's REST API, never creates or changes a tag, and is
idempotent only when a pre-existing release exactly matches this publication.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import sys
import urllib.error
import urllib.request

OWNER_REPO = "syutkinmga-del/mass-ontology"
TAG = "v0.4.0"
TARGET = "d0f2368df4268cfe3c6079a1681502cad0b867fb"
TAG_OBJECT = "9da6a854d663d8c3b455f96521ea87d3579646cc"
TITLE = "MASS Ontology v0.4.0 — Observation Core (BH-P04)"
EXPECTED_NOTICES = "7387ce9b98911917bb02ea9f3228fad2942fe65c8c7974d2f9890e01620f8ce5"
REQUIRED_CI_RUNS = {
    42217787701: "Validate MASS Ontology",
    42217787880: "BH-P04 Behavior Validation",
}


def request(path: str, token: str, payload: dict | None = None) -> tuple[int, dict]:
    url = "https://api.github.com/repos/" + OWNER_REPO + path
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    req = urllib.request.Request(url, data=data,
                                 method="POST" if data is not None else "GET",
                                 headers={
                                     "Authorization": "Bearer " + token,
                                     "Accept": "application/vnd.github+json",
                                     "X-GitHub-Api-Version": "2022-11-28",
                                     "User-Agent": "MASS-P04-owner-approved-release",
                                     "Content-Type": "application/json",
                                 })
    try:
        with urllib.request.urlopen(req, timeout=45) as resp:
            return resp.status, json.load(resp)
    except urllib.error.HTTPError as err:
        data = err.read()[:600].decode("utf-8", errors="replace")
        if err.code == 404 and payload is None:
            return 404, {}
        raise RuntimeError(f"GitHub API HTTP {err.code} on {path}: {data}") from err


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--notes", type=Path, required=True)
    p.add_argument("--audit", type=Path, required=True)
    args = p.parse_args()

    if os.environ.get("GITHUB_EVENT_NAME") != "push":
        raise SystemExit("BLOCKED: publication must be triggered by push to main")
    if os.environ.get("GITHUB_REF") != "refs/heads/main":
        raise SystemExit("BLOCKED: publication only on refs/heads/main")
    if os.environ.get("GITHUB_REPOSITORY") != OWNER_REPO:
        raise SystemExit("BLOCKED: wrong repository")
    token = os.environ.get("GH_TOKEN")
    if not token:
        raise SystemExit("BLOCKED: missing GitHub release-token permission")
    notes = args.notes.read_text(encoding="utf-8")
    if len(notes) < 2000 or TAG not in notes or TARGET not in notes or "BH-P05" not in notes:
        raise SystemExit("BLOCKED: release notes incomplete or not exact-tag scoped")
    if "not an electronic signature" not in notes:
        raise SystemExit("BLOCKED: R10 text approval provenance is not disclosed")
    audit = json.loads(args.audit.read_text(encoding="utf-8"))
    if not (audit.get("status") == "PASS"
            and audit.get("approved_commit_sha") == TARGET
            and audit.get("tag") == TAG
            and audit.get("source_archive_formats_match") is True
            and audit.get("publisher_rdf_checked") == 8
            and audit.get("notices_sha256") == EXPECTED_NOTICES):
        raise SystemExit("BLOCKED: exact source archive ZIP/TAR audit did not PASS")

    code, ref = request("/git/ref/tags/" + TAG, token)
    if code != 200 or ref.get("object", {}).get("type") != "tag":
        raise SystemExit("BLOCKED: source tag is absent or not annotated")
    if ref.get("object", {}).get("sha") != TAG_OBJECT:
        raise SystemExit("BLOCKED: tag object SHA is not the original owner-approved annotated tag")
    code, tag = request("/git/tags/" + TAG_OBJECT, token)
    if code != 200 or tag.get("object", {}).get("sha") != TARGET or tag.get("tag") != TAG:
        raise SystemExit("BLOCKED: annotated tag does not resolve to the exact approved commit")

    for run_id, expected_name in REQUIRED_CI_RUNS.items():
        code, run = request("/actions/runs/" + str(run_id), token)
        if code != 200 or not (
            run.get("name") == expected_name
            and run.get("head_sha") == TARGET
            and run.get("status") == "completed"
            and run.get("conclusion") == "success"
        ):
            raise SystemExit(f"BLOCKED: exact-tag candidate CI run {run_id} not successful")
        print(f"PASS candidate CI {run_id} at {TARGET}: {expected_name}", flush=True)

    code, found = request("/releases/tags/" + TAG, token)
    if code == 404:
        print("No existing GitHub Release for annotated tag; publishing", flush=True)
        code, release = request("/releases", token, payload={
            "tag_name": TAG,
            "target_commitish": TARGET,
            "name": TITLE,
            "body": notes,
            "draft": False,
            "prerelease": False,
            "generate_release_notes": False,
            "make_latest": "true",
        })
        if code != 201:
            raise SystemExit("GitHub Release creation returned unexpected HTTP status: " + str(code))
        action = "created"
    else:
        release = found
        action = "existing_verified"

    if not (
        release.get("tag_name") == TAG
        and release.get("name") == TITLE
        and release.get("body", "").strip() == notes.strip()
        and release.get("draft") is False
        and release.get("prerelease") is False
        and release.get("zipball_url")
        and release.get("tarball_url")
        and release.get("html_url") == f"https://github.com/{OWNER_REPO}/releases/tag/{TAG}"
    ):
        raise SystemExit("BLOCKED: GitHub Release metadata/content differs from approved version")

    print(json.dumps({
        "release_action": action,
        "release_id": release["id"],
        "release_url": release["html_url"],
        "tag": TAG,
        "annotated_tag_object": TAG_OBJECT,
        "approved_target": TARGET,
        "published_at": release.get("published_at"),
        "source_archives_verified": True,
        "source_zip_url_present": bool(release.get("zipball_url")),
        "source_tar_url_present": bool(release.get("tarball_url")),
    }, ensure_ascii=False, indent=2), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
