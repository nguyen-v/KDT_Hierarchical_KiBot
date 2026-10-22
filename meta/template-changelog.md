# Template change history

This tracks the template, not a PCB's release history (`CHANGELOG.md`).

## 1.0.0 — proposed KiCad 9/10 update

- Support KiCad 9 and 10 using one runner for local Docker and GitHub Actions.
- Pin KiCad/KiBot toolchains, dependencies and downloads; isolate runtime profiles.
- Adapt KiCad 10's renderer camera and use high-quality transparent images without floor shadows.
- Resolve embedded worksheets from a cold profile and preserve the reviewer text variable.
- Generate releases from the exact tag, transfer their assets directly, and reject concurrent branch changes rather than force-pushing.
- Add optional versioned template-update metadata and maintenance tests under `meta/`.
- Correct generated README logo/image references and document the revised local workflow.

First versioned template manifest; existing board release versions are independent.
Public project, license, fonts, logos, component-field defaults and KiRI history output are retained.
