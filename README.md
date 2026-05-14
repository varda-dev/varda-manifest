# Varda Manifest

`varda-manifest` is source of truth for Varda server manifest JSON contract.

- Current schema file: `manifest.schema.json`
- Current schema version: `2`
- Producer: `varda-modpack`
- Consumer: `varda-server-installer`

This repo defines shared shape for manifest emitted by modpack and read by installer. Installer-specific safety logic still lives in installer code.

## Validate

```powershell
python -m pip install jsonschema
python tools/validate_manifest.py examples/manifest.example.json
python tools/validate_manifest.py testdata/valid/manifest.v2.json
```

## Integration

### `varda-modpack`

- Generate `docs/manifest.json`.
- Validate generated file against `manifest.schema.json` before publish.
- Start by copying this schema repo or pinning it as submodule/vendor copy.
- Do not publish if validation fails.

### `varda-server-installer`

- Keep Go structs local for now.
- Add tests that load valid and invalid fixtures from this repo or a pinned copy.
- Installer-specific safety checks remain in installer code:
  - safe inferred jar filenames
  - ZIP traversal checks
  - application of manifest to filesystem
- JSON Schema is shared contract; installer code still owns installation behavior.

## Compatibility Policy

- Additive optional fields should be added carefully and tested.
- `schema_version` should only change when old consumers must reject manifest.
- Do not change existing required field meaning without schema version bump.
- Tag this repo when schema changes release.

## Validation Script

`tools/validate_manifest.py` validates one or more manifest files against schema. It prints `OK: <path>` for valid files and readable errors for invalid files.
