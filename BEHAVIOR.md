# Development behavior

## Purpose

Iterate on a browser-based NBA team, roster, and player explorer while keeping
the application small, understandable, and reproducible.

## Principles

- Prefer the bundled, versioned datasets for deterministic browsing behavior.
- Keep presentation, navigation, and data access responsibilities distinct.
- Add tests for repaired behavior and document important design decisions.
- Treat the MVP predictor and scraping notebook as experimental surfaces until
  their inputs, outputs, and acceptance criteria are documented.
- Keep pipeline ingestion manual and approval-gated unless the source owner has
  authorized automation; preserve raw artifacts and publish only reviewed
  Angular snapshots.
- The credential-free Airflow dashboard is permitted only on development port
  `8765` for the explicitly approved local-network browser boundary; do not
  use it for a public interface or add a webserver elsewhere without a
  separately approved access boundary.
- Promote generally reusable capabilities only through an explicit service
  decision; this side project does not provide a stable shared API.

## Lifecycle

The project is an active prototype. Source and project contracts persist in
the nested repository while active. Generated builds, caches, dependencies,
runtime output, and local configuration are disposable and must remain
untracked. Archive or promote the project intentionally when its purpose
changes.
