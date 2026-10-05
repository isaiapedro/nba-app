# NBA Team Explorer system contract

## Purpose

Provide a client-side Angular interface for exploring NBA teams, rosters, and
players from repository-bundled datasets.

## Inputs

- Versioned JSON statistics used by the Angular application.
- Manually promoted, provenance-validated JSON candidates produced by the local
  Airflow/PostgreSQL pipeline when an approved data source is available.
- Historical CSV and HTML snapshots retained by the imported repository.
- User-entered team and player search text in the browser.

## Outputs

- Local browser views for team rosters, player lookup, and experimental MVP
  prediction.
- Build artifacts generated under `dist/`.
- Local immutable source artifacts, curated PostgreSQL rows, and review-only
  frontend candidates produced by the pipeline.

## Operational boundary

The current application has no registered backend, public API, credential
store, or runtime Personal-data dependency. Historical scraping material is
repository-owned source evidence, not authorization for unattended collection
or authenticated access. Any future listener or service integration requires
Registry and local-contract updates first.

The pipeline is local-only and has a credential-free Airflow dashboard on the
development-network port `8765`, explicitly approved for browser access. Its
two PostgreSQL instances use trusted authentication only inside Docker's
private network and are operated through the dashboard or scheduler CLI. It
does not collect from the web by default and never auto-publishes to the
Angular application. An automated source adapter requires documented
authorization, provenance, retention, and operational approval before its
schedule can be enabled.

## Non-responsibilities

- Production-grade NBA statistics distribution.
- Long-term availability or public API compatibility.
- Storage of user profiles, credentials, or Personal records.
