#!/usr/bin/env python

from __future__ import annotations

import json
import glob
import sys
from pathlib import Path


def load_json(path: Path):
  with path.open(encoding="utf-8") as fh:
    return json.load(fh)


def format_path(error_path):
  if not error_path:
    return "<root>"
  parts = []
  for part in error_path:
    if isinstance(part, int):
      parts.append(str(part))
    else:
      parts.append(str(part))
  return ".".join(parts)


def main() -> int:
  if len(sys.argv) < 2:
    print("Usage: python tools/validate_manifest.py <manifest.json> [more.json...]", file=sys.stderr)
    return 2

  try:
    from jsonschema import Draft202012Validator, FormatChecker
  except ImportError:
    print("Missing dependency: jsonschema")
    print("Install with: python -m pip install jsonschema")
    return 1

  repo_root = Path(__file__).resolve().parent.parent
  schema_path = repo_root / "manifest.schema.json"

  try:
    schema = load_json(schema_path)
  except OSError as exc:
    print(f"ERROR: unable to read schema {schema_path}: {exc}", file=sys.stderr)
    return 1
  except json.JSONDecodeError as exc:
    print(f"ERROR: invalid schema JSON {schema_path}: {exc}", file=sys.stderr)
    return 1

  validator = Draft202012Validator(schema, format_checker=FormatChecker())
  ok = True
  inputs = []
  for arg in sys.argv[1:]:
    matches = glob.glob(arg)
    if matches:
      inputs.extend(matches)
    else:
      inputs.append(arg)

  for arg in inputs:
    path = Path(arg)
    try:
      instance = load_json(path)
    except OSError as exc:
      print(f"ERROR: {path}: {exc}")
      ok = False
      continue
    except json.JSONDecodeError as exc:
      print(f"ERROR: {path}: invalid JSON: {exc}")
      ok = False
      continue

    errors = sorted(validator.iter_errors(instance), key=lambda err: list(err.path))
    if not errors:
      print(f"OK: {path}")
      continue

    ok = False
    print(f"INVALID: {path}")
    for error in errors:
      print(f"{format_path(error.path)}: {error.message}")

  return 0 if ok else 1


if __name__ == "__main__":
  raise SystemExit(main())
