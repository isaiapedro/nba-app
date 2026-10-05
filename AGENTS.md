# NBA Team Explorer instructions

This is an independently governed side-project repository. Application source,
project contracts, bundled data, and tests belong to this repository, never to
the parent PIOS repository.

## Start here

1. Read `manifest.yaml`, `SYSTEM.md`, `BEHAVIOR.md`, and `README.md`.
2. Use `ROADMAP.md` and `TASKS.md` to understand current priorities.
3. Preserve the imported repository history and unrelated worktree changes.
4. Run `npm run build` after source or configuration changes; run the applicable
   test command when deterministic tests exist.

## Boundaries

- Treat the checked-in NBA statistics and scraped reference snapshots as
  third-party source material with owner-scoped provenance.
- Do not add credentials, authenticated sessions, Personal records, browser
  profiles, runtime logs, generated builds, or dependency directories.
- Do not introduce a new external data service, scraping workflow, telemetry,
  or public deployment without documenting its data, privacy, retention, and
  operational consequences.
- Use the root Registry port allocation before fixing a local listener port in
  a durable contract. The development-server default is not a reserved PIOS
  service port.

## Change records

Record material architecture, dependency, data-source, privacy, or deployment
choices in `DECISIONS.md`. Update `AUDIT.md` and `TRACEABILITY.md` with bounded,
non-sensitive verification evidence when the project boundary or release state
changes.
