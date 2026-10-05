# Audit log

## 2026-09-18 — Workspace import baseline

- Cloned `https://github.com/isaiapedro/nba-app.git` at revision
  `043fed7105c4a7d8818edc77d4a458be717cdf2b` on branch `main`.
- Applied the side-project template controls without rewriting imported source
  or history.
- Registered the independent repository boundary and personal Git identity.
- `npm ci --no-audit --no-fund` completed from the committed lockfile using
  Node 24.14.0 and npm 11.9.0. Upstream deprecation warnings were emitted for
  `inflight`, `rimraf@3`, and `glob@7`.
- `npm run build` failed because `src/app/player-page/player-page.ts` imports
  `@ng-bootstrap/ng-bootstrap`, which is absent from the project dependencies.
  The compiler also reported non-fatal CSS syntax and unused-import warnings.
- Root `python3 registry/implementation/cli.py check` passed with 44 components,
  10 registered repositories, 12 fail-closed unmanaged scopes, passing
  governance tests, and passing Git whitespace validation. The Registry
  snapshot was rebuilt afterward.
- This is an import baseline, not a claim of a green application build,
  production behavior, or user-runtime validation.

## 2026-09-21 — Dependency repair and verification baseline

- Removed the unused `@ng-bootstrap/ng-bootstrap` import and unused Angular
  Material imports; no new runtime data source, backend, credential, or
  Personal-data flow was introduced.
- Updated the Angular 20 dependency floor to 20.3.28 and regenerated the lock
  file. The resolved framework packages are on 20.3.31 and the build tooling is
  on 20.3.37; compatible transitive security updates were then applied.
- Added six deterministic Jasmine assertions for root navigation, navigation
  surfaces, team search initialization/filtering, and player search/filtering.
  `npm test -- --watch=false` passed in Puppeteer-managed Chrome Headless
  153.0.0.0.
- `npm run build` passed with a 572.50 kB initial bundle, below the documented
  600 kB warning budget and 1 MB error budget.
- `npm audit` completed with 0 vulnerabilities across 563 resolved packages.

## Scope note

This verifies build, dependency, route-configuration, and component-search
behavior. It does not claim that the empty MVP predictor route is implemented
or that the bundled sports datasets have been refreshed or independently
validated.

## 2026-09-21 — Local pipeline recovery baseline

- Inspected the recovered `nba-tests/` material. Its historical Airflow DAG
  declared extract/transform/load tasks but imported a nonexistent module and
  had no PostgreSQL implementation, schema, Compose setup, or dependency
  definition.
- Added a local Airflow 2.10.5/PostgreSQL Compose architecture with separate
  Airflow metadata, curated NBA, immutable raw-artifact, inbox, and candidate
  storage volumes. No service has a host-port mapping.
- Added snapshot validation and publication tests. Three tests passed; the
  current frontend data also passed the canonical contract check with 30 teams
  and 230 players, including permitted source aggregate `2TM` player rows.
- `docker compose --env-file .env.example config --quiet` passed. The custom
  Airflow image built successfully and an isolated container import check passed
  for Airflow 2.10.5, psycopg2, and the PostgreSQL provider.
- No containers were started, no web request was made by the pipeline, and no
  source data was refreshed. The legacy Basketball Reference scraper remains
  disabled pending authorization.

## 2026-09-21 — Local-secret removal and dashboard boundary

- Removed the Airflow administrator password, both PostgreSQL password
  variables, and administrator bootstrap from the Compose configuration and
  `.env` template. The password-era Airflow and NBA PostgreSQL volumes were
  deleted after explicit approval.
- Restored the webserver with anonymous access on development port `8765`.
  Local-network exposure was explicitly approved because loopback Docker
  forwarding did not reach the browser. The dashboard configuration is mounted
  as `webserver_config.py` and grants the anonymous role Admin access.
- `airflow db migrate` completed against the fresh credential-free metadata
  database. The running webserver returned HTTP 200 for `/home` without a
  login from inside its container; the scheduler and both PostgreSQL services
  were healthy.

## 2026-09-21 — Local-secret removal

- Removed the Airflow administrator password, both PostgreSQL password
  variables, Airflow webserver service, and administrator bootstrap from the
  Compose configuration and `.env` template.
- Config validation completed with no password or webserver references in the
  pipeline configuration. The old password-based Compose containers and network
  were stopped and removed; named volumes were deliberately retained.
- Deleted the two confirmed password-era PostgreSQL volumes
  (`pipeline_airflow_db` and `pipeline_nba_db`) after explicit approval. This
  permanently removed their Airflow metadata, curated NBA rows, raw-artifact
  records, and prior database credential hashes; the next stack initialization
  will use the credential-free configuration.
