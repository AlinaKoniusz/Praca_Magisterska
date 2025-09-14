// UWAGA NIESKOŃCZONE MAKRO
// 2.
// previous: 1. Macro_timelaps_pos_1-6
// next: 3. macro_stacks_pos_1-6
// 

for (i = 1; i <= 6; i++) {
    pos = "pos" + i;
	slice_1 = 39;
	slice_2 = 33;
	slice_3 = 15;
	slice_4 = 9;
	slice_5 = 1;
	
	//open("C:/Users/3000000/Desktop/STUDIA/UJ/magisterka/glowne eksperymenty grudzien/analiza makro/aktywne makro/"+pos+"_timelaps_plane_0.tif");
	//selectImage(pos+"_timelaps_plane_0.tif");
	//open("C:/Users/3000000/Desktop/STUDIA/UJ/magisterka/glowne eksperymenty grudzien/analiza makro/aktywne makro/"+pos+"_timelaps_plane_1.tif");
	//electImage(pos+"_timelaps_plane_1.tif");
	//selectImage(pos+"_StarDist_segmentation.tif");

	//selectImage(pos+"_StarDist_segmentation_binary_2.tif");
	setSlice(slice_1);
	run("Delete Slice");
	setSlice(slice_2);
	run("Delete Slice");
	setSlice(slice_3);
	run("Delete Slice");
	setSlice(slice_4);
	run("Delete Slice");
	setSlice(slice_5);
	run("Delete Slice");
	run("Save");
	close;
}