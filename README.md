# Radiomics Thesis Paper
*Radiomic data has the potential to uncover disease characteristics that fail to be appreciated by the naked eye. The central hypothesis of radiomics is that distinctive imaging algorithms quantify the state of diseases, and thereby provide valuable information for personalized medicine. Radiomics has emerged from oncology, but can be applied to other medical problems where a disease is imaged.* 

Read more [here](https://www.radiomics.io/). 

## 0.0 Radiomics workflow
In the `/notebooks` folder there is example code for some basic "how to use pyradiomics" and further analysis for radiomics workflow.

![alt text](https://healthcare-in-europe.com/media/story_section_image/3188/image-01-picture-radiomics-workflow.jpg)

## 1.0 Image Acquisition and Segmentation
  The data consist of two folders:
  - pyradiomics_data from [pyradiomics](https://github.com/Radiomics/pyradiomics/tree/master/data) project.
  - CT_medical_images from [kaggle](https://www.kaggle.com/kmader/siim-medical-images).
    - The dataset is designed to allow for different methods to be tested for examining the trends in CT image data associated with using contrast and patient age. The basic idea is to identify image textures, statistical patterns and features correlating strongly with these traits and possibly build simple tools for automatically classifying these images when they have been misclassified (or finding outliers which could be suspicious cases, bad measurements, or poorly calibrated machines).  
    - The data are a tiny subset of images from the cancer imaging archive. They consist of the middle slice of all CT images taken where valid age, modality, and contrast tags could be found. TCIA Archive Link - https://wiki.cancerimagingarchive.net/display/Public/TCGA-LUAD
  The images data is provided in DICOM format, named with a naming convention allowing us to identify some meta-data about the images.
  
## 2.0 Feature extraction 
  In this section we will focus on feature extraction from a single image or a batch of images. For this project our masks (ROI) are already segmented. Detailed description on feature classes and individual features is provided in section [Radiomic Features](https://pyradiomics.readthedocs.io/en/latest/features.html#radiomics-features-label) of the documentation.
  
  *On average, Pyradiomics extracts ≈1500 features per image, which consist of the 16 shape descriptors and features extracted from original and derived images (LoG with 5 sigma levels, 1 level of Wavelet decomposistions yielding 8 derived images and images derived using Square, Square Root, Logarithm and Exponential filters).*

## 3.0 Feature analysis

## 4.0 Model Building

## 5.0 Models Comparison
