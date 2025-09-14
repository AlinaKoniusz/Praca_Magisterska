import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# ==== DANE (3 średnie + SD) ====
means = np.abs([-25.9620886, -17.6506686, -17.7126628, -18.0885655])
stds  = [2.9193099, 3.0129419, 4.9424418, 4.19317288]

# ==== Styl globalny ====
plt.rcParams["font.family"] = "Times New Roman"
AXIS_FONTSIZE = 20
TICK_FONTSIZE = 18
EDGE_COLOR = "black"

# --- Rysowanie ---
fig, ax = plt.subplots(figsize=(10, 7), constrained_layout=True)

ax.set_axisbelow(True)
ax.grid(True, axis="y", linestyle=":", linewidth=0.8, zorder=0)

n = len(means)
x = np.arange(n)
labels = [f"eksperyment {i+1}" for i in range(n)]

ax.bar(
    x, means, yerr=stds, width=0.4, capsize=8,
    color=["#8da0cb", "#66c2a5", "#ef8a8a", "#e9c46a"],
    edgecolor=EDGE_COLOR, ecolor=EDGE_COLOR,
    linewidth=1.2, zorder=2
)

# --- Oś X ---
ax.set_xticks(x)
ax.set_xticklabels(["Olaparib\neksperyment 1", "Olaparib\neksperyment 2", "Olaparib\neksperyment 3", "Eksperymenty\nbez olaparibu"],
                   fontsize=TICK_FONTSIZE)

# --- Oś Y ---
ax.set_ylabel("% średniego spadku stosunku fluorescencji\nczerwony/zielony", fontsize=AXIS_FONTSIZE, labelpad=12)
ax.tick_params(axis="y", labelsize=TICK_FONTSIZE)

# --- Formatowanie przecinki zamiast kropek ---
ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _: f"{y:.0f}".replace(".", ",")))

ax.margins(x=0.1)

plt.show()
