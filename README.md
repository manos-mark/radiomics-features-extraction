# Radiomics Thesis Paper
Radiomic data has the potential to uncover disease characteristics that fail to be appreciated by the naked eye. The central hypothesis of radiomics is that distinctive imaging algorithms quantify the state of diseases, and thereby provide valuable information for personalized medicine. Radiomics has emerged from oncology, but can be applied to other medical problems where a disease is imaged. 

## Radiomics workflow
![alt text](https://ars.els-cdn.com/content/image/1-s2.0-S0360301619301786-gr1.jpg)

## Data 
  The example data files consist of two folders:
  - pyradiomics_data from [pyradiomics](https://github.com/Radiomics/pyradiomics/tree/master/data) project.
  - CT_medical_images from [kaggle](https://www.kaggle.com/kmader/siim-medical-images).
    - The dataset is designed to allow for different methods to be tested for examining the trends in CT image data associated with using contrast and patient age. The basic idea is to identify image textures, statistical patterns and features correlating strongly with these traits and possibly build simple tools for automatically classifying these images when they have been misclassified (or finding outliers which could be suspicious cases, bad measurements, or poorly calibrated machines).  
    - The data are a tiny subset of images from the cancer imaging archive. They consist of the middle slice of all CT images taken where valid age, modality, and contrast tags could be found. TCIA Archive Link - https://wiki.cancerimagingarchive.net/display/Public/TCGA-LUAD
  The images data is provided in DICOM format, named with a naming convention allowing us to identify some meta-data about the images.
