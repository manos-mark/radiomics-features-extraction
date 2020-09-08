//-------------------------------------------------------------------------------------
//
// GrayScaleThresholding.cpp 
// Copyright 2007 by Piotr M. Szczypinski
// Version 2007.03.18
//
// This is a sample module for MaZda software. The sample shows how to use MaZdaSDK
// classes to load image, create regions of interest based on grey-scale image 
// thresholding and how to save regions of interest to a file.
//
// Compile this sample and copy an executable file GrayScaleThresholding.exe
// GrayScaleThresholding.plugin to the MaZda folder. 
// Run MaZda. The new menu option GrayScaleThresholding appears in the Tools.
// After you load any image to MaZda run the GrayScaleThresholding plugin by
// Clicking on Tools->GrayScaleThresholding. The plugin will save an image,
// run the sample module GrayScaleThresholding.exe and then will load resulting 
// regions.
//
// This sample was not inteded as a useful tool for image analysis.
// This is an example code only to show usage of IntImage and RoiImage classes.
// This code was intended to be easy to understand and it is not optimized. 
//
//-------------------------------------------------------------------------------------

#include "MaZdaSDK.h"
const BYTE grayscalethreshold = 128;
const int max_stack = 0x4000;
DWORD stack[max_stack];

//-------------------------------------------------------------------------------------
#define ffpop(x, y)\
    {\
      if(stackPointer > 0)\
      {\
        unsigned int p = stack[stackPointer];\
        x = p & 0xffff;\
        y = ((p >> 16) & 0xffff);\
        stackPointer--;\
      }\
      else return area;\
    };

#define ffpush(x, y)\
		{\
      if(stackPointer < max_stack - 1)\
      {\
        stackPointer++;\
        stack[stackPointer] = ((x) | ((y) << 16));\
      }\
      else return area;\
		};


//-------------------------------------------------------------------------------------
int FillIn(WORD xp, WORD yp, IntImage* image, RoiImage* roi, BYTE region)
{
 	int stackPointer;
	int area = 0;
	if(roi->GetPixel(xp, yp)!=0) return 0;
	if(image->GetPixel(xp, yp)<=grayscalethreshold) return 0;
  stackPointer = 0;
	ffpush (xp, yp);

	while(true)
  {
		WORD y, x;
    ffpop (x, y);
		roi->SetRoi(x, y, region);
		if(x > 0)
			if(image->GetPixel(x-1, y)>grayscalethreshold && roi->GetPixel(x-1, y)==0) ffpush (x-1, y);
    if(y > 0) 
			if(image->GetPixel(x, y-1)>grayscalethreshold && roi->GetPixel(x, y-1)==0) ffpush (x, y-1);
		if(x < image->GetWidth())
			if(image->GetPixel(x+1, y)>grayscalethreshold && roi->GetPixel(x+1, y)==0) ffpush (x+1, y);
		if(y < image->GetHeight()) 
			if(image->GetPixel(x, y+1)>grayscalethreshold && roi->GetPixel(x, y+1)==0) ffpush (x, y+1);
		area++;
  }
}

//-------------------------------------------------------------------------------------
WORD Segment(IntImage* image, RoiImage* roi)
{
	BYTE region = 0;

	for(unsigned int y=0; y<image->GetHeight(); y++)
	for(unsigned int x=0; x<image->GetWidth(); x++)
	{
		if(FillIn(x, y, image, roi, region)>0)
		{
			region++;
		}
		if(region>=16) return region;
	}
	return region;
}

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

// Creates an empty object defining up to 16 ROIs.
// Dimensions of a ROI image is the same as dimensions of the loaded image.
	RoiImage* roi = new RoiImage(image->GetWidth(), image->GetHeight());
	if(roi == NULL) 
	{
		delete image;
		return 2;
	}

// Segments an image. 
// It thresholds image at a given 'grayscalethreshold' and then searches 
// for maximum 16 regions that are lighter then the threshold.
	Segment(image, roi);

// Saves regions to the file. The same file name is used as for 
// the input file. Thus, the input file is overwritten.
	roi->RoiSave(argv[1]);

//Defines class names 
	for(int r=0; r<8; r++)
		roi->SetClassName(r, "FirstEightSamples");
	for(int r=8; r<16; r++)
		roi->SetClassName(r, "LastEightSamples");

//Saves regions to the ROI format file. The defined classnames are saved in this format.
	char* filename = (char*)malloc(sizeof(char)*strlen(argv[1])+8);
	strcpy(filename, argv[1]);
	strcat(filename, ".roi");
	roi->RoiSave(filename);
	free(filename);

//Frees memory allocated for image and roi objects.
	delete roi;
	delete image;
	return 0;
}

