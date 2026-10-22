# Optional template tests

These files are for maintaining the template. KiCad excludes `meta/` when
creating PCB projects, and Project Manager does not manage these tests or the
optional workflow.

From the template repository, with Docker installed:

```sh
python3 meta/tests/check_workflow.py --major 10 --workspace /tmp/kicad-template-test-10
# Use --major 9 and a different fresh workspace to check KiCad 9.
```

This runs all four documentation statuses on an example board, verifies that
a deliberate schematic error is caught, and checks the original hierarchical
starter (including the reviewer in its generated PDF). The first run downloads/builds the
toolchain; subsequent runs reuse it.

To run on GitHub, move `meta/tests/kicad-port-trial.yaml` into
`.github/workflows/` on `dev_k10` or a `port/` test branch, then commit and push. It checks
both KiCad versions and uploads the generated results. Move the YAML back here
when finished. Ordinary PCB projects need only `.github/workflows/ci.yaml`.
