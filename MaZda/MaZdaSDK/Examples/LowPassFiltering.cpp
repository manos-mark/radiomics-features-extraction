//-------------------------------------------------------------------------------------
//
// LowPassFiltering.cpp 
// Copyright 2007 by Piotr M. Szczypinski
// Version 2007.03.18
//
// This is a sample module for MaZda software. The sample shows how to use MaZdaSDK
// classes to load image, create bufer of image and perform simple filtering. 
//
// Compile this sample and copy an executable file LowPassFilter.exe
// LowPassFiltering.plugin to the MaZda folder. 
// Run MaZda. The new menu option LowPassFiltering appears in the Tools.
// After you load any image to MaZda run the GrayScaleThresholding plugin by
// Clicking on Tools->LowPassFiltering. The plugin will save an image,
// run the sample module LowPassFiltering.exe and then will load resulting 
// regions.
//
// This sample was not inteded as a useful tool for image analysis.
// This is an example code only to show usage of IntImage class.
// This code was intended to be easy to understand, and it is not optimized. 
//
//-------------------------------------------------------------------------------------

#include "MaZdaSDK.h"

//-------------------------------------------------------------------------------------
int main(int argc, char* argv[])
{
	if(argc<=1)
	{
		printf("Error: Input file not specified.\r\n");
		return 1; 
	}

// Creates an image object and loads an image from the specified file
	IntImage* image = new IntImage(argv[1]);
	if(image == NULL) return 2;

// Creates an empty image of the same size as image.
	IntImage* buf = new IntImage(image->GetWidth(), image->GetHeight());
	if(buf == NULL) 
	{
		delete image;
		return 2;
	}

//Filters an image by averaging pixel's gray-scale within 5x5 window
	for(int y = 0; y < (int) image->GetHeight(); y++)
	for(int x = 0; x < (int) image->GetWidth(); x++)
	{
		int div = 0;
		int sum = 0;
		for(int dy = -2; dy <= 2; dy++)
		for(int dx = -2; dx <= 2; dx++)
		{
			int xx = x+dx;
			int yy = y+dy;
			if(xx<0 || yy<0 || xx>=image->GetWidth() || yy>=image->GetHeight()) continue;
			sum += image->GetPixel(xx, yy);
			div++;
		}
		if(div > 1) sum/=div;
		buf->SetPixel(x, y, (BYTE)sum);
	}

//Saves a filtered image to the file of the same name as an input file.
	buf->IntSave(argv[1]);
	

	delete buf;
	delete image;

	return 0;
}

