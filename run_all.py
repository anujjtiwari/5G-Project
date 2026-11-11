"""Run the whole project end to end: python run_all.py [--skip-build] [--skip-bench]"""
import subprocess, sys, time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
steps = [
    ("e01_build_twin.py", "Tasks 1-2: ray-trace the channel database"),
    ("e02_scenario_and_channels.py", "Tasks 1-2: scenario, coverage, measurements"),
    ("e03_compare_strategies.py", "Tasks 3, 4, 6: baseline vs twin-assisted allocation"),
    ("e05_mobility.py", "Task 5: mobility"),
    ("e06_twin_fidelity.py", "Task 6: twin fidelity vs allocation gain"),
    ("e07_whatif.py", "Task 7: what-if analysis"),
    ("e08_benchmark.py", "Task 8: computational requirements"),
]
if "--skip-build" in sys.argv:
    steps = steps[1:]
if "--skip-bench" in sys.argv:
    steps = steps[:-1]
for script, label in steps:
    print(f"\n=== {label} ({script}) ===", flush=True)
    t = time.time()
    subprocess.run([sys.executable, "-u", str(ROOT / "experiments" / script)], check=True)
    print(f"--- finished in {time.time() - t:.0f} s", flush=True)
