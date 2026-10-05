# Architectural decisions

## 2026-09-18 — Import as an independent side-project repository

**Decision:** Place `isaiapedro/nba-app` at
`workspace/side_projects/nba-app` as a registered nested repository and apply
the `templates/side_projects/` control pattern.

**Reason:** The application is an independent prototype with its own Git
history, source, datasets, and lifecycle. The parent PIOS repository governs
only its structural boundary.

**Alternatives:** Importing its source into the PIOS root was rejected because
the root repository excludes application implementation. Treating it as a
service was rejected because it exposes no stable shared capability.

**Consequences:** Source and project contracts commit only to `nba-app`.
Generated output, dependencies, credentials, and runtime material stay local.

## 2026-09-18 — Preserve imported sports-data snapshots in the owner boundary

**Decision:** Retain the existing JSON, CSV, notebook, and historical HTML
material in the nested repository without promoting it to PIOS Knowledge or
Registry payloads.

**Reason:** These files are inputs and provenance artifacts of the imported
application, not objective PIOS consensus records.

**Consequences:** Any future refresh, redistribution, or external scraping
workflow requires a separate provenance, licensing, retention, and operational
review.

## 2026-09-21 — Reproducible Angular verification baseline

**Decision:** Raise the Angular 20 dependency floor to patched 20.3.28 releases,
remove unused ng-bootstrap and Angular Material imports, and lock the resolved
tree after compatible security updates. Use Puppeteer-managed Chrome for Karma
tests and set the production bundle warning budget to 600 kB while retaining the
1 MB error cap.

**Reason:** The imported project could not build because it referenced an
undeclared carousel module, its installed dependency tree was incomplete, and
the machine-independent test command had no browser runtime. The application
uses Bootstrap styling, so the measured 572.50 kB initial bundle is within a
documented prototype warning budget.

**Consequences:** `npm ci` installs the locked application and test
dependencies; `npm test -- --watch=false` resolves Puppeteer's managed browser
without a system Chrome installation. The project now has deterministic tests
for route configuration and team/player search. The MVP predictor remains an
explicitly unimplemented product surface.

## 2026-09-21 — Restore a local, approval-gated data pipeline

**Decision:** Recover the legacy Airflow-to-PostgreSQL architecture as a local
Docker Compose stack. It accepts only manually supplied, approved snapshots;
stores raw artifact copies and checksums in a Docker volume; records curated
rows and provenance in PostgreSQL; and produces an Angular-compatible candidate
that requires manual promotion.

**Reason:** The recovered legacy DAG established the intended ETL shape but was
not runnable: it lacked its imported functions, schema, dependencies, Compose
configuration, and website publication step. Its Basketball Reference
`cloudscraper` extractor is not authorized for activation. Sports Reference's
published data-use policy restricts automated access and using scraped data in
websites/tools without permission.

**Consequences:** The pipeline exposes no host port, accepts no credentials,
and has no scheduled web collection. An approved source adapter, retention
change, or automatic publication requires a new decision and bounded audit.
The legacy extractor remains historical evidence only.

## 2026-09-21 — Credential-free local pipeline operation

**Decision:** Remove the Airflow webserver, administrator bootstrap, and all
password variables from the local Compose configuration. Use PostgreSQL `trust`
authentication only within the private Docker network and operate the stack by
the Airflow scheduler CLI.

**Reason:** This prototype has no published host port or multi-user access
requirement. Keeping local database and administrator secrets added setup and
rotation work without a useful protection boundary.

**Consequences:** The stack has no browser dashboard or login. It must not be
published, attached to another network, or given a host port while trust
authentication is enabled. Existing initialized PostgreSQL volumes retain their
old internal credential records until deliberately removed.

## 2026-09-21 — Development-network Airflow dashboard

**Decision:** Restore the Airflow webserver as an unauthenticated dashboard on
development port `8765`, with anonymous access receiving the Airflow Admin
role.

**Reason:** The dashboard is useful for inspecting and manually triggering the
local-only pipeline, while the prototype deliberately has no credential store.

**Consequences:** The dashboard may be exposed on the local development network
only by explicit approval to support a browser/port-forwarding layer. The
configuration must be replaced with authenticated access before any public
exposure.
