import os
import numpy as np
import netCDF4 as nc
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ============================================================
# Replot Figure 3 from cached direct-response NetCDF
# No raw WRF wrfout files are required.
# ============================================================

BASE_DIR = r"C:\Users\lrc-n\OneDrive\Desktop\WRF\JGR_Submission"

NC_FILE = os.path.join(
    BASE_DIR,
    "data",
    "intermediates",
    "direct_response_mean.nc"
)

FIG_DIR = os.path.join(
    BASE_DIR,
    "figures"
)

os.makedirs(FIG_DIR, exist_ok=True)

# The original Figure 3 contains the four experiments
# and compares each against Control.
EXPS = ["Exp1", "Exp2", "Exp3", "Exp4"]

# Same experiment colours used elsewhere in the analysis package.
EXP_COLORS = {
    "Exp1": "#3182bd",
    "Exp2": "#e6550d",
    "Exp3": "#31a354",
    "Exp4": "#756bb1"
}

# ============================================================
# Load cached direct-response data
# ============================================================

print("=" * 60)
print("Figure 3 — Direct Response  [REPLOT FROM CACHE]")
print("=" * 60)

print("\n[0] Loading cached NetCDF ...")
print(NC_FILE)

with nc.Dataset(NC_FILE) as ds:

    iy_arr = ds.variables["iy_arr"][:]
    ix_arr = ds.variables["ix_arr"][:]
    years = ds.variables["year"][:].astype(int)

    exp_raw = ds.variables["experiment"][:]

    # Decode experiment names robustly
    exp_names = []
    for x in exp_raw:
        if isinstance(x, bytes):
            exp_names.append(x.decode().strip())
        else:
            exp_names.append(str(x).strip())

    # Store cached variables as NumPy arrays.
    VARS = [
        "Albedo",
        "R_net",
        "LE",
        "H",
        "EF",
        "T2_day",
        "T2_night",
        "LST_day",
        "SM",
        "precip_daily",
        "wet_day_freq"
    ]

    d = {
        v: ds.variables[f"d_{v}"][:].astype(float)
        for v in VARS
    }

print(f"  Experiments in cache: {exp_names}")
print(f"  Years: {years.tolist()}")
print(f"  Cells: {len(iy_arr)}")
print(f"  Grid indices: {int(iy_arr.max()) + 1}×{int(ix_arr.max()) + 1}")

# ============================================================
# Verify expected experiment order
# ============================================================

if exp_names != EXPS:
    print("\nWarning: experiment order in cache differs from expected order.")
    print("Using the experiment order stored in the NetCDF.")
    EXPS = exp_names

# ============================================================
# Reproduce original aggregation exactly
#
# Original logic:
# yearly_means = nanmean(anom[v][e], axis=1)
# stats[v][e] = (mean(yearly_means), std(yearly_means, ddof=1))
# ============================================================

stats = {}

for v in VARS:

    stats[v] = {}

    for ei, e in enumerate(EXPS):

        yearly_means = np.nanmean(
            d[v][ei, :, :],
            axis=1
        )

        stats[v][e] = (
            float(np.mean(yearly_means)),
            float(np.std(yearly_means, ddof=1))
        )

# ============================================================
# Print the values used in the four panels
# ============================================================

print("\n[1] Mask-mean anomalies (mean ± inter-annual σ):")

for v in VARS:

    print(f"\n  {v}")

    for e in EXPS:

        mean, std = stats[v][e]

        if v == "wet_day_freq":
            mean_print = mean * 100
            std_print = std * 100
        else:
            mean_print = mean
            std_print = std

        print(
            f"    {e:8s}: "
            f"{mean_print:+.6f} ± {std_print:.6f}"
        )

# ============================================================
# Plot — same original 2×2 structure
# ============================================================

print("\n[2] Plotting Figure 3 ...")

fig, axes = plt.subplots(
    2,
    2,
    figsize=(12, 8)
)

ax_a, ax_b = axes[0]
ax_c, ax_d = axes[1]

width = 0.2

offsets = np.linspace(
    -1.5 * width,
    1.5 * width,
    4
)

def bar_group(
    ax,
    x_pos,
    e_idx,
    mean,
    std,
    hatch=None
):
    ax.bar(
        x_pos + offsets[e_idx],
        mean,
        width,
        yerr=std,
        capsize=2,
        color=EXP_COLORS[EXPS[e_idx]],
        edgecolor="black",
        linewidth=0.4,
        hatch=hatch
    )

# ------------------------------------------------------------
# (a) Radiative pathway: ΔR_net
# ------------------------------------------------------------

for i, e in enumerate(EXPS):

    mean, std = stats["R_net"][e]

    bar_group(
        ax_a,
        0,
        i,
        mean,
        std
    )

ax_a.axhline(
    0,
    color="k",
    linewidth=0.6
)

ax_a.set_xticks([0])

ax_a.set_xticklabels(
    [r"$\Delta R_{net}$"]
)

ax_a.set_ylabel(
    r"$\Delta R_{net}$ [W m$^{-2}$]"
)

ax_a.set_title(
    "(a) Radiative pathway"
)

ax_a.set_xlim(
    -0.5,
    0.5
)

ax_a.grid(
    axis="y",
    alpha=0.3
)

# ------------------------------------------------------------
# (b) Turbulent: ΔLE, ΔH, ΔEF
# ------------------------------------------------------------

ax_b2 = ax_b.twinx()

for i, e in enumerate(EXPS):

    le_mean, le_std = stats["LE"][e]
    h_mean, h_std = stats["H"][e]
    ef_mean, ef_std = stats["EF"][e]

    bar_group(
        ax_b,
        0,
        i,
        le_mean,
        le_std
    )

    bar_group(
        ax_b,
        1,
        i,
        h_mean,
        h_std
    )

    bar_group(
        ax_b2,
        2,
        i,
        ef_mean,
        ef_std,
        hatch="//"
    )

ax_b.axhline(
    0,
    color="k",
    linewidth=0.6
)

ax_b.set_xticks(
    [0, 1, 2]
)

ax_b.set_xticklabels(
    [
        r"$\Delta LE$",
        r"$\Delta H$",
        r"$\Delta EF$"
    ]
)

ax_b.set_ylabel(
    r"$\Delta LE, \Delta H$ [W m$^{-2}$]"
)

ax_b2.set_ylabel(
    r"$\Delta EF$ (–)"
)

ax_b.set_title(
    "(b) Turbulent partitioning"
)

ax_b.grid(
    axis="y",
    alpha=0.3
)

# ------------------------------------------------------------
# (c) Near-surface: ΔT2 day/night, ΔLST_day, ΔSM
# ------------------------------------------------------------

ax_c2 = ax_c.twinx()

for i, e in enumerate(EXPS):

    t2d_mean, t2d_std = stats["T2_day"][e]
    t2n_mean, t2n_std = stats["T2_night"][e]
    lst_mean, lst_std = stats["LST_day"][e]
    sm_mean, sm_std = stats["SM"][e]

    bar_group(
        ax_c,
        0,
        i,
        t2d_mean,
        t2d_std
    )

    bar_group(
        ax_c,
        1,
        i,
        t2n_mean,
        t2n_std
    )

    bar_group(
        ax_c,
        2,
        i,
        lst_mean,
        lst_std
    )

    bar_group(
        ax_c2,
        3,
        i,
        sm_mean,
        sm_std,
        hatch="//"
    )

ax_c.axhline(
    0,
    color="k",
    linewidth=0.6
)

ax_c.set_xticks(
    [0, 1, 2, 3]
)

ax_c.set_xticklabels(
    [
        r"$\Delta T2_{day}$",
        r"$\Delta T2_{night}$",
        r"$\Delta LST_{day}$",
        r"$\Delta SM$"
    ]
)

ax_c.set_ylabel(
    r"$\Delta T2, \Delta LST$ [°C]"
)

ax_c2.set_ylabel(
    r"$\Delta SM$ [m$^3$ m$^{-3}$]"
)

ax_c.set_title(
    "(c) Near-surface state"
)

ax_c.grid(
    axis="y",
    alpha=0.3
)

# ------------------------------------------------------------
# (d) Precipitation: ΔPrecip, ΔWet-day frequency
# ------------------------------------------------------------

ax_d2 = ax_d.twinx()

for i, e in enumerate(EXPS):

    p_mean, p_std = stats["precip_daily"][e]

    wet_mean, wet_std = stats["wet_day_freq"][e]

    bar_group(
        ax_d,
        0,
        i,
        p_mean,
        p_std
    )

    bar_group(
        ax_d2,
        1,
        i,
        wet_mean * 100,
        wet_std * 100,
        hatch="//"
    )

ax_d.axhline(
    0,
    color="k",
    linewidth=0.6
)

ax_d.set_xticks(
    [0, 1]
)

ax_d.set_xticklabels(
    [
        r"$\Delta$Precip",
        r"$\Delta$Wet-day freq"
    ]
)

ax_d.set_ylabel(
    r"$\Delta$Precip [mm day$^{-1}$]"
)

ax_d2.set_ylabel(
    r"$\Delta$Wet-day freq [%]"
)

ax_d.set_title(
    "(d) Precipitation response"
)

ax_d.grid(
    axis="y",
    alpha=0.3
)

# ------------------------------------------------------------
# Shared legend — same original convention
# ------------------------------------------------------------

handles = [
    plt.Rectangle(
        (0, 0),
        1,
        1,
        color=EXP_COLORS[e],
        edgecolor="black",
        linewidth=0.4,
        label=e
    )
    for e in EXPS
]

fig.legend(
    handles=handles,
    loc="lower center",
    ncol=4,
    bbox_to_anchor=(0.5, -0.02),
    frameon=False,
    fontsize=10
)

fig.tight_layout(
    rect=[0, 0.03, 1, 1]
)

# ============================================================
# Save
# ============================================================

out_png = os.path.join(
    FIG_DIR,
    "fig3_direct_response_replot.png"
)

plt.savefig(
    out_png,
    dpi=150,
    bbox_inches="tight"
)

plt.close(fig)

print("\nSaved:")
print(out_png)

print("\nDone.")
