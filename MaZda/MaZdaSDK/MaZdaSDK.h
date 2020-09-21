//-------------------------------------------------------------------------------------
//
// MaZdaSDK.h - Header of class library for writing MaZda plugins.
// Copyright 2007 by Piotr M. Szczypinski
// Version 2007.03.18
//
//-------------------------------------------------------------------------------------

#include <stdio.h>
#include <string.h>
#include <windows.h>
#include <math.h>



//Class of MaZda grey-scale image. Pixel is given by 8-bit integer number.
//Functions to use:
//	IntImage(int width, int height); - creates black width x height image.
//	IntImage(char* filename); - creates and loads image from a file of a given filename.
//														Accepts only Windows bitmap (*.bmp) files in current version.
//	~IntImage(); - closes an image.
//	int ReadPixel(int x, int y); - returns grey level of a pixel at x, y coordinates. 
//																Negative value indicates an error. 
//	void WritePixel(int x, int y, unsigned char intensity); 
//                               - sets grey level of a pixel at x, y coordinates. 
//																Does nothing if coordinates are out of range.
class IntImage
{
public:
	IntImage(unsigned int width, unsigned int height);
	IntImage(char* filename);
	~IntImage();
	BYTE GetPixel(unsigned int x, unsigned int y);
	void SetPixel(unsigned int x, unsigned int y, BYTE intensity);
	int IntSave(char* filename);
	unsigned int GetWidth(void);
	unsigned int GetHeight(void);
private:
	unsigned int Width;
	unsigned int Height;
	BYTE* Image8bit; 
};
//Class of MaZda grey-scale image. Pixel is given by a 32-bit floating point number.
//Functions to use:

//	FloImage(int width, int height); - creates width x height image of all zeros. 
//	FloImage(char* filename); - creates and loads image from a file of a given filename.
//														Accepts only only BMF (*.bmf) files in current version.
//	FloSave(char* filename); - saves current image to a file of a given filename.
//														Accepts only BMF (*.bmf) files in current version.
//	~FloImage(); - closes an image.
//	float ReadPixel(int x, int y); - returns grey level of a pixel at x, y coordinates. 
//																HUGE_VAL value indicates an error. 
//	void WritePixel(int x, int y, float intensity); - sets grey level of a pixel at x, y coordinates. 
//																Does nothing if coordinates are out of range.
/*
class FloImage
{
public:
	FloImage(int width, int height);
	FloImage(char* filename);
	~FloImage();
	float GetPixel(unsigned int x, unsigned int y);
	void SetPixel(unsigned int x, unsigned int y, float intensity);
	unsigned int GetWidth(void);
	unsigned int GetHeight(void);
private:
	unsigned int Width;
	unsigned int Height;
	float* Image32bitfloat; 
};
*/
//Class of MaZda region-of-interest mask. Pixel is given by 16-bit integer number, 
//Each bit represents one of regions. If a bit is 1 region exists, if 0 there is no region.
//Functions to use:
//	RoiImage(int width, int height); - creates black, width x height image.
//	RoiImage(char* filename); - creates and loads image from a file of a given filename.
//	RoiSave(char* filename); - saves current image to a file of a given filename.
//														Accepts only ROI (*.roi) files for overlaping and non-overlaping regions
//														or Windows bitmaps (*.bmp). 
//														No overlaping regions nor class names are saved in Windows bitmaps.
//	~RoiImage(); - closes an image.
//	int ReadPixel(int x, int y); - returns grey level of a pixel at x, y coordinates. 
//																Negative value indicates an error. 
//	void WritePixel(int x, int y); - sets grey level of a pixel at x, y coordinates. 
//																Does nothing if coordinates are out of range.
//	bool IsRoi(int x, int y, int roinumber); - returns true if a pixel of given coordinates x, y
//																							belongs to ROI of a number roinumber
//	void SetRoi(int x, int y, int roi); - adds pixel of given coordinates x, y
//																							to a given ROI
//	void ClearRoi(int x, int y, int roi); - removes pixel of given coordinates x, y
//																							from a given ROI 
//	void ClearAll(int x, int y); - removes pixel of given coordinates x, y from all the ROIs
//	SetClassName(int roi, char* classname); - defines a class name for a given ROI.

struct PMS_ROI_2001
{
  char magic[12];
  WORD xmax;
  WORD ymax;
  WORD roi_text_length[16];
  WORD reserved[32];
};

class RoiImage
{
public:
	RoiImage(unsigned int width, unsigned int height);
	RoiImage(char* filename);
	~RoiImage();
	WORD GetPixel(unsigned int x, unsigned int y);
	void SetPixel(unsigned int x, unsigned int y, WORD allroi);
	bool IsRoi(unsigned int x, unsigned int y, BYTE roinumber);
	void SetRoi(unsigned int x, unsigned int y, BYTE roinumber);
	void ClearRoi(unsigned int x, unsigned int y, BYTE roinumber);
	void ClearAll(unsigned int x, unsigned int y);
	int SetClassName(BYTE roi, char* classname);
	int GetClassName(char* buffer, int buffersize, BYTE roi);
	unsigned int GetWidth(void);
	unsigned int GetHeight(void);
	int RoiSave(char* filename);

private:
	int LoadRoiFromBmp(char* filename);
	int LoadRoiFromRoi(char* filename);
	int RoiSaveAsBmp(char* filename);
	int RoiSaveAsRoi(char* filename);

	char classnames[16][1024];
	unsigned int Width;
	unsigned int Height;
	WORD* Roi16bit; 
};