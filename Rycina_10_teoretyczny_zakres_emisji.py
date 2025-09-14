# --- Parametry czcionek ---
axis_fontsize = 18
legend_fontsize = 14
tick_fontsize = 16

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.lines import Line2D
from matplotlib.legend_handler import HandlerBase
from matplotlib.ticker import FuncFormatter

plt.rcParams["font.family"] = "Times New Roman"

# === Handler legendy: tło + kreskowana linia (bez kropki) ===
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

# === Wczytywanie CSV (obsługa przypadku „jedna kolumna”) ===
def load_emission_csv(path):
    df = pd.read_csv(path, sep=None, engine="python", dtype=str)
    if df.shape[1] == 1:
        split = df.iloc[:, 0].astype(str).str.split(",", expand=True)
        header = split.iloc[0].tolist()
        split = split.iloc[1:].reset_index(drop_by=True) if hasattr(split, "reset_index") else split.iloc[1:]
        # fallback, gdyby starsza wersja pandas nie miała drop_by:
        if not hasattr(split, "reset_index"):
            split = split.reset_index(drop=True)
        split.columns = header
        df = split
    df.columns = [str(c).strip() for c in df.columns]
    wl_col = next((c for c in df.columns if "wave" in c.lower()), df.columns[0])
    em_candidates = [c for c in df.columns if "em" in c.lower() and "ex" not in c.lower() and "2p" not in c.lower()]
    if not em_candidates:
        em_col = df.columns[1] if df.shape[1] >= 2 else df.columns[0]
    else:
        em_candidates.sort(key=len, reverse=True)
        em_col = em_candidates[0]
    wl = pd.to_numeric(df[wl_col], errors="coerce").to_numpy()
    em = pd.to_numeric(df[em_col], errors="coerce").to_numpy()
    mask = np.isfinite(wl) & np.isfinite(em)
    wl, em = wl[mask], em[mask]
    order = np.argsort(wl)
    return wl[order], em[order]

# === Dane ===
wl1, em1 = load_emission_csv("mNeon_green.csv")
wl2, em2 = load_emission_csv("mScarlet-I_.csv")

# (Opcjonalnie) normalizacja
NORMALIZE = True
if NORMALIZE:
    if np.nanmax(em1) > 0: em1 = em1 / np.nanmax(em1)
    if np.nanmax(em2) > 0: em2 = em2 / np.nanmax(em2)

# Zakresy emisji
granice = [510, 550, 585, 700]

# === Rysunek ===
plt.figure(figsize=(11, 4.5))
ax = plt.gca()

# Dwie linie – grube, bez punktów
ax.plot(wl1, em1, '-', color="green", linewidth=2.8, label="mNeonGreen (emisja)")
ax.plot(wl2, em2, '-', color="red",   linewidth=2.8, label="mScarlet-I (emisja)")

# Cieniowanie zakresów
mask1_green = (wl1 >= granice[0]) & (wl1 <= granice[1])
mask2_green = (wl2 >= granice[0]) & (wl2 <= granice[1])
mask1_red   = (wl1 >= granice[2]) & (wl1 <= granice[3])
mask2_red   = (wl2 >= granice[2]) & (wl2 <= granice[3])
ax.fill_between(wl1[mask1_green], em1[mask1_green], 0, color='green', alpha=0.2)
ax.fill_between(wl2[mask2_green], em2[mask2_green], 0, color='green', alpha=0.2)
ax.fill_between(wl1[mask1_red],   em1[mask1_red],   0, color='red',   alpha=0.2)
ax.fill_between(wl2[mask2_red],   em2[mask2_red],   0, color='red',   alpha=0.2)

# Linie graniczne + adnotacje i punkty
ymin, ymax = 0, max(np.nanmax(em1), np.nanmax(em2))
pad = 0.02*(ymax - ymin)

for i, g in enumerate(granice):
    col = 'green' if i < 2 else 'red'
    ax.axvline(x=g, color=col, linestyle='--')
    # adnotacje i punkt dla odpowiedniego widma
    spectrum_wl, spectrum_em = (wl1, em1) if i < 2 else (wl2, em2)
    y = np.interp(g, spectrum_wl, spectrum_em)
    ha = 'right' if (i % 2 == 0) else 'left'
    x_text = g - 2.5 if ha == 'right' else g + 2.5
    ax.text(x_text, y + pad, f"{g} nm",
            color=col, ha=ha, va='bottom',
            fontsize=12, fontweight='bold')
    ax.plot(g, y, 'o', color=col, markersize=9,
            markeredgecolor='white', markeredgewidth=1.5, zorder=5)

# Oś i siatka
ax.set_xlabel("Długość fali (nm)", fontsize=axis_fontsize, labelpad=12)
ax.set_ylabel("Znormalizowana\nintensywność fluorescencji" if NORMALIZE else "Intensywność emisji",
              fontsize=axis_fontsize, labelpad=12)
ax.tick_params(axis="both", labelsize=tick_fontsize)
ax.grid(True, linestyle=":", linewidth=0.8)

# Zasięg osi
ax.set_xlim(489, 790)
ax.set_ylim(bottom=0)

# Przecinki zamiast kropek
ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:.0f}".replace(".", ",")))
ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:.1f}".replace(".", ",")))

# Legenda
spec1_proxy = Line2D([], [], color="green", linestyle='-', linewidth=2.8, label="mNeonGreen (emisja)")
spec2_proxy = Line2D([], [], color="red",   linestyle='-', linewidth=2.8, label="mScarlet-I (emisja)")
green_range_proxy = Line2D([], [], color='green', label="Wybrany zakres emisji mNeonGreen")
red_range_proxy   = Line2D([], [], color='red',   label="Wybrany zakres emisji mScarlet-I")
ax.legend(
    handles=[spec1_proxy, spec2_proxy, green_range_proxy, red_range_proxy],
    handler_map={
        green_range_proxy: ShadedRangeHandler(alpha_fill=0.2, linewidth=2),
        red_range_proxy:   ShadedRangeHandler(alpha_fill=0.2, linewidth=2),
    },
    fontsize=legend_fontsize,
    loc="upper right",
    facecolor='white',
    framealpha=1,
    edgecolor='grey'
)

plt.tight_layout()
plt.show()
