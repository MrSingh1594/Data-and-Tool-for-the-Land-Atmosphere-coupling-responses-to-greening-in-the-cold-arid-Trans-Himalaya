# Data-and-tools-for-the-Land-Atmospheric-Coupling-response-to-greening-in-the-cold-arid-tans-Himalaya
Related-codes-and-reproducible figures
-----------------------
Reviewer_Reproduction
------------------------
│
├── code/
│   ├── replot_fig3_direct_response.py
│   ├── replot_M4.py
│   └── replot_precip_spatial_extent.py
│
├── data/
│   └── intermediates/
│       ├── direct_response_mean.nc
│       ├── direct_response_summary.csv
│       ├── M4_precip_per_cell.npz
│       ├── M4_wet_day_cdf.npz
│       ├── M4_pooled_summary.csv
│       └── precip_spatial_extent.npz
│
└── figures/
    ├── fig3_direct_response_replot.png
    ├── fig_M4_precip_dynamics_replot.png
    └── fig9_precip_spatial_extent_replot.png

-------------------------------
# Python Packages required
-------------------------------
numpy
pandas
matplotlib
scipy

-------------------------
# File path/directories
-------------------------

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DAT_DIR = BASE_DIR / "data" / "intermediates"
FIG_DIR = BASE_DIR / "figures"


-------------------
# Required files
-------------------
Figure								Python code to provide					Data required/summary
Fig. 3 — fig3_direct_response_replot				replot_fig3_direct_response.py				direct_response_mean.nc, direct_response_summary.csv
Fig. 8 — fig_M4_precip_dynamics_replot				replot_M4.py						M4_precip_per_cell.npz, M4_wet_day_cdf.npz, M4_pooled_summary.csv
Fig. 9 — fig9_precip_spatial_extent_replot			replot_precip_spatial_extent.py				precip_spatial_extent.npz


