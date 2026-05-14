#!/usr/bin/env python

from __future__ import annotations

import shutil
import sys
from pathlib import Path


def main() -> int:
  repo_root = Path(__file__).resolve().parent.parent
  source = repo_root / "manifest.schema.json"
  docs_dir = repo_root / "docs"
  target = docs_dir / "manifest.schema.json"
  nojekyll = docs_dir / ".nojekyll"

  if not source.exists():
    print(f"ERROR: missing source schema: {source}", file=sys.stderr)
    return 1

  docs_dir.mkdir(exist_ok=True)
  shutil.copyfile(source, target)
  nojekyll.touch()

  print("Synced manifest.schema.json -> docs/manifest.schema.json")
  return 0


if __name__ == "__main__":
  raise SystemExit(main())
