// 4.
// previous: 3. macro_stacks_pos_1-6
// next: 5. stardist_binary
// Po zmienieniu gammy i gausa wrzuca do stardista żeby znaleźć jądra

// Makro powtarzające sekwencję X razy
for (i = 1; i <= 6; i++) {
    // Zmienna oznaczająca aktualną pozycję
    pos = "pos" + i;
    
    // Jeśli obraz nie jest otwarty, można go otworzyć (odkomentować i ustawić właściwą ścieżkę):
    open("C:/Users/3000000/Desktop/STUDIA/UJ/magisterka/glowne eksperymenty grudzien/analiza makro/aktywne makro/" + pos + "_timelaps_plane_0_add_1_gamma_gaus.tif");
    
    // Wybieramy (lub otwieramy) plik, który chcemy przetworzyć
    selectImage(pos + "_timelaps_plane_0_add_1_gamma_gaus.tif");
    
    run("Duplicate...", "use");
    run("Concatenate...", 
        "title=" + pos + "_timelaps " +
        "keep " +
        "image1=[c:1/3 t:1/13 - " + pos + "_control] " +
        "image2=" + pos + "_timelaps_plane_0_add_1_gamma_gaus.tif");
    
    run("Properties...", 
    //UWAGA FRAMES
        "channels=1 slices=1 frames=64 " + ///frames +1 (bo dublujemy 1. frame)
        "pixel_width=0.4814711 pixel_height=0.4814711 voxel_depth=1.0000000 " +
        "frame=[300.01 sec]");
    
    saveAs("Tiff", 
        "C:/Users/3000000/Desktop/STUDIA/UJ/magisterka/glowne eksperymenty grudzien/analiza makro/aktywne makro/" + pos + "_timelaps.tif");
    close;
    
    open("C:/Users/3000000/Desktop/STUDIA/UJ/magisterka/glowne eksperymenty grudzien/analiza makro/aktywne makro/" + pos + "_timelaps.tif");
    selectImage(pos + "_timelaps.tif");
    
    run("Command From Macro", 
        "command=[de.csbdresden.stardist.StarDist2D], " +
        "args=['input':'" + pos + "_timelaps.tif', " +
              "'modelChoice':'Versatile (fluorescent nuclei)', " +
              "'normalizeInput':'true', " +
              "'percentileBottom':'1.0', " +
              "'percentileTop':'99.0', " +
              "'probThresh':'0.3', " +
              "'nmsThresh':'0.15', " +
              "'outputType':'Label Image', " +
              "'nTiles':'1', " +
              "'excludeBoundary':'2', " +
              "'roiPosition':'Automatic', " +
              "'verbose':'false', " +
              "'showCsbdeepProgress':'false', " +
              "'showProbAndDist':'false'], " +
        "process=[false]");

    // Po zakończeniu StarDist 2D pojawia się obraz o nazwie "Label Image"
    selectImage("Label Image");
    
    saveAs("Tiff", 
        "C:/Users/3000000/Desktop/STUDIA/UJ/magisterka/glowne eksperymenty grudzien/analiza makro/aktywne makro/stardist segmentation/" + pos + "_StarDist_segmentation.tif");
    close;
    
    open("C:/Users/3000000/Desktop/STUDIA/UJ/magisterka/glowne eksperymenty grudzien/analiza makro/aktywne makro/stardist segmentation/" + pos + "_StarDist_segmentation.tif");
    selectImage(pos + "_StarDist_segmentation.tif");
    
    run("RGB Color");
    run("Save");
    
    // Można dodać dodatkowe instrukcje, np. zamykanie bieżących obrazów, jeśli nie chcemy ich trzymać w pamięci
    // close;
}

