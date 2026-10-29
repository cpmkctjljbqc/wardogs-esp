# Security Policy

## Scope

`wardogs-esp` is a hobbyist cheat research project for **Wardogs** (offline
and private-server use). We do not support or endorse use in competitive
matchmaking. Reports about "my account got banned" will be closed.

## Reporting a vulnerability

- **Do not open a public issue** for kernel-driver bypass bugs or anything
  that could get users flagged by Wardogs' anti-cheat (WG-Shield).
- Email `security@wardogs-esp.dev` (PGP key in `docs/pgp.txt`) with:
  - Build hash / commit
  - Repro steps
  - Whether the issue is detectable by WG-Shield
- We aim to respond within 72h.

## Supported versions

| Branch | Supported |
|--------|-----------|
| `main` (2026.x) | ✅ |
| `legacy/2025`  | ⚠️ security fixes only |

## Known limitations

- The overlay is not signed; SmartScreen will warn on first run.
- `wardogs_native.dll` must be rebuilt per game patch when signatures rotate.
- ESP box math assumes the current 16:9 camera FOV. Ultrawide users should
  set `camera.fov_scale` in `config/local.yaml`.