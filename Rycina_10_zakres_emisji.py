import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.lines import Line2D
from matplotlib.legend_handler import HandlerBase
from matplotlib.ticker import FuncFormatter

plt.rcParams["font.family"] = "Times New Roman"

# --- Handler legendy: tło + kreskowana linia (bez kropki) ---
class ShadedRangeHandler(HandlerBase):
    def __init__(self, alpha_fill=0.2, linewidth=2, **kwargs):
        super().__init__(**kwargs)
        self.alpha_fill = alpha_fill
        self.linewidth = linewidth
    def legend_artist(self, legend, orig_handle, fontsize, handlebox):
        color = orig_handle.get_color()
        x0, y0 = handlebox.xdescent, handlebox.ydescent
        w, h = handlebox.width, handlebox.height
        bg = Rectangle((x0, y0), w, h, facecolor=color, edgecolor='none', alpha=self.alpha_fill)
        handlebox.add_artist(bg)
        y_mid = y0 + h/2
        ln = Line2D([x0, x0 + w], [y_mid, y_mid],
                    color=color, linestyle='--', linewidth=self.linewidth,
                    dash_capstyle='butt', solid_capstyle='butt')
        handlebox.add_artist(ln)
        return [bg, ln]

# ------------------ Dane ------------------
x = np.loadtxt("spektrum_emisji_os_X.txt")
y = np.loadtxt("spektrum_emisji_os_Y.txt")
# normalizacja do 1
y = y / np.max(y)

granice = [510, 550, 585, 700]

plt.figure(figsize=(11, 5.5))
ax = plt.gca()

# Spektrum z drobnymi markerami co 5 nm
ax.plot(x, y, '-o', color="#505050", markersize=3)

# Cieniowanie
mask_green = (x >= granice[0]) & (x <= granice[1])
ax.fill_between(x[mask_green], y[mask_green], 0, color='green', alpha=0.2)

mask_red = (x >= granice[2]) & (x <= granice[3])
ax.fill_between(x[mask_red], y[mask_red], 0, color='red', alpha=0.2)

# Granice zakresów + duże kropki
for i, g in enumerate(granice):
    idx = (np.abs(x - g)).argmin()
    y_val = y[idx]
    col = 'green' if i < 2 else 'red'
    ax.axvline(x=g, color=col, linestyle='--')
    ax.plot(x[idx], y_val, 'o', color=col,
            markersize=9, markeredgecolor='white',
            markeredgewidth=1.5, zorder=5)
    ax.text(g + 2.5, y_val + 0.02, f"{g} nm",
            color=col, ha='left', va='bottom',
            fontsize=12, fontweight='bold')

# --- Parametry czcionek ---
axis_fontsize = 18
legend_fontsize = 14
tick_fontsize = 16

ax.set_xlabel("", fontsize=axis_fontsize, labelpad=12)
ax.set_ylabel("Znormalizowana\nintensywność fluorescencji", fontsize=axis_fontsize, labelpad=12)

# === Formatowanie osi ===
# 1) przecinki zamiast kropek
ax.xaxis.set_major_formatter(FuncFormatter(lambda val, _: f"{val:.0f}".replace(".", ",")))
ax.yaxis.set_major_formatter(FuncFormatter(lambda val, _: f"{val:.1f}".replace(".", ",")))

# 2) brak podpisów na osi X (zostają same kreski)
ax.set_xticklabels([])

# 3) dłuższe ticki (kreski) na obu osiach
ax.tick_params(axis="x", which="major", length=10, width=1)
ax.tick_params(axis="both", labelsize=tick_fontsize)

# Legenda
spec_handle = Line2D([], [], color="#303030", marker='o', linestyle='-',
                     label="Spektrum emisji")
green_proxy = Line2D([], [], color='green', label="Wybrany zakres emisji mNeonGreen")
red_proxy   = Line2D([], [], color='red',   label="Wybrany zakres emisji mScarlet-I")

ax.legend(
    handles=[spec_handle, green_proxy, red_proxy],
    handler_map={
        green_proxy: ShadedRangeHandler(alpha_fill=0.2, linewidth=2),
        red_proxy:   ShadedRangeHandler(alpha_fill=0.2, linewidth=2),
    },
    fontsize=legend_fontsize,
    loc="upper right",
    facecolor='white',
    framealpha=1,
    edgecolor='grey'
)

ax.set_ylim(0, 1.05)   # od 0 do trochę ponad 1
ax.set_xlim(489, 790)

# linie pomocnicze
ax.grid(True, linestyle=":", linewidth=0.8)

plt.tight_layout()
plt.show()
