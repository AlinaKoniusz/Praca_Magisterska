// 3.
// previous: 2. makro_delete_slices - tylko że zdaje się potem na sam koniec usuwałam slcies
// next: 4. makro_StarDist
// Łączy plane 0 i 1, a następnie ustawia gammę na 0,7 i filtr gaussa na 1



// ------------------  PARAMETRY  ------------------
basePath = "C:/Users/3000000/Desktop/STUDIA/UJ/magisterka/glowne eksperymenty grudzien/analiza makro/aktywne makro/";
nPos     = 4;                 // <- zmień, gdy pozycji jest więcej/mniej
// -------------------------------------------------

for (p = 1; p <= nPos; p++) {

    pos        = "pos" + p;                     
    plane0Name = pos + "_timelaps_plane_0.tif";
    plane1Name = pos + "_timelaps_plane_1.tif";

    // ── 1. Otwórz oba kanały (gdy nie są jeszcze w pamięci) ──
    open(basePath + plane0Name);
    open(basePath + plane1Name);

    // ── 2. Zrób duplikaty, żeby nie nadpisywać oryginałów ──
    selectImage(plane0Name);
    dup0 = pos + "_timelaps_plane_0-1.tif";
    run("Duplicate...", "title=" + dup0 + " duplicate");

    selectImage(plane1Name);
    dup1 = pos + "_timelaps_plane_1-1.tif";
    run("Duplicate...", "title=" + dup1 + " duplicate");

    // (opcjonalne) upewnij się, że oryginały są zapisane
    selectImage(plane0Name); run("Save");
    selectImage(plane1Name); run("Save");

    // ── 3. Dodaj obydwa stosy (Image Calculator → Add stack) ──
    imageCalculator("Add stack", dup0, dup1);     // wynik jest aktywny
    addName = pos + "_timelaps_plane_0_add_1.tif";
    run("Rename...", "title=" + addName);
    saveAs("Tiff", basePath + addName);

    // ── 4. Duplikat do obróbki, gamma 0,7 i filtr Gaussa σ = 1 ──
    run("Duplicate...", "title=" + pos + "_timelaps_plane_0_add_1-1.tif duplicate");
    selectImage(pos + "_timelaps_plane_0_add_1-1.tif");
    run("Gamma...", "value=0.7 stack");
    run("Gaussian Blur...", "sigma=1 stack");
    saveAs("Tiff", basePath + pos + "_timelaps_plane_0_add_1_gamma_gaus.tif");

    // ── 5. Sprzątanie – zamykamy wszystko, żeby zwolnić RAM ──
    run("Close All");
}
