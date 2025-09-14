// 7.
// previous: 6. makro_trackmate_mask
// Przerobi pliki posX_TrackMate_mask i zapisać jako posX_mask i to jest input dla tego makra
// teraz już ręczne poprawienie mixed planes i pomiar trackmatem

for (i = 1; i <= 6; i++) {
	pos = "pos" + i;
	slices = 34;
	
	//........................NALOZENIE MASKI NA PLANE 0 i 1........................
	open("C:/Users/3000000/Desktop/STUDIA/UJ/magisterka/glowne eksperymenty grudzien/analiza makro/aktywne makro/stardist segmentation/trackmate stardist/analiza/"+pos+"_mask.tif");
	selectImage(pos+"_mask.tif");
	open("C:/Users/3000000/Desktop/STUDIA/UJ/magisterka/glowne eksperymenty grudzien/analiza makro/aktywne makro/"+pos+"_timelaps_plane_0.tif");
	selectImage(pos+"_timelaps_plane_0.tif");
	open("C:/Users/3000000/Desktop/STUDIA/UJ/magisterka/glowne eksperymenty grudzien/analiza makro/aktywne makro/"+pos+"_timelaps_plane_1.tif");
	selectImage(pos+"_timelaps_plane_1.tif");
	imageCalculator("AND create stack", pos+"_mask.tif", pos+"_timelaps_plane_0.tif");
	selectImage("Result of "+pos+"_mask.tif");
	saveAs("Tiff", "C:/Users/3000000/Desktop/STUDIA/UJ/magisterka/glowne eksperymenty grudzien/analiza makro/aktywne makro/stardist segmentation/trackmate stardist/analiza/"+pos+"_plane_0.tif");
	
	imageCalculator("AND create stack", pos+"_mask.tif", pos+"_timelaps_plane_1.tif");
	selectImage("Result of "+pos+"_mask.tif");
	saveAs("Tiff", "C:/Users/3000000/Desktop/STUDIA/UJ/magisterka/glowne eksperymenty grudzien/analiza makro/aktywne makro/stardist segmentation/trackmate stardist/analiza/"+pos+"_plane_1.tif");
	run("Duplicate...", " ");
	selectImage(pos+"_plane_0.tif");
	run("Duplicate...", " ");
	selectImage(pos+"_timelaps_plane_1.tif");
	close;
	selectImage(pos+"_timelaps_plane_0.tif");
	close;
	selectImage(pos+"_mask.tif");
	close;
	
	//........................MIESZANE PLANE 0_1........................//
	run("Concatenate...", "open image1="+pos+"_plane_0-1.tif image2="+pos+"_plane_1-1.tif image3=[-- None --]");
	
	for(j=2; j<=slices; j++){
	selectImage(pos+"_plane_0.tif");
	run("Next Slice [>]");
	selectImage(pos+"_plane_1.tif");
	run("Next Slice [>]");
	
	selectImage(pos+"_plane_0.tif");
	run("Duplicate...", " ");
	selectImage(pos+"_plane_1.tif");
	run("Duplicate...", " ");
	run("Concatenate...", "  image1=Untitled image2="+pos+"_plane_0-1.tif image3="+pos+"_plane_1-1.tif image4=[-- None --]");
	}
	selectImage("Untitled");
	saveAs("Tiff", "C:/Users/3000000/Desktop/STUDIA/UJ/magisterka/glowne eksperymenty grudzien/analiza makro/aktywne makro/stardist segmentation/trackmate stardist/analiza/"+pos+"_plane_0_1.tif");
	selectImage(pos+"_plane_0.tif");
	close;
	selectImage(pos+"_plane_1.tif");
	close;
	
}