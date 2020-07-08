# Radiomics Feature Extraction
*Radiomic data has the potential to uncover disease characteristics that fail to be appreciated by the naked eye. The central hypothesis of radiomics is that distinctive imaging algorithms quantify the state of diseases, and thereby provide valuable information for personalized medicine. Radiomics has emerged from oncology, but can be applied to other medical problems where a disease is imaged.* [radiomics.io](https://www.radiomics.io/). 

The purpose of this project is to automate the radiomics workflow and find the best composition of features, settings and parameters that can be used in order to achieve the best performance. Performance can be measured with some specific metrics (like accuracy or AUC) after our AI model has been trained. 

Using the pyradiomics library, multiple features can be extracted from medical images. After the extraction, feature analysis takes place in order to omit some portion of the features and then a machine learning model will be trained on those features. 

This process will take place multiple times using scenarios of different features and parameters until the best-case scenario can be found. 

## 0.0 Radiomics workflow
In the `/notebooks` folder there is example code for some basic "how to use pyradiomics" and further analysis for radiomics workflow.

![alt text](https://healthcare-in-europe.com/media/story_section_image/3188/image-01-picture-radiomics-workflow.jpg)

## 1.0 Image Acquisition and Segmentation
  The data consist of two folders:
  - `input-images` from [pyradiomics](https://github.com/Radiomics/pyradiomics/tree/master/data) project.
  
## 2.0 Feature extraction 
  In this section we will focus on feature extraction from a single image or a batch of images. For this project our masks (ROI) are already segmented. Detailed description on feature classes and individual features is provided in section [Radiomic Features](https://pyradiomics.readthedocs.io/en/latest/features.html#radiomics-features-label) of the documentation.
  
  *On average, Pyradiomics extracts ≈1500 features per image, which consist of the 16 shape descriptors and features extracted from original and derived images (LoG with 5 sigma levels, 1 level of Wavelet decomposistions yielding 8 derived images and images derived using Square, Square Root, Logarithm and Exponential filters).*

## 3.0 Feature analysis

## 4.0 Model Building

## 5.0 Models Comparison
