# Project briefing for Claude Code

Course project for *5G and Beyond* (IIT Gandhinagar, Semester I 2026): a 5G RAN digital twin
for channel-aware resource allocation and what-if analysis. The full brief has 8 tasks
(scenario, channels, baseline, channel-aware allocation, mobility, KPI comparison,
what-if, platform evaluation). All 8 are already implemented and run for the Munich scene;
see README.md, REPORT.md and results/.

The student is new to the terminal and to Claude Code. Explain each step in one plain
sentence before running it, and ask before anything that deletes files or takes > 10 minutes.

## Layout
- `config/scenario.yaml` — all parameters (Munich). `DT_CONFIG=config/<name>.yaml` selects another scenario.
- `dt/` — twin (Sionna RT), channel database, KPI engine, allocation strategies, scene builder.
- `experiments/e01…e08` — one script per task group; `run_all.py` runs them in order.
- `tools/build_scene.py` — builds a scene of a real site from OpenStreetMap and writes `config/<name>.yaml`.
- `KRATU.md`, `tools/check_env.sh`, `tools/kratu_job.sbatch` — running on the Kratu L40S GPU server over SSH.

## Setup on the student's Mac
1. `python3 --version` must be 3.10+. If not, install Python 3.12 from python.org (or `brew install python@3.12`).
2. `python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`
3. Check the ray tracer: `python -c "import mitsuba as mi; mi.set_variant('llvm_ad_mono_polarized'); print('ok')"`.
   If it fails mentioning LLVM: `brew install llvm`, then retry (if still failing, set
   `DRJIT_LIBLLVM_PATH` to the libLLVM.dylib under `$(brew --prefix llvm)/lib`).
4. Reproduce Munich results quickly: `python run_all.py --skip-build --skip-bench` (reuses data/).

## Next goal: IIT Gandhinagar campus twin
1. `python tools/build_scene.py --name iitgn --lat 23.2114 --lon 72.6821 --size 1400`
   (downloads OSM buildings; centre is Wikipedia's campus coordinate — check that the box covers the campus).
2. Review `scenes/iitgn/scene_meta.json`: building count, % with height tags, suggested sites.
   Untagged buildings default to 12 m. Show the student a top-down plot of footprints + sites before continuing.
3. Full study: `DT_CONFIG=config/iitgn.yaml python run_all.py --skip-bench` → results/iitgn/.
   On a Mac CPU this can take 1–2 hours (ray tracing dominates); prefer Kratu once access is available.
4. Compare IITGN vs Munich results and add an IITGN section to REPORT.md.

## Conventions
- Never overwrite Munich results in data/ and results/ (other scenarios use output_tag subfolders).
- Ray traces are cached in data/<tag>/_raw_*.npz; delete them only to force a re-trace.
- Report limitations honestly: OSM has no trees/terrain; the "physical network" is a higher-fidelity simulation.
