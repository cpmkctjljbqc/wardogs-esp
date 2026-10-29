# Contributing to wardogs-esp

Thanks for wanting to help the Wardogs Cheats project. This is a community
hobbyist repo — treat it like any other open-source modding project.

## Ground rules

- **Educational / research use only.** Do not ship builds aimed at ranked
  matchmaking abuse; test on offline lobbies, private servers, and your own
  Wardogs install.
- Keep PRs focused. One feature per PR. No drive-by refactors of the
  overlay renderer.
- Match the existing folder layout: `src/main` owns the process + IPC,
  `src/preload` owns the bridge, `src/renderer` owns the UI, `src/shared`
  owns contracts, `src-native` owns the C++ helper.
- Python 3.11+ only. Type hints required on new public functions.
- Run `pytest tests/` before opening a PR.

## Adding a new feature handler

1. Drop the handler in `src/main/features/`.
2. Register it in `src/main/features/registry.py`.
3. Add the toggle key to `config/toggles.default.yaml`.
4. Add a stub test in `tests/`.

## Offset updates

Wardogs patches every ~2 weeks. When offsets break, update
`src/main/memory/offsets.py` and bump `OFFSETS_VERSION`. Do not commit
raw signatures — put them in `config/signatures.json`.

## Code of conduct

Be cool. No leaks of paid cheat sources, no doxxing, no drama.