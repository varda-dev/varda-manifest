# Varda Manifest

`varda-manifest` defines the JSON Schema contract for the Varda server manifest.

The schema is used by:

- `varda-modpack` to validate the manifest it produces
- `varda-server-installer` to understand the manifest shape it consumes

## Schema

Canonical source:

```text
manifest.schema.json
```

Published GitHub Pages copy:

```text
docs/manifest.schema.json
```

Public URL:

```text
https://varda-dev.github.io/varda-manifest/manifest.schema.json
```

Current schema version:

```text
2
```

The root `manifest.schema.json` file is the source of truth. The copy under `docs/` exists only so GitHub Pages can publish it.

## Setup

Install the Python validation dependency:

```powershell
python -m pip install jsonschema
```

The helper scripts are plain Python scripts and do not require this repo to be installed as a package.

## Scripts

### `tools/sync_docs.py`

Copies the canonical schema into the GitHub Pages directory.

Run this after editing `manifest.schema.json`:

```powershell
python tools/sync_docs.py
```

It updates:

```text
docs/manifest.schema.json
docs/index.html
docs/.nojekyll
```

### `tools/validate_manifest.py`

Validates one or more manifest JSON files against the root schema.

Run:

```powershell
python tools/validate_manifest.py examples/manifest.example.json testdata/valid/manifest.v2.json
```

Expected output:

```text
OK: examples/manifest.example.json
OK: testdata/valid/manifest.v2.json
```

Validate the intentionally invalid fixtures:

```powershell
python tools/validate_manifest.py testdata/invalid/*.json
```

That command is expected to fail. Those files exist to prove the schema rejects bad manifests.

## Normal workflow

Before committing schema changes, run:

```powershell
python tools/sync_docs.py
python tools/validate_manifest.py examples/manifest.example.json testdata/valid/manifest.v2.json
python tools/validate_manifest.py testdata/invalid/*.json
```

The first validation command should pass.

The invalid fixture command should fail.

## Consumer guidance

### `varda-modpack`

`varda-modpack` should validate its generated `docs/manifest.json` before publishing.

Recommended schema URL:

```text
https://varda-dev.github.io/varda-manifest/manifest.schema.json
```

If validation fails, the manifest should not be published.

### `varda-server-installer`

`varda-server-installer` should not fetch the schema at runtime.

The installer should stay self-contained and keep its own Go validation for installer-specific behavior, such as:

- safe inferred `.jar` filenames
- ZIP traversal protection
- applying the manifest to the server directory

## Compatibility policy

Only bump `schema_version` when old consumers must reject the manifest.

Safe changes usually include adding optional fields. Unsafe changes include changing the meaning of required fields, removing required fields, or changing hash/URL semantics.

Tag this repo when releasing schema changes.
