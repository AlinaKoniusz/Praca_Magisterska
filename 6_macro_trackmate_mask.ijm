// 6.
// previous: 5. stardist_binary
// next: 7. loop
// Wynik z TrackMate (plik RGB) przekształca na maskę o właściwej skali
// Poprawienie ręczne maski (pos + _TrackMate_mask.tif) --> wystające elementy itp

for (i = 1; i <= 6; i++) {
    pos = "pos" + i;
    
    for (i = 1; i <= 6; i++) {
    pos = "pos" + i;
   
    // Otwarcie pliku
    open("C:/Users/3000000/Desktop/STUDIA/UJ/magisterka/glowne eksperymenty grudzien/analiza makro/aktywne makro/stardist segmentation/trackmate stardist/" + pos + "_TrackMate_1.tif");
   
    // Eliminacja zbędnych komórek
    selectImage(pos + "_TrackMate_1.tif");
    minVal = 129;
    maxVal = 383;
    n = 20;
    for (s = 1; s <= n; s++) {
        setSlice(s);
        setMinAndMax(minVal, maxVal);
    }
    
    //Binaryzacja
    run("8-bit");
    setAutoThreshold("Default dark no-reset");
    setThreshold(1, 255, "raw");
    setOption("BlackBackground", true);
    run("Convert to Mask", "background=Dark calculate black");
    run("Remove Outliers...", "radius=2 threshold=50 which=Bright stack");
    
    // Przeskalowanie
    run("Scale...", "x=- y=- z=1.0 width=512 height=512 depth=44 interpolation=Bilinear average process create");
    setAutoThreshold("Default dark no-reset");
    setThreshold(1, 255, "raw");
    run("Convert to Mask", "background=Dark calculate black");
    
    // Zapis
    saveAs("Tiff", "C:/Users/3000000/Desktop/STUDIA/UJ/magisterka/glowne eksperymenty grudzien/analiza makro/aktywne makro/stardist segmentation/trackmate stardist/" + pos + "_TrackMate_mask.tif");
    selectImage(pos + "_TrackMate_1.tif");
    saveAs("Tiff", "C:/Users/3000000/Desktop/STUDIA/UJ/magisterka/glowne eksperymenty grudzien/analiza makro/aktywne makro/stardist segmentation/trackmate stardist/" + pos + "_TrackMate_2.tif");
}
