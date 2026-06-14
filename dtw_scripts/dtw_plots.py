"""
DTW Plotting Script
---------------------
Loads precomputed DTW results from an .npz file (produced by
dtw_analysis.py) and generates the DTW-aligned overlay plot and the
raw baseline-subtracted overlay plot.

Requirements:
    pip install numpy matplotlib
"""

import numpy as np
import matplotlib.pyplot as plt

INPUT_NPZ = "dtw_plots/dtw_results.npz"  # path to the saved DTW results

DTW_PLOT_CUTOFF_MS = 100  # x-axis cutoff for the DTW-aligned overlay plot
RAW_PLOT_CUTOFF_MS = 110  # x-axis cutoff for the raw baseline-subtracted overlay plot

# ── Load precomputed results ──────────────────────────────────────────────────

data = np.load(INPUT_NPZ, allow_pickle=True)

aligned      = data["aligned"]
time_aligned = data["time_aligned"]
ref_signal   = data["ref_signal"]
mean_trace   = data["mean_trace"]
rolling_std  = data["rolling_std"]
raw_signals  = data["raw_signals"]
raw_times    = data["raw_times"]
ref_key      = str(data["ref_key"])

# ── Plot 1: DTW-aligned overlay ───────────────────────────────────────────────

fig, ax = plt.subplots(figsize=(12, 6))

for trace in aligned:
    ax.plot(time_aligned, trace, color="steelblue", alpha=0.15, linewidth=0.5)

ax.plot(time_aligned, mean_trace, color="darkred", linewidth=1.5, label="Mean aligned trace")
ax.plot(time_aligned, rolling_std, color="orange", linewidth=1.5, label="Rolling std of mean")
ax.plot(time_aligned, ref_signal, color="black", linewidth=1, linestyle="--", label="Reference")

ax.axvline(0, color="gray", linestyle=":", linewidth=0.8)
ax.set_xlim(time_aligned[0], DTW_PLOT_CUTOFF_MS)  # limit x-axis to the configured cutoff
ax.set_xlabel("Time (ms)")
ax.set_ylabel("Baseline-subtracted current (nA)")
ax.set_title("DTW-Aligned Event Overlays")
ax.legend(loc="lower right")
plt.tight_layout()
plt.savefig("dtw_plots/dtw_aligned_overlay.png", dpi=150)
plt.show()
print("Saved: dtw_plots/dtw_aligned_overlay.png")

# ── Plot 2: Raw baseline-subtracted overlay (no DTW alignment) ────────────────

fig2, ax2 = plt.subplots(figsize=(12, 6))

for sig, time_axis in zip(raw_signals, raw_times):
    ax2.plot(time_axis, sig, color="steelblue", alpha=0.15, linewidth=0.5)

ax2.set_xlim(0, RAW_PLOT_CUTOFF_MS)  # limit x-axis to the configured cutoff
ax2.set_xlabel("Time (ms)")
ax2.set_ylabel("Baseline-subtracted current (nA)")
ax2.set_title("Raw Event Overlays (baseline-subtracted, no alignment)")
plt.tight_layout()
plt.savefig("dtw_plots/raw_baseline_overlay.png", dpi=150)
plt.show()
print("Saved: dtw_plots/raw_baseline_overlay.png")