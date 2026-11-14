# Artifacts

Large generated outputs and local rebuild products go here.

## Current artifacts

| File | What | Source | Rebuild |
|---|---|---|---|
| `confucius_laozi.db` | SQLite database: 10 sources, 16 passages, 9 topics, 5 date claims, 2 objects, 10 scholarship records | `../sources/processed/passages.json` | `python code/build_db.py` |

This directory is ignored by git except for this README. The JSON dataset and
the build script are the durable record; the database is disposable.
