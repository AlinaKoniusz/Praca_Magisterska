// 5.
// previous: 4. makro_StarDist
// next: 6. makro_trackmate_mask
//Ważne! Zrobić najpierw color threshold
//Po tym idziemy do trackmate żeby wyeliminować komórki odpadające z analizy
 

for (i = 1; i <= 4; i++) {
    pos = "pos" + i;
    
    // Upewnij się, że pracujemy na właściwym obrazie
    selectImage(pos + "_StarDist_segmentation.tif");
    
    run("8-bit");
    setAutoThreshold("Default dark no-reset");
    setThreshold(1, 255, "raw");
    setOption("BlackBackground", true);
    run("Convert to Mask", "background=Dark calculate black");

    run("Grays");
    
    saveAs("Tiff", "C:/Users/3000000/Desktop/STUDIA/UJ/magisterka/"
        + "glowne eksperymenty grudzien/analiza makro/aktywne makro/"
        + "stardist segmentation/" + pos + "_StarDist_segmentation_binary.tif");
    
    run("Watershed", "stack");
    run("Analyze Particles...", "show=Masks display exclude summarize stack");
    
    run("Grays");
    
    saveAs("Tiff", "C:/Users/3000000/Desktop/STUDIA/UJ/magisterka/"
        + "glowne eksperymenty grudzien/analiza makro/aktywne makro/"
        + "stardist segmentation/" + pos + "_StarDist_segmentation_binary_2.tif");
    
    
    // Jeśli chcesz zamknąć obraz po każdej iteracji, odkomentuj poniższe polecenie:
    // close();
}
