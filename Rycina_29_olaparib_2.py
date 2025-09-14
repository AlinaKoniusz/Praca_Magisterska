"""
Wykres wielu serii z Excela (tylko wartości), z osią czasu podaną w kodzie.
Dodane pionowe linie zdarzeń:
- X=64  : Rozpoczęcie hipoksji
- X=96  : Reoksygenacja
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FuncFormatter

# ==== KONFIGURACJA ====
EXCEL_PATH = "olaparib_2.xlsx"  # <- ścieżka do Excela (tylko wartości)
SHEET_NAME = 0                  # nazwa arkusza lub indeks (0)
HAS_HEADER = False              # brak nagłówków kolumn -> False

FIGSIZE = (11, 7.5)
FONT_FAMILY = "Times New Roman"
AXIS_FONTSIZE = 26
TICK_FONTSIZE = 20
LINEWIDTH = 1.5
MARKERSIZE = 3
XTICK_STEP_MIN = 20
SAVE_PNG = False
PNG_PATH = "wykres_czas_komorki.png"
DPI = 300

# ==== OŚ CZASU (minuty) ====
TIME_POINTS = np.array([
    0, 5, 10, 15, 20, 25, 30, 35, 40, 45,
    50, 55, 60, 65, 67, 72, 77, 82, 87
], dtype=float)

# ==== USTAWIENIA MATPLOTLIB ====
plt.rcParams["font.family"] = FONT_FAMILY

# ==== WCZYTANIE DANYCH ====
header_arg = 0 if HAS_HEADER else None
df = pd.read_excel(EXCEL_PATH, sheet_name=SHEET_NAME, header=header_arg)

df = df.apply(pd.to_numeric, errors="coerce").dropna(how="all")

# Dopasowanie długości danych
n_time = len(TIME_POINTS)
n_rows = len(df)
if n_rows < n_time:
    TIME_POINTS = TIME_POINTS[:n_rows]
else:
    df = df.iloc[:n_time, :]

df = df.interpolate(method="linear", axis=0, limit_direction="both")

# ==== RYSOWANIE ====
fig, ax = plt.subplots(figsize=FIGSIZE)

for col in df.columns:
    ax.plot(TIME_POINTS, df[col].values, "-o", linewidth=LINEWIDTH, markersize=MARKERSIZE)

# --- Pionowa linia zdarzenia ---
line_ola = ax.axvline(
    x=30, color="black", linestyle="dotted", linewidth=4, zorder=10,
    label="Dodanie Olaparibu"
)
line_reo = ax.axvline(
    x=66, color="black", linestyle="--", linewidth=4, zorder=10,
    label="Rozpoczęcie hipoksji"
)

# Opisy osi
ax.set_xlabel("Czas (min)", fontsize=AXIS_FONTSIZE, labelpad=15)
ax.set_ylabel("Znormalizowany stosunek fluorescencji\nczerwony/zielony", fontsize=AXIS_FONTSIZE, labelpad=15)
ax.tick_params(axis="both", labelsize=TICK_FONTSIZE)

# Zakresy osi
ax.set_xlim(-1, 88)
ax.set_ylim(0.65, 1.45)  # <--- ustawienie zakresu Y

ax.xaxis.set_major_locator(MultipleLocator(XTICK_STEP_MIN))

# --- Przecinki zamiast kropek na osi Y ---
ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _: f"{y:.1f}".replace(".", ",")))

# Siatka
ax.grid(True, linestyle=":", linewidth=0.8)

# Legenda
ax.legend(
    handles=[line_ola,line_reo],
    loc="lower left",
    facecolor="white",
    framealpha=1,
    edgecolor="grey",
    fontsize=16
)

plt.tight_layout()

if SAVE_PNG:
    plt.savefig(PNG_PATH, dpi=DPI, bbox_inches="tight")

plt.show()
