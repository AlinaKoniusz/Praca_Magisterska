// 1 
// ======================
//  PARAMETRY DO EDYCJI
// ======================
basePath = "C:/Users/3000000/Desktop/STUDIA/UJ/magisterka/glowne eksperymenty grudzien/analiza makro/aktywne makro/";
nPos     = 4;   // <- ile pozycji (pos1 … posN) chcesz przetworzyć
nPlanes  = 2;   // <- ile kanałów (0 = C0, 1 = C1, …) ma każdy plik
// ======================

for (p = 1; p <= nPos; p++) {                // pętla po pozycjach
    pos = "pos" + p;                         // np. "pos3"

    for (c = 0; c < nPlanes; c++) {          // pętla po kanałach (plane 0, 1 …)
        title = pos + "_timelaps_plane_" + c;

        // -------- budowa argumentu Concatenate --------
        cmd  = "title=" + title;
        cmd += " image1=[eksperyment.lif - " + pos + "_control - C=" + c + "]";
        cmd += " image2=[eksperyment.lif - " + pos + "_control2 - C=" + c + "]";
        cmd += " image3=[eksperyment.lif - " + pos + "_hypoxia - C=" + c + "]";
        cmd += " image4=[eksperyment.lif - " + pos + "_reoxygenation1 - C=" + c + "]";
        cmd += " image5=[eksperyment.lif - " + pos + "_reoxygenation2 - C=" + c + "]";
        cmd += " image6=[-- None --]";       // piąty slot pusty – zostaje tak, jak w oryginale
        // ----------------------------------------------

        run("Concatenate...", cmd);

        // zapis scalonego stacka
        saveAs("Tiff", basePath + title + ".tif");

        //run("Duplicate...");                 // zostawiam, bo było w Twoim kodzie
        // close(title);                     // (opcjonalnie) zamknij, gdy brakuje RAM-u
    }
}
