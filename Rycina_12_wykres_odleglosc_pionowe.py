import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

# Ustawienie czcionki Times New Roman globalnie
plt.rcParams["font.family"] = "Times New Roman"

# ------------------ Dane ------------------
x = np.loadtxt("odleglosc_os_X.txt")  # odległość (µm)
y = np.loadtxt("odleglosc_os_Y.txt")  # intensywność fluorescencji

plt.figure(figsize=(6,7.5))
plt.plot(y, x, '-o', color="green", markersize=3)  # zamiana osi

# --- Zacieniowanie wybranego zakresu (nad progiem) ---
threshold = 22.69594857
mask = (x >= 70.312606812) & (x <= 143.750228882)
plt.fill_betweenx(x[mask], y[mask], threshold,
                  where=(y[mask] > threshold),
                  color='green', alpha=0.3, label="Zakres powyżej progu")

# --- Linia progu (teraz pionowa) ---
plt.axvline(x=threshold, color='red', linestyle='--', linewidth=1.5)

# --- Parametry czcionek ---
axis_fontsize = 18
legend_fontsize = 16
tick_fontsize = 16

plt.ylabel("Odległość (µm)", fontsize=axis_fontsize, labelpad=15)   # było xlabel
plt.xlabel("Znormalizowana intensywność fluorescencji", fontsize=axis_fontsize, labelpad=15)  # było ylabel
plt.xticks(fontsize=tick_fontsize)
plt.yticks(fontsize=tick_fontsize)

# --- Legenda ---
spec_handle = Line2D([], [], color="green", marker='o', linestyle='-',
                     label="Spektrum emisji")

line_threshold = plt.axvline(
    x=threshold, color='red', linestyle='--', linewidth=1.5,
    label="Próg odcięcia tła"
)

plt.legend(
    handles=[spec_handle, line_threshold],
    fontsize=legend_fontsize,
    loc="upper right",
    facecolor='white',
    framealpha=1,
    edgecolor='grey'
)

# Zakresy osi i siatka
plt.xlim(0, None)   # teraz X = intensywność fluorescencji
plt.ylim(0, 400)    # Y = odległość (µm)
plt.grid(True, linestyle=":", linewidth=0.8)

plt.tight_layout()
plt.show()
