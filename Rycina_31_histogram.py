import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

# ==== Wczytanie danych z Excela ====
file = "olaparib3_histogram.xlsx"
df = pd.read_excel(file)

# bierzemy pierwszą kolumnę z wartościami liczbowymi
data = df.iloc[:, 0].dropna().values  

# ==== Parametry histogramu ====
bin_width = 3
bins = np.arange(min(data), max(data) + bin_width, bin_width)

plt.rcParams["font.family"] = "Times New Roman"
AXIS_FONTSIZE = 20
TICK_FONTSIZE = 16
EDGE_COLOR = "black"

fig, ax = plt.subplots(figsize=(12, 6), constrained_layout=True)

# --- Histogram ---
counts, edges, patches = ax.hist(
    data, bins=bins, edgecolor=EDGE_COLOR, linewidth=1.2, zorder=2
)

# --- Kolory ---
base_color = "#f5e6a1"       # żółtawy/beżowy dla <= -11
transition_color = "#f4a261" # pomarańcz dla -11 do -8
cmap = mcolors.LinearSegmentedColormap.from_list("orange_to_red", [transition_color, "#ff0000"])

# gradient działa od -8 w górę
norm = mcolors.Normalize(vmin=-8, vmax=max(data))

for count, edge_left, edge_right, patch in zip(counts, edges[:-1], edges[1:], patches):
    center = (edge_left + edge_right) / 2
    if center <= -11:
        patch.set_facecolor(base_color)
    elif -11 < center <= -8:
        patch.set_facecolor(transition_color)
    else:
        patch.set_facecolor(cmap(norm(center)))

# --- Linie pomocnicze (siatka) ---
ax.set_axisbelow(True)
ax.grid(True, axis="y", linestyle=":", linewidth=0.8, color="gray", zorder=0)

# --- Podpisy nad słupkami ---
for count, edge_left, edge_right in zip(counts, edges[:-1], edges[1:]):
    if count > 0:
        center = (edge_left + edge_right) / 2
        ax.text(center, count, str(int(count)),
                ha="center", va="bottom", fontsize=12)

# --- Oś X: podpisy przedziałów ---
labels = [f"{int(edge_left)} do {int(edge_right)}"
          for edge_left, edge_right in zip(edges[:-1], edges[1:])]
ax.set_xticks((edges[:-1] + edges[1:]) / 2)  
ax.set_xticklabels(labels, rotation=30, ha="right", fontsize=TICK_FONTSIZE)

# --- Oś Y ---
ax.tick_params(axis="y", labelsize=TICK_FONTSIZE)

# --- Opisy osi ---
ax.set_xlabel("Zmiana stosunku fluorescencji czerwonej/zielonej w hipoksji (%)", fontsize=AXIS_FONTSIZE, labelpad=10)
ax.set_ylabel("Liczność komórek", fontsize=AXIS_FONTSIZE, labelpad=10)

# --- Marginesy ---
ax.margins(x=0.05)

plt.show()
