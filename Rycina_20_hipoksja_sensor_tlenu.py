"""
Wykres wielu serii z Excela (tylko wartości), z osią czasu podaną w kodzie.
Dodane pionowe linie zdarzeń:
- X=64  : Rozpoczęcie hipoksji
- X=96  : Rozpoczęcie reoksygenacji
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FuncFormatter

# ==== KONFIGURACJA ====
EXCEL_PATH = "wykres_sensor_hipoksja.xlsx"  # <- ścieżka do Excela (tylko wartości)
SHEET_NAME = 0                              # nazwa arkusza lub indeks (0)
HAS_HEADER = False                          # brak nagłówków kolumn -> False

FIGSIZE = (11, 7.5)
FONT_FAMILY = "Times New Roman"
AXIS_FONTSIZE = 20
TICK_FONTSIZE = 18
LINEWIDTH = 1.5
MARKERSIZE = 3
XTICK_STEP_MIN = 10
SAVE_PNG = False
PNG_PATH = "wykres_czas_komorki.png"
DPI = 300

# ==== OŚ CZASU (minuty) – Twoja lista punktów czasowych ====
TIME_POINTS = np.array([0, 5, 10, 15, 20, 25, 30, 35, 40, 45], dtype=float)

# ==== USTAWIENIA MATPLOTLIB ====
plt.rcParams["font.family"] = FONT_FAMILY

# ==== WCZYTANIE DANYCH Z EXCELA (tylko wartości) ====
header_arg = 0 if HAS_HEADER else None
df = pd.read_excel(EXCEL_PATH, sheet_name=SHEET_NAME, header=header_arg)

# Zamiana na liczby i usunięcie pustych wierszy
df = df.apply(pd.to_numeric, errors="coerce").dropna(how="all")

# Dopasowanie długości danych do liczby punktów czasu
n_time = len(TIME_POINTS)
n_rows = len(df)
if n_rows < n_time:
    TIME_POINTS = TIME_POINTS[:n_rows]
else:
    df = df.iloc[:n_time, :]

# Interpolacja braków
df = df.interpolate(method="linear", axis=0, limit_direction="both")

# ==== RYSOWANIE ====
fig, ax = plt.subplots(figsize=FIGSIZE)

# Serie pomiarowe (bez legendy)
for col in df.columns:
    ax.plot(TIME_POINTS, df[col].values, "-o", linewidth=LINEWIDTH, markersize=MARKERSIZE)

# Opisy osi i podziałka X co 10 minut
ax.set_xlabel("Czas (min)", fontsize=AXIS_FONTSIZE, labelpad=15)
ax.set_ylabel("Znormalizowany stosunek fluorescencji czerwona/zielona", fontsize=AXIS_FONTSIZE, labelpad=15)
ax.tick_params(axis="both", labelsize=TICK_FONTSIZE)

# Zakresy osi
ax.set_xlim(-1, float(TIME_POINTS.max()) + 1)
ax.set_ylim(0.7, None)  # Y od 0.7

# Podziałka X
ax.xaxis.set_major_locator(MultipleLocator(XTICK_STEP_MIN))

# Formatowanie liczb z przecinkami zamiast kropek
ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x:.1f}".replace('.', ',')))
ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{int(x)}"))

# Siatka
ax.grid(True, linestyle=":", linewidth=0.8)

plt.tight_layout()

if SAVE_PNG:
    plt.savefig(PNG_PATH, dpi=DPI, bbox_inches="tight")

plt.show()
