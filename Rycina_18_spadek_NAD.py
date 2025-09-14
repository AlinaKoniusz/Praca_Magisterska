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
EXCEL_PATH = "wykres_dluga_hipoksja_powietrze.xlsx"  # <- ścieżka do Excela (tylko wartości)
SHEET_NAME = 0                                 # nazwa arkusza lub indeks (0)
HAS_HEADER = False                              # brak nagłówków kolumn -> False

FIGSIZE = (15, 7.5)
FONT_FAMILY = "Times New Roman"
AXIS_FONTSIZE = 24
TICK_FONTSIZE = 20
LINEWIDTH = 1.5
MARKERSIZE = 3
XTICK_STEP_MIN = 20
SAVE_PNG = False
PNG_PATH = "wykres_czas_komorki.png"
DPI = 300

# ==== OŚ CZASU (minuty) – Twoja lista punktów czasowych ====
TIME_POINTS = np.array([0, 5, 10, 15, 20,25,30,35,40,45,50,55,60,65,70,75,
80,85,90,95,100,105,110,115,120,125,130,135,140,145,150,155,160,165
], dtype=float)

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

# (opcjonalnie) interpolacja pojedynczych braków
df = df.interpolate(method="linear", axis=0, limit_direction="both")

# ==== RYSOWANIE ====
fig, ax = plt.subplots(figsize=FIGSIZE)

# Serie pomiarowe (bez legendy)
for col in df.columns:
    ax.plot(TIME_POINTS, df[col].values, "-o", linewidth=LINEWIDTH, markersize=MARKERSIZE)




# --- Pionowa linia zdarzenia ---
plt.rcParams["mathtext.fontset"] = "custom"
plt.rcParams["mathtext.rm"] = "Times New Roman"
plt.rcParams["mathtext.it"] = "Times New Roman:italic"
plt.rcParams["mathtext.bf"] = "Times New Roman:bold"

line_ola = ax.axvline(
    x=90, color="black", linestyle="dotted", linewidth=4, zorder=10,
    label="Moment osiągnięcia " + r"$\mathit{plateau}$"
)


line_reo = ax.axvline(
    x=60, color="black", linestyle="--", linewidth=4, zorder=10,
    label="Rozpoczęcie hipoksji"
)


# Opisy osi i podziałka X co 20 minut
ax.set_xlabel("Czas (min)", fontsize=AXIS_FONTSIZE, labelpad=15)
ax.set_ylabel("Znormalizowany\nstosunek fluorescencji czerwony/zielony", fontsize=AXIS_FONTSIZE, labelpad=15)
ax.tick_params(axis="both", labelsize=TICK_FONTSIZE)

ax.set_xlim(-2, float(TIME_POINTS.max()) + 2)
ax.xaxis.set_major_locator(MultipleLocator(XTICK_STEP_MIN))

# --- Przecinki zamiast kropek na osi Y ---
ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _: f"{y:.1f}".replace(".", ",")))

# Siatka
ax.grid(True, linestyle=":", linewidth=0.8)

# # Legenda TYLKO dla linii zdarzeń (serie zostają bez etykiet)
# ax.legend(
#     handles=[line_reo],
#     loc="upper right",
#     facecolor="white",
#     framealpha=1,
#     edgecolor="grey",
#     fontsize=16
# )
# Legenda
ax.legend(
    handles=[line_reo, line_ola],
    loc="upper right",
    facecolor="white",
    framealpha=1,
    edgecolor="grey",
    fontsize=20
)

plt.tight_layout()

if SAVE_PNG:
    plt.savefig(PNG_PATH, dpi=DPI, bbox_inches="tight")

plt.show()


