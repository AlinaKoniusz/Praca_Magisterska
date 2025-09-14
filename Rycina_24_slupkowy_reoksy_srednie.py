import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# ==== DANE ====
labels = ["równowaga z powietrzem", "koniec hipoksji", "reoksygenacja"]
means  = [0.715066493, 0.585729695, 0.705680084]
stds   = [0.05795697, 0.056462138, 0.062264931]

# ==== Styl ====
plt.rcParams["font.family"] = "Times New Roman"
AXIS_FONTSIZE = 20
TICK_FONTSIZE = 18
EDGE_COLOR = "black"
BAR_COLORS = ["#9ecae1", "#d63c3c", "#a6dba0"]

# --- Walidacja ---
n = len(labels)
if not (len(means) == len(stds) == n):
    raise ValueError("labels, means i stds muszą mieć tę samą długość.")

# --- Rozmieszczenie ---
bar_width = 0.5
x = np.arange(n)

# --- Rysowanie ---
fig, ax = plt.subplots(figsize=(10, 6))

ax.set_axisbelow(True)
ax.grid(True, axis="y", linestyle=":", linewidth=0.8, zorder=0)

ax.bar(
    x, means,
    yerr=stds,
    width=bar_width,
    capsize=8,
    color=BAR_COLORS[:n],
    edgecolor=EDGE_COLOR,
    ecolor=EDGE_COLOR,
    linewidth=1.2,
    zorder=2
)

# --- Oś X ---
ax.set_xticks(x)
ax.set_xticklabels(labels, rotation=0, ha="center", fontsize=TICK_FONTSIZE)

# 🔹 lekkie wycentrowanie słupków
ax.set_xlim(-0.5, n - 0.5)   # dodaje równy margines po obu stronach

# --- Oś Y ---
ax.set_ylabel("Średni stosunek fluorescencji czerwony/zielony", fontsize=AXIS_FONTSIZE, labelpad=30)
ax.tick_params(axis="y", labelsize=TICK_FONTSIZE)
ax.yaxis.set_major_formatter(FuncFormatter(lambda val, _: f"{val:.1f}".replace(".", ",")))

# --- Marginesy ---
fig.tight_layout(pad=1.0)
fig.subplots_adjust(left=0.23)

plt.show()

