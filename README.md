# 5G RAN Digital Twin for Channel-Aware Resource Allocation and What-If Analysis

Course project, *5G and Beyond* (Semester I, 2026). A site-specific digital twin of a
3-site / 9-sector NR n78 network in a dense city block, built on **NVIDIA Sionna RT**
(the open-source ray tracer from NVIDIA's Aerial/Sionna stack). The twin is used to

1. obtain per-link, per-PRB channel information for every UE location,
2. drive a channel-aware cell association + PRB scheduler,
3. compare it against fixed / random baselines on 5G KPIs,
4. follow moving UEs through LOS/NLOS transitions, and
5. predict the effect of network changes (what-if) **before** applying them, with the
   prediction checked against a higher-fidelity "physical network" stand-in.

## Quick start

```bash
pip install -r requirements.txt          # sionna-rt, numpy, pandas, matplotlib, pyyaml
python run_all.py                        # runs every experiment, ~45-60 min on a 2-core CPU
python run_all.py --skip-build           # reuse the ray-traced channel database in data/
```

A GPU is used automatically when present (Mitsuba `cuda_ad_*` variant). Everything also runs on CPU (LLVM backend) or Google Colab.

## Running on another site (e.g. IIT Gandhinagar) or on a GPU server

```bash
python tools/build_scene.py --name iitgn --lat 23.2114 --lon 72.6821 --size 1400   # OSM -> scene + config
DT_CONFIG=config/iitgn.yaml python run_all.py                                     # results/iitgn/
```

See `KRATU.md` for running headless over SSH on an L40S server, including the AODT route.

## Repository layout

| Path | What it is |
|---|---|
| `config/scenario.yaml` | **All** scenario parameters: carrier, sites, power, antennas, ray-tracing fidelity, impairments, experiment sizes |
| `dt/twin.py` | The digital twin: scene, RUs, outdoor UE sampling, LOS test, ray tracing -> `ChannelSet` |
| `dt/channel.py` | Channel database (`ChannelSet`), 3GPP TR 38.901 helpers, statistical model, physical-network impairments |
| `dt/kpi.py` | KPI engine: effective SINR, CQI (TS 38.214 Table 5.2.2.1-3), throughput, fairness |
| `dt/alloc.py` | Association + scheduling strategies (B1, B2, T1, T2, T3) and the slot-level DL simulator |
| `experiments/e01_build_twin.py` | Tasks 1-2: ray-trace the channel database (twin, twin at noisy positions, physical) |
| `experiments/e02_scenario_and_channels.py` | Tasks 1-2: scenario/coverage figures, channel table, RAN measurements |
| `experiments/e03_compare_strategies.py` | Tasks 3, 4, 6: Monte Carlo comparison of all strategies |
| `experiments/e05_mobility.py` | Task 5: moving UEs, re-association events |
| `experiments/e06_twin_fidelity.py` | Task 6: how twin accuracy (positions, materials, sync) changes the gain |
| `experiments/e07_whatif.py` | Task 7: what-if prediction vs "actual" |
| `experiments/e08_benchmark.py` | Task 8: runtime / memory scaling of the twin |
| `results/figures/` | All figures (`fig01` ... `fig16`) |
| `results/tables/` | All result tables (`t1` ... `t8`) |
| `REPORT.md` | Full project report |
| `dt/scene_builder.py`, `tools/build_scene.py` | Build a scene of any real site from OpenStreetMap, place rooftop gNBs, write its config |
| `tools/check_env.sh`, `tools/kratu_job.sbatch`, `KRATU.md` | GPU-server check, SLURM job, step-by-step server guide |

## Strategies compared

| ID | Association | PRB allocation | Uses twin? |
|---|---|---|---|
| B1 | Nearest site, sector by bearing | Fixed equal contiguous blocks | No |
| B2 | Nearest site, sector by bearing | Random every slot | No |
| T1 | Max RSRP from twin | Fixed equal blocks | Association only |
| T2 | Twin load-aware (max sum-log predicted rate) | Frequency-selective proportional fair | Yes |
| T3 | Twin load-aware | PF + twin-predicted inter-cell PRB muting | Yes |

## Swapping in NVIDIA AODT

Everything downstream of `DigitalTwin.trace()` only needs a `ChannelSet`:
UE positions `[U,3]`, per-PRB channel power `H2[U,R,K]`, LOS flags `[U,R]` and RU geometry.
To run the same study on AODT, export the CFRs from AODT's results database for each
RU-UE link, sample them at the PRB centre frequencies, and build a `ChannelSet` from them.

## Understand 5G: core network explorer

`tools/understand_5g/` is an interactive teaching tool for the whole 5G system behind the RAN that the twin models.
It is plain HTML/JavaScript with no install. Open `tools/understand_5g/index.html` in a browser, or click
**Understand 5G →** in the 3D twin viewer (`results/<scenario>/twin_3d.html`).

- **Network map**: a 5G standalone network (UE, two gNBs, AMF, SMF, UPF, AUSF, UDM, UDR, PCF, NRF, NSSF, NEF, AF, DN).
  Click any network function for its role, capabilities and SBI services. Click any interface (Uu, N1–N6, Xn, N33, SBI)
  for its protocol stack and 3GPP specs. Messages animate across the map with subtitles and optional voice narration.
- **Call flow & decodes**: 93 messages in 9 chapters (network start-up, cell search and RACH, registration with
  5G-AKA, PDU session, user data and scheduling, QoS via NEF, Xn handover, idle and paging, deregistration).
  Each message is decoded field by field, with a live UE/session state panel.
- **SBI API builder**: real HTTP/2 request and response examples for NRF, AUSF, UDM, SMF, PCF, AMF and NSSF operations.
- **Air interface**: SINR → CQI → MCS → throughput using the same CQI table and gaps as `dt/kpi.py`.

`python tools/install_5g_explorer.py` copies the explorer next to every existing `twin_3d.html` and adds the
button; `tools/export_3d.py` does this automatically. Deep links: `index.html?step=25&tab=flow`.
Message contents follow 3GPP Rel-16/17; identities use the test PLMN 001/01 and are illustrative.
