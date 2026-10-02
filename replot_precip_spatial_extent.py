import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from scipy.signal import convolve2d

# ============================================================
# Replot Figure 9 from cached intermediate data
# No raw WRF wrfout files are required.
# ============================================================

BASE_DIR = r"C:\Users\lrc-n\OneDrive\Desktop\WRF\JGR_Submission"

NPZ_FILE = os.path.join(
    BASE_DIR,
    "data",
    "intermediates",
    "precip_spatial_extent.npz"
)

FIG_DIR = os.path.join(
    BASE_DIR,
    "figures"
)

os.makedirs(FIG_DIR, exist_ok=True)

EXPS = ["Exp1", "Exp2", "Exp3", "Exp4"]

KERNEL_SMTH9 = np.array(
    [[1, 2, 1],
     [2, 4, 2],
     [1, 2, 1]],
    dtype=float
) / 16.0


def smth9(data):
    return convolve2d(
        data,
        KERNEL_SMTH9,
        mode="same",
        boundary="symm"
    )


print("=" * 60)
print("Precipitation spatial-extent diagnostic  [REPLOT FROM CACHE]")
print("=" * 60)

# ------------------------------------------------------------
# Load cached data
# ------------------------------------------------------------
data = np.load(NPZ_FILE)

print("\n[0] Loading cached data ...")
print(f"  File: {NPZ_FILE}")

mask = data["mask"].astype(bool)

mean_precip = {
    "Control": data["mean_precip_Control"],
    "Exp1": data["mean_precip_Exp1"],
    "Exp2": data["mean_precip_Exp2"],
    "Exp3": data["mean_precip_Exp3"],
    "Exp4": data["mean_precip_Exp4"],
}

wet_freq = {
    "Control": data["wet_freq_Control"],
    "Exp1": data["wet_freq_Exp1"],
    "Exp2": data["wet_freq_Exp2"],
    "Exp3": data["wet_freq_Exp3"],
    "Exp4": data["wet_freq_Exp4"],
}

print(f"  Mask shape: {mask.shape}")
print(f"  Mask cells: {mask.sum()}")

# ------------------------------------------------------------
# Compute Exp - Control
# ------------------------------------------------------------
print("\n[1] Computing Δ maps ...")

d_precip = {
    e: mean_precip[e] - mean_precip["Control"]
    for e in EXPS
}

d_wet = {
    e: wet_freq[e] - wet_freq["Control"]
    for e in EXPS
}

# ------------------------------------------------------------
# Inside/outside mask summary
# ------------------------------------------------------------
inv_mask = ~mask

print("\nSpatial signal summary:")
print(
    f"{'Exp':6s}"
    f"{'Δprecip in':>15s}"
    f"{'Δwet in':>15s}"
    f"{'Δprecip out':>16s}"
    f"{'Δwet out':>15s}"
)

for e in EXPS:
    d_p_in = np.nanmean(d_precip[e][mask])
    d_w_in = np.nanmean(d_wet[e][mask])
    d_p_out = np.nanmean(d_precip[e][inv_mask])
    d_w_out = np.nanmean(d_wet[e][inv_mask])

    print(
        f"{e:6s}"
        f"{d_p_in:+15.4f}"
        f"{d_w_in:+15.3f}"
        f"{d_p_out:+16.4f}"
        f"{d_w_out:+15.3f}"
    )

# ------------------------------------------------------------
# Smooth maps — same original method
# ------------------------------------------------------------
print("\n[2] Applying smth9 smoothing ...")

d_precip_s = {
    e: smth9(d_precip[e])
    for e in EXPS
}

d_wet_s = {
    e: smth9(d_wet[e])
    for e in EXPS
}

# ------------------------------------------------------------
# Symmetric colour limits — same original method
# ------------------------------------------------------------
p_max = float(max(
    np.nanpercentile(np.abs(d_precip_s[e]), 98)
    for e in EXPS
))

w_max = float(max(
    np.nanpercentile(np.abs(d_wet_s[e]), 98)
    for e in EXPS
))

norm_p = mcolors.TwoSlopeNorm(
    vmin=-p_max,
    vcenter=0,
    vmax=p_max
)

norm_w = mcolors.TwoSlopeNorm(
    vmin=-w_max,
    vcenter=0,
    vmax=w_max
)

cmap = plt.cm.RdBu

print(f"  Precipitation ± limit: {p_max:.6f}")
print(f"  Wet-day frequency ± limit: {w_max:.6f}")

# ------------------------------------------------------------
# Figure 9
# ------------------------------------------------------------
print("\n[3] Plotting Figure 9 ...")

fig, axes = plt.subplots(
    2,
    4,
    figsize=(16, 8),
    constrained_layout=True
)


def style_frame(ax):
    ax.set_xticks([])
    ax.set_yticks([])

    for spine in ax.spines.values():
        spine.set_visible(True)
        spine.set_linewidth(1.2)
        spine.set_edgecolor("black")


# Row 1: Δ mean daily precipitation
for i, e in enumerate(EXPS):
    ax = axes[0, i]

    im = ax.imshow(
        d_precip_s[e],
        origin="lower",
        cmap=cmap,
        norm=norm_p
    )

    style_frame(ax)

    letter = chr(ord("a") + i)

    ax.set_title(
        f"({letter}) {e}: ΔPrecip",
        fontsize=10,
        fontweight="bold"
    )

cb_p = fig.colorbar(
    im,
    ax=axes[0, :].tolist(),
    fraction=0.03,
    pad=0.02,
    shrink=0.9,
    orientation="vertical"
)

cb_p.set_label(
    r"$\Delta$Precip [mm d$^{-1}$]",
    fontsize=10
)

# Row 2: Δ wet-day frequency
for i, e in enumerate(EXPS):
    ax = axes[1, i]

    im = ax.imshow(
        d_wet_s[e],
        origin="lower",
        cmap=cmap,
        norm=norm_w
    )

    style_frame(ax)

    letter = chr(ord("e") + i)

    ax.set_title(
        f"({letter}) {e}: ΔWet-day freq",
        fontsize=10,
        fontweight="bold"
    )

cb_w = fig.colorbar(
    im,
    ax=axes[1, :].tolist(),
    fraction=0.03,
    pad=0.02,
    shrink=0.9,
    orientation="vertical"
)

cb_w.set_label(
    r"$\Delta$Wet-day freq [%]",
    fontsize=10
)

# ------------------------------------------------------------
# Save
# ------------------------------------------------------------
out_png = os.path.join(
    FIG_DIR,
    "fig9_precip_spatial_extent_replot.png"
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
