import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import FancyBboxPatch

# spójność estetyczna
plt.rcParams["font.family"] = "Times New Roman"

def draw_arrow(ax, start_x, end_x, y_position,
               color='black', line_width=2, mutation_scale=28):
    ax.annotate(
        '',
        xy=(end_x, y_position),
        xytext=(start_x, y_position),
        arrowprops=dict(arrowstyle='-|>', lw=line_width,
                        color=color, mutation_scale=mutation_scale)
    )

def interp_at(x_target, x, y):
    m = np.isfinite(x) & np.isfinite(y)
    if m.sum() < 2:
        return np.nan
    order = np.argsort(x[m])
    xx = x[m][order]
    yy = y[m][order]
    if x_target < xx[0] or x_target > xx[-1]:
        return np.nan
    return float(np.interp(x_target, xx, yy))

def plot_raw_data_from_excel(file_path):
    # --- wczytanie danych ---
    try:
        df = pd.read_excel(file_path, sheet_name=0, header=None, decimal=',')
    except Exception as e:
        print(f"❌ BŁĄD: Nie mogę wczytać pliku '{file_path}': {e}")
        return

    if df.shape[1] < 2:
        print("❌ BŁĄD: Plik musi mieć ≥2 kolumny (czas + co najmniej 1 seria).")
        return

    time = pd.to_numeric(df.iloc[:, 0], errors='coerce')
    values = df.iloc[:, 1:].apply(pd.to_numeric, errors='coerce')

    mask = time.notna()
    time = time[mask].to_numpy()
    values = values[mask]

    if time.size == 0:
        print("❌ BŁĄD: Brak poprawnych wartości czasu.")
        return

    Y = values.to_numpy(dtype=float)
    # krzywa średnia po wierszach (po czasie), z pominięciem NaN
    y_mean = np.nanmean(Y, axis=1)

    # --- rysunek ---
    fig, ax = plt.subplots(figsize=(11, 5.5))

    # tło: pojedyncze serie – cienkie, półprzezroczyste
    for col in values.columns:
        ax.plot(time, values[col].to_numpy(), linewidth=1.2, alpha=0.35, color="#555555")

    # wyróżniona krzywa średnia – gruba, ciemna
    mean_line, = ax.plot(time, y_mean, linewidth=3.0, color="#202020", label="Średnia z serii")

    # osie i siatka
    ax.set_xlabel("Czas (min)", fontsize=20, labelpad=12)
    ax.set_ylabel("Stężenie objętościowe tlenu (%)", fontsize=20, labelpad=12)
    ax.tick_params(axis='both', labelsize=18)
    ax.grid(True, linestyle=":", linewidth=0.8)


    # podpis przy linii (delikatnie nad dołem wykresu)
    ymin, ymax = np.nanmin(Y), np.nanmax(Y)
    yspan = (ymax - ymin) if np.isfinite(ymax - ymin) and (ymax - ymin) > 0 else 1.0


    # strzałka 26 → 90 na poziomie y ~ 10% zakresu (jeśli chcesz na stałym Y, podaj stałą)
    arrow_y = ymin + 0.18*yspan


    # ===== Poziome linie w Y(x=56) i Y(x=71) – czarne, różne wzory =====
    X1, X2 = 56.0-26, 71.0-26

    def y_at_x_on_mean(xq):
        return interp_at(xq, time, y_mean)

    y56 = y_at_x_on_mean(X1)
    y71 = y_at_x_on_mean(X2)

    # niestandardowe wzory kreskowania (bardziej rozróżnialne niż ':' i '-.')
    # (0, (dash_len, gap_len, ...))
    ls2 = (0, (6, 3))      # długa kreska – przerwa
    ls1 = (0, (2, 2, 1, 2)) # kropka-kreska (punktowane)

#     # poziome linie
#     if np.isfinite(y56):
#         h1 = ax.axhline(y56, color='violet', linewidth=3, linestyle=ls1)
#         # duży marker na przecięciu średniej z X1
#         ax.plot(X1, y56, 'o', color='violet', markersize=9,
#                 markeredgecolor='white', markeredgewidth=1.6, zorder=5)

    if np.isfinite(y71):
        h2 = ax.axhline(y71, color='violet', linewidth=3, linestyle=ls2)
        ax.plot(X2, y71, 'o', color='violet', markersize=9,
                markeredgecolor='white', markeredgewidth=1.6, zorder=5)

    # dyskretne etykiety przy liniach poziomych (po prawej)
    x_right = float(np.nanmax(time))


    # zakresy osi
    ax.set_xlim(left=min(0, float(np.nanmin(time))), right=float(np.nanmax(time)))
    ax.set_ylim(bottom=0, top=17)

    # ustawienia osi Y – tylko nieparzyste ticki
    ymin, ymax = ax.get_ylim()
    odd_ticks = np.arange(np.ceil(ymin), np.floor(ymax)+1, 1)
    odd_ticks = odd_ticks[odd_ticks % 2 == 1]
    ax.set_yticks(odd_ticks)

    # zamknięta ramka
    for side in ("top", "right", "bottom", "left"):
        ax.spines[side].set_visible(True)


    # legenda (spójna – białe tło, szara ramka)
#     proxy_y56  = Line2D([], [], color='violet', linestyle=ls1, linewidth=3, label='Stężenie objętościowe tlenu (%) po 30 min hipoksji')
    proxy_y71  = Line2D([], [], color='violet', linestyle=ls2, linewidth=3, label='Poziom objętościowego stężenia tlenu (%) po 45 min hipoksji')
    ax.legend(handles=[proxy_y71],
              fontsize=16, loc='upper right',
              facecolor='white', framealpha=1, edgecolor='grey')

    plt.tight_layout()
    plt.show()

# --- uruchomienie ---
file_path = "Kinga_Serafin_tlen.xlsx"
plot_raw_data_from_excel(file_path)
