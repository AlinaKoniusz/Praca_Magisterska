"""
Wykres średniej ± SD (linia) oraz wykres słupkowy ± SD (tylko pierwszy i ostatni pomiar).
Panel słupkowy jest mniejszy dzięki gridspec_kw.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FuncFormatter

# ==== KONFIGURACJA ====
EXCEL_PATH = "wykres_sensor_hipoksja_srednia.xlsx"
SHEET_NAME = 0
HAS_HEADER = False

FIGSIZE = (13, 6)
FONT_FAMILY = "Times New Roman"
AXIS_FONTSIZE = 20
TICK_FONTSIZE = 18
LINEWIDTH = 2
MARKERSIZE = 5
XTICK_STEP_MIN = 10
YMIN, YMAX = 0.5, 0.8
SAVE_PNG = False
PNG_PATH = "wykres_linia_plus_slupki.png"
DPI = 300

# ==== OŚ CZASU (minuty) ====
TIME_POINTS = np.array([0, 5, 10, 15, 20, 25, 30, 35, 40, 45], dtype=float)

# ==== USTAWIENIA MATPLOTLIB ====
plt.rcParams["font.family"] = FONT_FAMILY

# ==== WCZYTANIE DANYCH ====
header_arg = 0 if HAS_HEADER else None
df = pd.read_excel(EXCEL_PATH, sheet_name=SHEET_NAME, header=header_arg)
df = df.apply(pd.to_numeric, errors="coerce").dropna(how="all")
df = df.iloc[:len(TIME_POINTS), :]   # dopasowanie długości

means = df.iloc[:, 0].values
stds  = df.iloc[:, 1].values

# ==== RYSOWANIE: dwa panele z różną szerokością ====
fig, (ax1, ax2) = plt.subplots(
    ncols=2, figsize=FIGSIZE, constrained_layout=True, sharey=True,
    gridspec_kw={"width_ratios": [3, 1]}  # <-- panel liniowy 3x szerszy
)

# --- Panel 1: linia z wąsami
ax1.errorbar(
    TIME_POINTS, means, yerr=stds,
    fmt="-o", color="green", ecolor="black",
    elinewidth=1.2, capsize=4,
    linewidth=LINEWIDTH, markersize=MARKERSIZE
)
ax1.set_xlabel("Czas (min)", fontsize=AXIS_FONTSIZE, labelpad=12)
ax1.set_ylabel("Stosunek fluorescencji czerwony/zielony", fontsize=AXIS_FONTSIZE, labelpad=12)
ax1.tick_params(axis="both", labelsize=TICK_FONTSIZE)
ax1.set_xlim(-1, float(TIME_POINTS.max()) + 1)
ax1.set_ylim(YMIN, YMAX)
ax1.xaxis.set_major_locator(MultipleLocator(XTICK_STEP_MIN))
ax1.yaxis.set_major_formatter(FuncFormatter(lambda y, _: f"{y:.1f}".replace('.', ',')))
ax1.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{int(x)}"))
ax1.grid(True, linestyle=":", linewidth=0.8)

# --- Panel 2: słupki ± SD (tylko pierwszy i ostatni punkt)
subset_means = [means[0], means[-1]]
subset_stds  = [stds[0], stds[-1]]
subset_labels = [f"{int(TIME_POINTS[0])}", f"{int(TIME_POINTS[-1])}"]

x = np.arange(len(subset_means))
ax2.bar(
    x, subset_means, yerr=subset_stds,
    width=0.6, capsize=6,
    color="#66c2a5", edgecolor="black", ecolor="black",
    linewidth=1.2, zorder=2
)
ax2.set_xlabel("Czas (min)", fontsize=AXIS_FONTSIZE, labelpad=12)
ax2.tick_params(axis="both", labelsize=TICK_FONTSIZE)
ax2.set_ylim(YMIN, YMAX)
ax2.set_xticks(x)
ax2.set_xticklabels(subset_labels, rotation=0, ha="center", fontsize=TICK_FONTSIZE)
ax2.yaxis.set_major_formatter(FuncFormatter(lambda y, _: f"{y:.2f}".replace('.', ',')))
ax2.grid(True, axis="y", linestyle=":", linewidth=0.8)

if SAVE_PNG:
    plt.savefig(PNG_PATH, dpi=DPI, bbox_inches="tight")

plt.show()
