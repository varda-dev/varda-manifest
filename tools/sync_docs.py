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
  index_html = docs_dir / "index.html"

  if not source.exists():
    print(f"ERROR: missing source schema: {source}", file=sys.stderr)
    return 1

  docs_dir.mkdir(exist_ok=True)
  shutil.copyfile(source, target)
  nojekyll.touch()

  index_html.write_text(
    """<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Varda Manifest Schema</title>
  </head>
  <body>
    <main>
      <h1>Varda Manifest Schema</h1>
      <p>Canonical JSON Schema for the Varda server manifest.</p>
      <ul>
        <li><a href="manifest.schema.json">manifest.schema.json</a></li>
        <li><a href="https://github.com/varda-dev/varda-manifest">GitHub repo</a></li>
        <li><a href="https://github.com/varda-dev/varda-modpack">varda-modpack</a></li>
        <li><a href="https://github.com/varda-dev/varda-server-installer">varda-server-installer</a></li>
      </ul>
      <p>Example validation commands:</p>
      <pre><code>python tools/sync_docs.py
python tools/validate_manifest.py examples/manifest.example.json testdata/valid/manifest.v2.json
python tools/validate_manifest.py testdata/invalid/*.json</code></pre>
    </main>
  </body>
</html>
""",
    encoding="utf-8",
  )

  print("Synced manifest.schema.json -> docs/manifest.schema.json")
  print("Wrote docs/index.html")
  return 0


if __name__ == "__main__":
  raise SystemExit(main())
