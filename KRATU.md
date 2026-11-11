# Running the project on Kratu (NVIDIA L40S, SSH only)

You don't need a desktop or GUI on the server. The ray tracer and all experiments run
headless. Every result is a PNG, CSV or JSON file that you copy back or view in your
laptop's browser through an SSH tunnel.

```
laptop  --ssh / scp / port-forward-->  Kratu (L40S)
  view figures, edit report               Sionna RT on the GPU, allocation + what-if experiments
```

## 0. Check the server (read-only, 1 minute)

```bash
ssh <you>@<kratu-address>
git clone <your-copy-of-this-project> 5g-dt-project   # or: scp -r 5g-dt-project <you>@<kratu>:~
cd 5g-dt-project
bash tools/check_env.sh 2>&1 | tee env_report.txt
```

Look for four things in `env_report.txt`:

1. The L40S GPUs and how much of their memory other users are already using.
2. The Python version (3.10 or newer).
3. Whether `pypi.org` and `overpass-api.de` are reachable.
4. Whether a job scheduler (`sbatch`) exists.

## 1. Route A: Sionna RT (recommended, no admin rights needed)

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python -c "import mitsuba as mi; mi.set_variant('cuda_ad_mono_polarized'); print('GPU backend OK')"
```

If the last line fails, the code still runs on CPU, just slower. That usually points to the
NVIDIA driver; send the error to the cluster admin.

**Choose a free GPU.** Run `nvidia-smi` and pick a GPU with little memory in use, then
`export CUDA_VISIBLE_DEVICES=1` (for example).

**Run the Munich study on the GPU** (this redoes everything, including the ray tracing):

```bash
tmux new -s dt                      # the run keeps going if your SSH connection drops
source .venv/bin/activate
python -u run_all.py 2>&1 | tee logs_munich.txt
# detach: Ctrl-b then d      reattach later: tmux attach -t dt
```

If Kratu uses SLURM, submit the job instead: `sbatch tools/kratu_job.sbatch`.

## 2. Build the IIT Gandhinagar campus twin

```bash
python tools/build_scene.py --name iitgn --lat 23.2114 --lon 72.6821 --size 1400
```

This command:
- downloads every building footprint in a 1.4 km × 1.4 km box around the campus from OpenStreetMap;
- extrudes each building to its OSM height (from `height` or `building:levels`, otherwise 12 m);
- adds a ground plane;
- writes the ray-tracing scene to `scenes/iitgn/`;
- places 3 rooftop gNB sites automatically on tall buildings spread across the campus;
- writes `config/iitgn.yaml`.

Check the centre point before relying on it. 23.2114 N, 72.6821 E is Wikipedia's campus
coordinate. Move it (and `--size`) so the box covers the part of campus you want.

**If Kratu cannot reach the internet**, export the buildings on your laptop instead:

1. Open <https://overpass-turbo.eu>, zoom to the campus and run this query:
   ```
   [out:json][timeout:60];
   (way["building"]({{bbox}}); relation["building"]["type"="multipolygon"]({{bbox}}););
   out geom;
   ```
2. Choose **Export → GeoJSON** and copy the file to Kratu.
3. Run `python tools/build_scene.py --name iitgn --lat 23.2114 --lon 72.6821 --size 1400 --geojson iitgn.geojson`.

**Run the full study on the campus:**

```bash
DT_CONFIG=config/iitgn.yaml python -u run_all.py 2>&1 | tee logs_iitgn.txt
```

Results go to `results/iitgn/` and `data/iitgn/`. The Munich results are not touched.

**Before you trust the campus results**, check three things:
- **Building heights.** `scenes/iitgn/scene_meta.json` reports how many buildings had OSM
  height tags. Untagged buildings are 12 m prisms. Correct important ones (hostels, academic
  blocks) by adding `height` in the GeoJSON, or by changing `--default-height`.
- **Site positions.** The auto-placed sites are a starting point. If you know where real masts
  are (or where IT would put them), edit `ran.sites` in `config/iitgn.yaml`. Coordinates are
  metres east (`x`) and north (`y`) of the centre point; `height_m` is the antenna height.
- **What the model leaves out.** OSM has no trees or terrain. IITGN has a lot of vegetation,
  so state this as a limitation, or add the 4 dB shadowing term to the twin as well.

## 3. Look at the results from your laptop

Copy them over:

```bash
scp -r <you>@<kratu>:~/5g-dt-project/results/iitgn ./results_iitgn
```

Or browse them live without copying:

```bash
# on Kratu
cd ~/5g-dt-project/results && python3 -m http.server 8765
# on your laptop, in a second terminal
ssh -N -L 8765:localhost:8765 <you>@<kratu>
# then open http://localhost:8765 in the laptop browser
```

## 4. Route B: NVIDIA AODT 1.5.1 on Kratu (needs the admin)

NVIDIA's AODT 1.5.1 prerequisites list the L40S as supported. The worker host also needs
the following, most of which only an administrator can set up on a shared server:

| Requirement | Why it usually needs the admin |
|---|---|
| Ubuntu 22.04 | OS version is fixed by the server |
| NVIDIA driver 575 series | Driver install or upgrade needs root |
| Docker with Compose v2 (2.3+) and the NVIDIA Container Toolkit | Package install needs root |
| Your user in the `docker` group | Equivalent to root access, so many clusters refuse it |
| NGC API key (log in to `nvcr.io`) | Personal; you create it on NVIDIA NGC |

The worker stack runs several services in containers, including MinIO and ClickHouse. A
Python client drives the simulations, and a browser viewer can be reached through an SSH
tunnel, so AODT 1.5 does not need a desktop on Kratu either. Older AODT versions (1.4 and
earlier) needed a separate GUI frontend over VNC or Remote Desktop.

To plug AODT channels into this project, export the per-link CFRs from AODT's results and
build a `ChannelSet` (see `dt/channel.py`). Every experiment after Task 2 then runs unchanged.

If the admin says no to Docker, ask whether Apptainer/Singularity is allowed. Otherwise
stay on Route A; Sionna RT on the L40S covers every task in the brief.
