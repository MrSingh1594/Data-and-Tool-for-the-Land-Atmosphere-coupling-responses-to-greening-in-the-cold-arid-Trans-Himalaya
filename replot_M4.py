import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ============================================================
# Replot Figure 8 (M4) from cached intermediate data
# No raw WRF wrfout files are required.
# ============================================================

BASE_DIR = r"C:\Users\lrc-n\OneDrive\Desktop\WRF\JGR_Submission"

DAT_DIR = os.path.join(
    BASE_DIR,
    "data",
    "intermediates"
)

FIG_DIR = os.path.join(
    BASE_DIR,
    "figures"
)

M4_FILE = os.path.join(
    DAT_DIR,
    "M4_precip_per_cell.npz"
)

CDF_FILE = os.path.join(
    DAT_DIR,
    "M4_wet_day_cdf.npz"
)

SUMMARY_FILE = os.path.join(
    DAT_DIR,
    "M4_pooled_summary.csv"
)

os.makedirs(FIG_DIR, exist_ok=True)

# ============================================================
# Settings copied from the original plotting workflow
# ============================================================

WET_DAY_MM = 1.0

EXP_COLORS = {
    "Control": "#808080",
    "Exp1": "#3182bd",
    "Exp2": "#e6550d",
    "Exp3": "#31a354",
    "Exp4": "#756bb1",
}

EXP_LABELS = [
    "Control",
    "Exp1",
    "Exp2",
    "Exp3",
    "Exp4",
]

# ============================================================
# Load cached data
# ============================================================

m4_data = np.load(M4_FILE)
cdf_data = np.load(CDF_FILE)
df_summary = pd.read_csv(SUMMARY_FILE)

# These are loaded to verify that the cached metric arrays exist.
iy_arr = m4_data["iy_arr"]
ix_arr = m4_data["ix_arr"]

wet_pools = {
    e: cdf_data[f"wet_pool_{e}"]
    for e in EXP_LABELS
}

print("=" * 60)
print("M4 — Precipitation Dynamics  [REPLOT FROM CACHE]")
print("=" * 60)

print("\n[0] Loading cached data ...")
print(f"  M4 metric file : {M4_FILE}")
print(f"  CDF file       : {CDF_FILE}")
print(f"  Summary file   : {SUMMARY_FILE}")
print(f"  Grid cells     : {len(iy_arr)}")
print(f"  Wet-day threshold: {WET_DAY_MM} mm d^-1")

print("\n  Cached variables:")
for key in m4_data.files:
    print(
        f"    {key:20s} "
        f"{m4_data[key].shape} "
        f"{m4_data[key].dtype}"
    )

print("\n  Cached CDF variables:")
for key in cdf_data.files:
    print(
        f"    {key:20s} "
        f"{cdf_data[key].shape} "
        f"{cdf_data[key].dtype}"
    )

# ============================================================
# Figure 8 — exact 1 × 3 plotting structure
# ============================================================

print("\n[1] Plotting Fig 8 ...")

fig, axes = plt.subplots(
    1,
    3,
    figsize=(16, 5)
)

ax_ri, ax_p95, ax_cdf = axes

x = np.arange(
    len(EXP_LABELS)
)

colors = [
    EXP_COLORS[e]
    for e in EXP_LABELS
]

# ------------------------------------------------------------
# (a) RI_wet bars
# ------------------------------------------------------------

ri_means = [
    df_summary.loc[
        df_summary["exp"] == e,
        "RI_wet_mean"
    ].values[0]
    for e in EXP_LABELS
]

ri_stds = [
    df_summary.loc[
        df_summary["exp"] == e,
        "RI_wet_std"
    ].values[0]
    for e in EXP_LABELS
]

ax_ri.bar(
    x,
    ri_means,
    0.6,
    yerr=ri_stds,
    capsize=3,
    color=colors,
    edgecolor="black",
    linewidth=0.5
)

for xi, v in zip(x, ri_means):
    ax_ri.text(
        xi,
        v + 0.02,
        f"{v:.2f}",
        ha="center",
        va="bottom",
        fontsize=9
    )

ax_ri.axhline(
    ri_means[0],
    color="k",
    linewidth=0.8,
    linestyle="--",
    alpha=0.6
)

ax_ri.set_xticks(x)

ax_ri.set_xticklabels(
    EXP_LABELS,
    fontsize=10
)

ax_ri.set_ylabel(
    r"RI$_{\rm wet}$ [mm d$^{-1}$]",
    fontsize=11
)

ax_ri.set_title(
    r"(a) Wet-day mean intensity RI$_{\rm wet}$",
    fontsize=11,
    fontweight="bold"
)

ax_ri.grid(
    axis="y",
    alpha=0.3
)

# ------------------------------------------------------------
# (b) Precip95 bars
# ------------------------------------------------------------

p95_means = [
    df_summary.loc[
        df_summary["exp"] == e,
        "Precip95_mean"
    ].values[0]
    for e in EXP_LABELS
]

p95_stds = [
    df_summary.loc[
        df_summary["exp"] == e,
        "Precip95_std"
    ].values[0]
    for e in EXP_LABELS
]

ax_p95.bar(
    x,
    p95_means,
    0.6,
    yerr=p95_stds,
    capsize=3,
    color=colors,
    edgecolor="black",
    linewidth=0.5
)

for xi, v in zip(x, p95_means):
    ax_p95.text(
        xi,
        v + 0.05,
        f"{v:.2f}",
        ha="center",
        va="bottom",
        fontsize=9
    )

ax_p95.axhline(
    p95_means[0],
    color="k",
    linewidth=0.8,
    linestyle="--",
    alpha=0.6
)

ax_p95.set_xticks(x)

ax_p95.set_xticklabels(
    EXP_LABELS,
    fontsize=10
)

ax_p95.set_ylabel(
    r"Precip95 [mm d$^{-1}$]",
    fontsize=11
)

ax_p95.set_title(
    "(b) 95th-percentile wet-day precipitation Precip95",
    fontsize=11,
    fontweight="bold"
)

ax_p95.grid(
    axis="y",
    alpha=0.3
)

# ------------------------------------------------------------
# (c) Wet-day CDFs
# ------------------------------------------------------------

for e in EXP_LABELS:

    w = np.sort(
        wet_pools[e]
    )

    cdf = (
        np.arange(1, len(w) + 1)
        / len(w)
    )

    ax_cdf.plot(
        w,
        cdf,
        color=EXP_COLORS[e],
        lw=1.6,
        label=e
    )

ax_cdf.set_xscale("log")

ax_cdf.set_xlabel(
    r"Wet-day precipitation [mm d$^{-1}$]",
    fontsize=11
)

ax_cdf.set_ylabel(
    "CDF",
    fontsize=11
)

ax_cdf.set_title(
    "(c) Pooled wet-day precipitation CDF",
    fontsize=11,
    fontweight="bold"
)

ax_cdf.grid(
    True,
    alpha=0.3,
    which="both"
)

ax_cdf.legend(
    fontsize=9,
    loc="lower right"
)

ax_cdf.set_xlim(
    WET_DAY_MM,
    None
)

fig.tight_layout()

# ============================================================
# Save
# ============================================================

out_png = os.path.join(
    FIG_DIR,
    "fig_M4_precip_dynamics_replot.png"
)

plt.savefig(
    out_png,
    dpi=150,
    bbox_inches="tight"
)

plt.close(fig)

print("\nSaved:")
print(out_png)

print("\n[2] Summary")
print(
    f"  {'Exp':8s}"
    f"  {'RI_wet (mm/d)':>18s}"
    f"  {'Precip95 (mm/d)':>18s}"
)

for e in EXP_LABELS:

    row = df_summary.loc[
        df_summary["exp"] == e
    ].iloc[0]

    print(
        f"  {e:8s}"
        f"  {row['RI_wet_mean']:8.3f} ± {row['RI_wet_std']:5.3f}"
        f"  {row['Precip95_mean']:8.3f} ± {row['Precip95_std']:5.3f}"
    )

print("\nDone.")
