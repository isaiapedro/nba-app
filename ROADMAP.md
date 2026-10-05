# Roadmap

## Vision

Offer a compact, understandable NBA exploration interface that demonstrates
Angular navigation, search, and data-driven UI design.

## Milestones

### Prototype

- Keep team and player browsing buildable from the imported source.
- Establish repository, governance, and data-source boundaries.

### MVP

- Add deterministic component and data-contract tests.
- Complete or remove the empty MVP predictor surface.
- Resolve accessibility and responsive-layout gaps.
- Obtain an authorized NBA data source before enabling scheduled collection.

### Validation

- Validate team and player search tasks with representative users.
- Review the provenance and refresh process for bundled statistics.
- Exercise an approved snapshot through the local Airflow/PostgreSQL pipeline
  and review the generated frontend candidate.

### Production candidate

- Define deployment ownership, update cadence, observability, and rollback.
- Allocate any fixed service ports and external integrations through Registry.

## Success criteria

The project builds reproducibly, core browsing tasks are tested and usable,
data provenance is documented, and promotion or archival is an explicit
decision.
