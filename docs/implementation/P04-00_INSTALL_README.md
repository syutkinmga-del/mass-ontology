# P04-00 installation and baseline evidence capture

1. Do **not** overwrite approved DCCR-01…04, the immutable SysML Kernel or production ontology TTL files.
2. Copy/extract this archive at the root of `~/Projects/mass-ontology` (the archive paths are relative to the repository root).
3. Check staged whitespace with `git diff --check` and ensure `docs/index.md` can link to these P04-00 documents if desired.
4. Execute from repository root: `python3 scripts/capture_p04_baseline.py`.
5. Send the console result and the JSON report contents (redact local paths if desired) for an evidence-based P04-00 gate review. Logs and JSON are written to `../mass-ontology-p04-00-evidence/` outside the repository.
6. `make catalog`, `make validate`, `make cq`, and `make test` are existing commands; a missing `.venv/bin/python` gives BLOCKED rather than a false PASS. The script does not install packages.
7. After local review of DRAFT policies, add files to git and make a new commit. Do not call the P04-00 gate complete until legacy tests have actually executed and key policies are decided.

**Remote GitHub snapshot at authoring:** `44d7131fac9c0827fa973e06067200e5b31f3328`. It is a historical anchor and does not automatically change when the GitHub branch advances.
