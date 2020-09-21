//-------------------------------------------------------------------------------------
//
// MaZdaSDK.cpp - Class library for writing MaZda plugins.
// Copyright 2007 by Piotr M. Szczypinski
// Version 2007.03.18
//
//-------------------------------------------------------------------------------------
#include "MaZdaSDK.h"


//=====================================================================================
//=====================================================================================
// 8-BIT GRAY-SCALE IMAGE CLASS 
//=====================================================================================
//=====================================================================================

//-------------------------------------------------------------------------------------
//Constructs 8-bit grey-scale image object from a bitmap file 
//(8-bit paletted or 24-bit RGB uncompressed bitmap implemented)
IntImage::IntImage(char* filename)
{
	BITMAPINFO *bih;
	void *bmp;
  FILE *plik;
  BITMAPFILEHEADER bfh;
  plik = fopen(filename, "rb");
	if (plik==NULL) {delete this; return;}
  fread(&bfh, sizeof(bfh), 1, plik);
  if(bfh.bfType!=0x4d42)
  {
    fclose(plik);
		delete this; return;
	}
  bih = (BITMAPINFO*) malloc(bfh.bfOffBits-sizeof(bfh));
	if(bih==NULL)
  {
    fclose(plik);
    delete this; return;
  }
	fread(bih, bfh.bfOffBits-sizeof(bfh), 1, plik);
	if((bih->bmiHeader.biBitCount!=8 && bih->bmiHeader.biBitCount!=24) || bih->bmiHeader.biCompression!=BI_RGB)
	{
		free(bih);
    fclose(plik);
    delete this; return;
  }
	Width = bih->bmiHeader.biWidth;
	Height = bih->bmiHeader.biHeight;

	int sz = ((Width*bih->bmiHeader.biBitCount+31)>>5)<<2;
	DWORD sizeim = Height*sz;
	bmp = malloc(sizeim);

	if(bmp==NULL)
  {
		free(bih);
    fclose(plik);
    delete this; return;
  }
  fread(bmp, sizeim, 1, plik);
  fclose(plik);

	Image8bit = (BYTE*)malloc(sizeof(BYTE)*Width*Height);
	if(Image8bit==NULL)
  {
		free(bih);
		free(bmp);
    delete this; return;
  }
	if(bih->bmiHeader.biBitCount==8)
	{
		for(unsigned int y = 0; y < Height; y++)
		{
			for(unsigned int x = 0; x < Width; x++)
			{
				BYTE index = *((BYTE*)bmp+sz*y+x);
				Image8bit[y*Width+x] = (((int)114*(int)bih->bmiColors[index].rgbBlue
																	+(int)587*(int)bih->bmiColors[index].rgbGreen
																	+(int)299*(int)bih->bmiColors[index].rgbRed
																	)/1000);
			}
		}
	}
	else if(bih->bmiHeader.biBitCount==24)
	{
		for(unsigned int y = 0; y < Height; y++)
		{
			for(unsigned int x = 0; x < Width; x++)
			{
				Image8bit[y*Width+x] = (((int)114*(int)*((BYTE*)bmp+sz*y+3*x)
																	+(int)587*(int)*((BYTE*)bmp+sz*y+3*x+1)
																	+(int)299*(int)*((BYTE*)bmp+sz*y+3*x+2)
																	)/1000);
			}
		}
	}
	free(bih);
	free(bmp);
};

//-------------------------------------------------------------------------------------
//Constructs black width x height, 8-bit, grey-scale image object
IntImage::IntImage(unsigned int width, unsigned int height)
{
	Width = width;
	Height = height;
	Image8bit = (BYTE*)malloc(sizeof(BYTE)*Width*Height);
	if(Image8bit==NULL)
  {
    delete this; return;
  }
	ZeroMemory(Image8bit, sizeof(BYTE)*Width*Height); 
};

//-------------------------------------------------------------------------------------
//Destructs 8-bit grey-scale image object. Frees memory. 
IntImage::~IntImage()
{
	free(Image8bit);
	Image8bit = NULL;
	Width = 0;
	Height = 0;
}

//-------------------------------------------------------------------------------------
//Gets pixel intensity. 
BYTE IntImage::GetPixel(unsigned int x, unsigned int y)
{
	if(Image8bit == NULL) return 0;
	if (x>=Width || y>=Height) return 0;
	return Image8bit[y*Width+x];
}
	
//-------------------------------------------------------------------------------------
//Sets pixel intensity. 
void IntImage::SetPixel(unsigned int x, unsigned int y, BYTE intensity)
{
	if(Image8bit == NULL) return;
	if (x>=Width || y>=Height) return;
	Image8bit[y*Width+x] = intensity;
}

//-------------------------------------------------------------------------------------
//Saves image into the bitmap file (8-bit paletted uncompressed bitmap).
int IntImage::IntSave(char* filename)
{
  HANDLE plik;
  plik=CreateFile(filename, GENERIC_WRITE, 0, NULL,
                CREATE_ALWAYS, FILE_ATTRIBUTE_NORMAL, NULL);
	if(plik==NULL) return 0;

	BITMAPINFOHEADER bih;
  BITMAPFILEHEADER bfh;
	BYTE linia[16];
  int szer;
  DWORD z;
  RGBQUAD plt[256];

  ZeroMemory(&bih, sizeof(BITMAPINFOHEADER));
  ZeroMemory(&bfh, sizeof(BITMAPFILEHEADER));

  szer=(((Width)+3)>>2)<<2;
  bih.biSize=sizeof(bih);
  bih.biWidth=Width;
  bih.biHeight=Height;
  bih.biPlanes=1;
  bih.biBitCount=8;
  bih.biCompression=BI_RGB;
  bih.biSizeImage=szer*Height;
  bih.biXPelsPerMeter=1000;
  bih.biYPelsPerMeter=1000;
  bih.biClrUsed=0;
  bih.biClrImportant=0;

  bfh.bfType=0x4d42;
  bfh.bfReserved1=0;
  bfh.bfReserved2=0;

  bfh.bfOffBits=sizeof(bfh)+sizeof(bih)+256*sizeof(RGBQUAD);
  bfh.bfSize=bfh.bfOffBits+bih.biSizeImage;
  WriteFile(plik, &bfh, sizeof(bfh), &z, NULL);
  WriteFile(plik, &bih, sizeof(bih), &z, NULL);

  for(int p=0; p<256; p++)
  {
    plt[p].rgbBlue = (BYTE)p;
    plt[p].rgbGreen = (BYTE)p;
    plt[p].rgbRed = (BYTE)p;
    plt[p].rgbReserved = 0;
  }
  WriteFile(plik, plt, 256*sizeof(RGBQUAD), &z, NULL);
  ZeroMemory(linia, 16);
	int dodaj = szer-Width;
	if(dodaj>0)	for(unsigned int y=0; y<Height; y++)
  {
   	WriteFile(plik, Image8bit+(Width*y), Width, &z, NULL);
   	WriteFile(plik, linia, dodaj, &z, NULL);
  }
	else for(unsigned int y=0; y<Height; y++)
  {
   	WriteFile(plik, Image8bit+(Width*y), Width, &z, NULL);
  }
	CloseHandle(plik);
	return 1;
}

//-------------------------------------------------------------------------------------
//Returns width of the image object. 
unsigned int IntImage::GetWidth(void)
{
	return Width;
}
//-------------------------------------------------------------------------------------
//Returns height of the image object. 
unsigned int IntImage::GetHeight(void)
{
	return Height;
}

//=====================================================================================
//=====================================================================================
// FLOATING POINT 32-BIT GRAY-SCALE IMAGE CLASS 
//=====================================================================================
//=====================================================================================



//=====================================================================================
//=====================================================================================
// REGION OF INTEREST 16-BIT MASK CLASS 
//=====================================================================================
//=====================================================================================

//Predefined ROI colors
RGBQUAD RoiColors[16]=
  {
		{0x00, 0x00, 0xff, 0x00}, 
		{0x00, 0xff, 0x00,0x00},
		{0xff, 0x00, 0x00,0x00},
		{0xff, 0xff, 0x00, 0x00},
		{0xff, 0x00, 0xff, 0x00},
		{0x00, 0xff, 0xff, 0x00}, 
		{0x00, 0x80, 0xFF, 0x00}, 
		{0x80, 0x00, 0xFF, 0x00},
		{0x00, 0xFF, 0x80, 0x00},
		{0x80, 0xFF, 0x00, 0x00},
		{0xFF, 0x00, 0x80, 0x00},
		{0xFF, 0x80, 0x00, 0x00},
		{0x00, 0xC4, 0xFF, 0x00},
		{0x00, 0xFF, 0xC4, 0x00},
		{0xFF, 0x00, 0xC4, 0x00},
		{0xC4, 0xFF, 0x00, 0x00}
  };

//-------------------------------------------------------------------------------------
//Constructs ROI from a file 
//(8-bit paletted bitmap, 24-bit RGB uncompressed bitmap and roi format implemented)
RoiImage::RoiImage(char* filename)
{
	char *token;
	token = strrchr(filename, '.');
	if(token)
	{				
		if(stricmp(token, ".bmp")==0)
		{
			if(!LoadRoiFromBmp(filename))
			{
				Roi16bit = NULL;
				Width = 0;
				Height = 0;
				delete this;
			}
		}
		if(stricmp(token, ".roi")==0)
		{
			if(!LoadRoiFromRoi(filename))
			{
				Roi16bit = NULL;
				Width = 0;
				Height = 0;
				delete this;
			}
		}
		else 
		{
			Roi16bit = NULL;
			Width = 0;
			Height = 0;
			delete this;
		}
	}
	else 
	{
		Roi16bit = NULL;
		Width = 0;
		Height = 0;
		delete this;
	}
};
//-------------------------------------------------------------------------------------
//Constructs empty ROI width x height
RoiImage::RoiImage(unsigned int width, unsigned int height)
{
	Width = width;
	Height = height;
	Roi16bit = (WORD*)malloc(sizeof(WORD)*Width*Height);
	if(Roi16bit==NULL)
  {
    delete this; return;
  }
	ZeroMemory(Roi16bit, sizeof(WORD)*Width*Height); 
};
//-------------------------------------------------------------------------------------
//Loads ROI from color bitmap file 
//(8-bit paletted or 24-bit RGB uncompressed bitmap implemented. Only non-overl.)
int RoiImage::LoadRoiFromBmp(char* filename)
{
	BITMAPINFO *bih;
	void *bmp;
  FILE *plik;
  BITMAPFILEHEADER bfh;
  plik = fopen(filename, "rb");
	if (plik==NULL) {return 0;}
  fread(&bfh, sizeof(bfh), 1, plik);
  if(bfh.bfType!=0x4d42)
  {
    fclose(plik);
		return 0;
	}
  bih = (BITMAPINFO*) malloc(bfh.bfOffBits-sizeof(bfh));
	if(bih==NULL)
  {
    fclose(plik);
    return 0;
  }
	fread(bih, bfh.bfOffBits-sizeof(bfh), 1, plik);
	if((bih->bmiHeader.biBitCount!=8 && bih->bmiHeader.biBitCount!=24) || bih->bmiHeader.biCompression!=BI_RGB)
	{
		free(bih);
    fclose(plik);
    return 0;
  }
	Width = bih->bmiHeader.biWidth;
	Height = bih->bmiHeader.biHeight;

	int sz = ((Width*bih->bmiHeader.biBitCount+31)>>5)<<2;
	DWORD sizeim = Height*sz;
	bmp = malloc(sizeim);

	if(bmp==NULL)
  {
		free(bih);
    fclose(plik);
    return 0;
  }
  fread(bmp, sizeim, 1, plik);
  fclose(plik);

	Roi16bit = (WORD*)malloc(sizeof(WORD)*Width*Height);
	if(Roi16bit==NULL)
  {
		free(bih);
		free(bmp);
    return 0;
  }
	if(bih->bmiHeader.biBitCount==8)
	{
		for(unsigned int y = 0; y < Height; y++)
		{
			for(unsigned int x = 0; x < Width; x++)
			{
				RGBQUAD rgb = bih->bmiColors[*((BYTE*)bmp+sz*y+x)];
				for(int roi = 0; roi < 16; roi++)
				{
					if(*(DWORD*)&RoiColors[roi] == *(DWORD*)&rgb)
					{
						Roi16bit[y*Width+x] = (WORD)1 << roi;
						continue;
					}
				}
			}
		}
	}
	else if(bih->bmiHeader.biBitCount==24)
	{
		for(unsigned int y = 0; y < Height; y++)
		{
			for(unsigned int x = 0; x < Width; x++)
			{
				RGBQUAD rgb;
				rgb.rgbBlue = *((BYTE*)bmp+sz*y+3*x);
				rgb.rgbGreen = *((BYTE*)bmp+sz*y+3*x+1);
				rgb.rgbRed = *((BYTE*)bmp+sz*y+3*x+2);
				rgb.rgbReserved = 0;
				for(int roi = 0; roi < 16; roi++)
				{
					if(*(DWORD*)&RoiColors[roi] == *(DWORD*)&rgb)
					{
						Roi16bit[y*Width+x] = (WORD)1 << roi;
						continue;
					}
				}
			}
		}
	}
	free(bih);
	free(bmp);
  for(int k=0; k<16; k++)
  {
    classnames[k][0]=0;
  }
	return 1;
};

//-------------------------------------------------------------------------------------
//Loads ROI from ROI format file 
int RoiImage::LoadRoiFromRoi(char* filename)
{
  HANDLE plik;
  DWORD z;
  PMS_ROI_2001 header;
  for(int k=0; k<32; k++) header.reserved[k] = 0;
  plik=CreateFile(filename, GENERIC_READ, 0, NULL,
                OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, NULL);
  if(plik==NULL) return 0;
  ReadFile(plik, &header, sizeof(header), &z, NULL);
  if(strncmp(header.magic, "PMS_ROI_2001", 12)) 
	{
		CloseHandle(plik); 
		return 0;
	}
	Roi16bit = (WORD*)malloc(sizeof(WORD)*Width*Height);
	if(Roi16bit==NULL)
	{
		CloseHandle(plik); 
		return 0;
	}

	for(int line = Height-1; line>=0; line--)
		ReadFile(plik, Roi16bit+header.xmax*line, header.xmax*sizeof(WORD), &z, NULL);
//  SetFilePointer(plik, sizeof(header)+(DWORD)header.xmax*header.ymax*sizeof(WORD), 0, FILE_BEGIN);
  for(int k=0; k<16; k++)
  if(header.roi_text_length[k]>0 && header.roi_text_length[k]<1023)
  {
    ReadFile(plik, classnames[k], header.roi_text_length[k], &z, NULL);
    classnames[k][header.roi_text_length[k]]=0;
  }
	else
  {
    classnames[k][0]=0;
  }
  CloseHandle(plik);
	return 1;
}

//-------------------------------------------------------------------------------------
//Destructs ROI object. Frees memory. 
RoiImage::~RoiImage()
{
	free(Roi16bit);
	Roi16bit = NULL;
	Width = 0;
	Height = 0;
}

//-------------------------------------------------------------------------------------
//Gets pixel intensity. 
WORD RoiImage::GetPixel(unsigned int x, unsigned int y)
{
	if(Roi16bit == NULL) return 0;
	if (x>=Width || y>=Height) return 0;
	return Roi16bit[y*Width+x];
}
//-------------------------------------------------------------------------------------
//Sets pixel intensity. 
void RoiImage::SetPixel(unsigned int x, unsigned int y, WORD allroi)
{
	if(Roi16bit == NULL) return;
	if (x>=Width || y>=Height) return;
	Roi16bit[y*Width+x] = allroi;
}
//-------------------------------------------------------------------------------------
//Saves ROI to a disk file.
int RoiImage::RoiSave(char* filename)
{
	char *token;
	token = strrchr(filename, '.');
	if(token)
	{				
		if(stricmp(token, ".bmp")==0)
		{
			return RoiSaveAsBmp(filename);
		}
		if(stricmp(token, ".roi")==0)
		{
			return RoiSaveAsRoi(filename);
		}
	}
	return 0;
}
//-------------------------------------------------------------------------------------
//Saves ROI to a bitmap file.
int RoiImage::RoiSaveAsBmp(char* filename)
{
  HANDLE plik;
  int error = 0;
  plik=CreateFile(filename, GENERIC_WRITE, 0, NULL,
                CREATE_ALWAYS, FILE_ATTRIBUTE_NORMAL, NULL);
  if(plik!=NULL)
  {
    BITMAPINFOHEADER bih;
    BITMAPFILEHEADER bfh;
    int szer;
    DWORD z;
    RGBQUAD plt[256];

    ZeroMemory(&bih, sizeof(BITMAPINFOHEADER));
    ZeroMemory(&bfh, sizeof(BITMAPFILEHEADER));

    szer=(((Width)+3)>>2)<<2;
    bih.biSize=sizeof(bih);
    bih.biWidth=Width;
    bih.biHeight=Height;
    bih.biPlanes=1;
    bih.biBitCount=8;
    bih.biCompression=BI_RGB;
    bih.biSizeImage=szer*Height;
    bih.biXPelsPerMeter=1000;
    bih.biYPelsPerMeter=1000;
    bih.biClrUsed=0;
    bih.biClrImportant=0;

    bfh.bfType=0x4d42;
    bfh.bfReserved1=0;
    bfh.bfReserved2=0;

    bfh.bfOffBits=sizeof(bfh)+sizeof(bih)+256*sizeof(RGBQUAD);
    bfh.bfSize=bfh.bfOffBits+bih.biSizeImage;
    WriteFile(plik, &bfh, sizeof(bfh), &z, NULL);
    WriteFile(plik, &bih, sizeof(bih), &z, NULL);
    int p=0;
    {
      plt[p].rgbBlue=0;
      plt[p].rgbGreen=0;
      plt[p].rgbRed=0;
      plt[p].rgbReserved=0;
    }
    for(p=1; p<17; p++)
    {
      plt[p].rgbBlue=RoiColors[p-1].rgbBlue;
      plt[p].rgbGreen=RoiColors[p-1].rgbGreen;
      plt[p].rgbRed=RoiColors[p-1].rgbRed;
      plt[p].rgbReserved=RoiColors[p-1].rgbReserved;
    }
    for(p=17; p<256; p++)
    {
      plt[p].rgbBlue=(BYTE)p;
      plt[p].rgbGreen=(BYTE)p;
      plt[p].rgbRed=(BYTE)p;
      plt[p].rgbReserved=0;
    }
    WriteFile(plik, plt, 256*sizeof(RGBQUAD), &z, NULL);
    BYTE* linia = new	BYTE[szer];
    ZeroMemory(linia, szer);
    for(unsigned int y=0; y<Height; y++)
    {
			WORD* pwtmp = Roi16bit + y*Width;
			BYTE* pbtmp = linia;

			for(unsigned int x=0; x<Width; x++)
  	  {
				WORD roi = *pwtmp;
				switch(*pwtmp)
				{
					case 0x0001: *pbtmp = 1; break;
					case 0x0002: *pbtmp = 2; break;
					case 0x0004: *pbtmp = 3; break;
					case 0x0008: *pbtmp = 4; break;
					case 0x0010: *pbtmp = 5; break;
					case 0x0020: *pbtmp = 6; break;
					case 0x0040: *pbtmp = 7; break;
					case 0x0080: *pbtmp = 8; break;
					case 0x0100: *pbtmp = 9; break;
					case 0x0200: *pbtmp =10; break;
					case 0x0400: *pbtmp =11; break;
					case 0x0800: *pbtmp =12; break;
					case 0x1000: *pbtmp =13; break;
					case 0x2000: *pbtmp =14; break;
					case 0x4000: *pbtmp =15; break;
					case 0x8000: *pbtmp =16; break;
					default: *pbtmp = 0;
				}
				pbtmp++;
				pwtmp++;
      }
   	  WriteFile(plik, linia, szer, &z, NULL);
    }
    delete[] linia;
	  CloseHandle(plik);
		return 1;
  }
	return 0;
}
//-------------------------------------------------------------------------------------
//Saves ROI to a roi format file.
int RoiImage::RoiSaveAsRoi(char* filename)
{
  HANDLE plik;
  plik=CreateFile(filename, GENERIC_WRITE, 0, NULL,
                CREATE_ALWAYS, FILE_ATTRIBUTE_NORMAL, NULL);
	if(plik==NULL) return 0;

  DWORD z;
  PMS_ROI_2001 header;
  strcpy(header.magic,"PMS_ROI_2001");
  header.xmax = Width;
  header.ymax = Height;
  header.roi_text_length[0] = (WORD)strlen(classnames[0]);
  header.roi_text_length[1] = (WORD)strlen(classnames[1]);
  header.roi_text_length[2] = (WORD)strlen(classnames[2]);
  header.roi_text_length[3] = (WORD)strlen(classnames[3]);
  header.roi_text_length[4] = (WORD)strlen(classnames[4]);
  header.roi_text_length[5] = (WORD)strlen(classnames[5]);
  header.roi_text_length[6] = (WORD)strlen(classnames[6]);
  header.roi_text_length[7] = (WORD)strlen(classnames[7]);
  header.roi_text_length[8] = (WORD)strlen(classnames[8]);
  header.roi_text_length[9] = (WORD)strlen(classnames[9]);
  header.roi_text_length[10] = (WORD)strlen(classnames[10]);
  header.roi_text_length[11] = (WORD)strlen(classnames[11]);
  header.roi_text_length[12] = (WORD)strlen(classnames[12]);
  header.roi_text_length[13] = (WORD)strlen(classnames[13]);
  header.roi_text_length[14] = (WORD)strlen(classnames[14]);
  header.roi_text_length[15] = (WORD)strlen(classnames[15]);
	for(int k=0; k<32; k++) header.reserved[k] = 0;
  WriteFile(plik, &header, sizeof(header), &z, NULL);

	for(int line = Height-1; line>=0; line--)
	  WriteFile(plik, Roi16bit+Width*line, (DWORD)Width*sizeof(WORD), &z, NULL);
  for(int k=0; k<16; k++)
		WriteFile(plik, classnames[k], header.roi_text_length[k], &z, NULL);
  CloseHandle(plik);
	return 1;
}
//-------------------------------------------------------------------------------------
//Returns width of the image object. 
unsigned int RoiImage::GetWidth(void)
{
	return Width;
}
//-------------------------------------------------------------------------------------
//Returns height of the image object. 
unsigned int RoiImage::GetHeight(void)
{
	return Height;
}
//-------------------------------------------------------------------------------------
//Returns true if pixel x, y belongs to roinumber roi, or false otherwise. 
bool RoiImage::IsRoi(unsigned int x, unsigned int y, BYTE roinumber)
{
	if(roinumber>=16) return false;
	WORD mask = GetPixel(x, y);	
	if((mask&((WORD)1<<roinumber)) != 0) return true;
	return false;
}
//-------------------------------------------------------------------------------------
//Assigns a pixel x, y to roinumber roi. 
void RoiImage::SetRoi(unsigned int x, unsigned int y, BYTE roinumber)
{
	if(roinumber>=16) return;
	WORD mask = GetPixel(x, y);
	mask |= ((WORD)1<<roinumber);
	SetPixel(x, y, mask);
}
//-------------------------------------------------------------------------------------
//Removes a pixel x, y from roinumber roi. 
void RoiImage::ClearRoi(unsigned int x, unsigned int y, BYTE roinumber)
{
	if(roinumber>=16) return;
	WORD mask = GetPixel(x, y);
	mask &= (~((WORD)1<<roinumber));
	SetPixel(x, y, mask);
}
//-------------------------------------------------------------------------------------
//Removes a pixel x, y from all rois. 
void RoiImage::ClearAll(unsigned int x, unsigned int y)
{
	SetPixel(x, y, 0);
}
//-------------------------------------------------------------------------------------
// Sets a classname for roi. 
int RoiImage::SetClassName(BYTE roi, char* classname)
{
	if(roi>=16) return 0;
	strncpy(classnames[roi], classname, 1023);
	classnames[roi][1023] = 0;
	return 1;
}
//-------------------------------------------------------------------------------------
// Gets a classname for roi. 
int RoiImage::GetClassName(char* buffer, int buffersize, BYTE roi)
{
	if(roi>=16) return 0;
	int copied = (1023<buffersize-1 ?1023 :buffersize-1);
	strncpy(buffer, classnames[roi], copied);
	buffer[copied] = 0;
	return copied;
}
