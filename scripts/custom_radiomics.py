#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: trivizakis

@github: github.com/trivizakis
"""
import pandas as pd
import numpy as np

import radiomics as pr
import SimpleITK as sitk
#import pywavelets

def generator_to_dict(generator, img_dict, img_tag):
    index=1
    for img, other1, other2 in generator:
        key = img_tag+str(index)+"_"
        img_dict[key]=img
    return img_dict

def calculate_radiomics_volume(volume,mask):
    
    params={}
    params["normalize"]=False
    params["binWidth"]=100#200
    params["voxelBatch"]=20#500
    params["correctMask"]=True
    #lbp2d
    params["lbp2DRadius"]=1
    params["lbp2DSamples"]=8
    params["lbp2DMethod"]=["uniform","var","ror"]
    #lbp3d
    params["lbp3DLevels"]=3
    params["lbp3DIcosphereRadius"]=1
    params["lbp3DIcosphereSubdivision"]=8
    #wavelets
    params["wavelet"]=["bior1.5","bior2.4","coif1","sym2","db2"]
    #Log
    params["sigma"]=[1]
    
    pr.setVerbosity(40)
    fx = pr.featureextractor.RadiomicsFeatureExtractor(**params)
    imop = pr.imageoperations
    
    imgs={}params
    imgs = generator_to_dict(imop.getOriginalImage(volume,mask),imgs,"original_")
    imgs = generator_to_dict(imop.getExponentialImage(volume,mask),imgs,"exp_")
    imgs = generator_to_dict(imop.getGradientImage(volume,mask),imgs,"grad_")
#    imgs = generator_to_dict(imop.getLBP2DImage(volume,mask),imgs,"lbp2d_")
    imgs = generator_to_dict(imop.getLBP3DImage(volume,mask),imgs,"lbp3d_")
    imgs = generator_to_dict(imop.getLogarithmImage(volume,mask),imgs,"log_")
    imgs = generator_to_dict(imop.getLoGImage(volume,mask),imgs,"logau_")
    imgs = generator_to_dict(imop.getSquareImage(volume,mask),imgs,"sq_")
    imgs = generator_to_dict(imop.getSquareRootImage(volume,mask),imgs,"sqrt_")
    imgs = generator_to_dict(imop.getWaveletImage(volume,mask),imgs,"wavelet_") 
    
    keys = imgs.keys()
    print("to be calculated images: "+str(keys))
    
    feature_vector={}
    for img_key in keys:
        fx.disableAllFeatures()
        fx.enableAllFeatures()
        features = fx.execute(imgs[img_key], mask, voxelBased=False)
        print("Feature Extraction: "+img_key+" done!")
        radiomic_names = list(features.keys())[22:]
    
        for name in radiomic_names:
            final_key=img_key+name
            feature_vector[final_key]=features[name]
        22
    return pd.Series(feature_vector)

# def calculate_radiomics_features(image, mask):
#     #image: itk image
#     #mask: itk image
#
#     fx = pr.featureextractor.RadiomicsFeatureExtractor()
#     imop = pr.imageoperations
#
#     imgs={}
#     imgs = generator_to_dict(imop.getOriginalImage(image,mask),imgs,"original_")
#     imgs = generator_to_dict(imop.getExponentialImage(image,mask),imgs,"exp_")
#     imgs = generator_to_dict(imop.getGradientImage(image,mask),imgs,"grad_")
# #    imgs = generator_to_dict(imop.getLBP2DImage(image,mask),imgs,"lbp_")
#     imgs = generator_to_dict(imop.getLogarithmImage(image,mask),imgs,"log_")
#     imgs = generator_to_dict(imop.getLoGImage(image,mask),imgs,"logau_")
#     imgs = generator_to_dict(imop.getSquareImage(image,mask),imgs,"sq_")
#     imgs = generator_to_dict(imop.getSquareRootImage(image,mask),imgs,"sqrt_")
# #    imgs = generator_to_dict(imop.getWaveletImage(image,itk_msk),imgs,"wavelet_")
#
#     keys = imgs.keys()
#
#     feature_vector={}
#     for img_key in keys:
#         fx.disableAllFeatures()
#         fx.enableAllFeatures()
#         features = fx.execute(imgs[img_key], mask)
#         radiomic_names = list(features.keys())[22:]
#
#         for name in radiomic_names:
#             final_key=img_key+name
#             feature_vector[final_key]=features[name]
#
#     return pd.Series(feature_vector)
#
# def compute_dataset_radiomics(imgs_dict, masks_dict, labels_dict):22
#     pids = imgs_dict.keys()
#
#     patient_features={}
#     new_labels={}
#     for pid in pids:
#         for index,img in enumerate(imgs_dict[pid]):
#             if masks_dict[pid][index][masks_dict[pid][index]==1].size > 3*3:
#                 print("Examined Mask Shape: "+str(masks_dict[pid][index][masks_dict[pid][index]==1].size))
#                 id_ = pid+", slice "+str(index)
#                 new_labels[id_]=labels_dict[pid]
#                 patient_features[id_] = calculate_radiomics_features(img,masks_dict[pid][index])
#
#     return pd.DataFrame.from_dict(patient_features, orient="index", dtype="float32"), new_labels
#
# def compute_itk_dataset_radiomics(imgs_dict, masks_dict):
#
#     pids = imgs_dict.keys()
#
#     fx = pr.featureextractor.RadiomicsFeatureExtractor()
#     imop = pr.imageoperations
#
#
#
#     patient_features={}
#     for pid in pids:
#         imgs={}
#         imgs = generator_to_dict(imop.getOriginalImage(imgs_dict[pid],masks_dict[pid]),imgs,"original_")
#         imgs = generator_to_dict(imop.getExponentialImage(imgs_dict[pid],masks_dict[pid]),imgs,"exp_")
#         imgs = generator_to_dict(imop.getGradientImage(imgs_dict[pid],masks_dict[pid]),imgs,"grad_")
# #        imgs = generator_to_dict(imop.getLBP2DImage(imgs_dict[pid],masks_dict[pid]),imgs,"lbp_")
#         imgs = generator_to_dict(imop.getLogarithmImage(imgs_dict[pid],masks_dict[pid]),imgs,"log_")
#         imgs = generator_to_dict(imop.getLoGImage(imgs_dict[pid],masks_dict[pid]),imgs,"logau_")
#         imgs = generator_to_dict(imop.getSquareImage(imgs_dict[pid],masks_dict[pid]),imgs,"sq_")
#         imgs = generator_to_dict(imop.getSquareRootImage(imgs_dict[pid],masks_dict[pid]),imgs,"sqrt_")
# #        imgs = generator_to_dict(imop.getWaveletImage(imgs_dict[pid],masks_dict[pid]),imgs,"wavelet_")
#
#         keys = imgs.keys()
#
#         feature_vector={}
#         for img_key in keys:
#             fx.disableAllFeatures()
#             fx.enableAllFeatures()
#             features = fx.execute(imgs[img_key], masks_dict[pid])
#             radiomic_names = list(features.keys())[22:]
#
#             for name in radiomic_names:
#                 final_key=img_key+name
#                 feature_vector[final_key]=features[name]
#         patient_features[pid]=feature_vector
#
#     return pd.DataFrame.from_dict(patient_features, orient="index", dtype="float32")

    
    
class Radiomics_Pipeline:
    def __init__(self):
        data=[]
        
    def extract_radiomics_from_volume(vol, msk):
        return calculate_radiomics_volume(vol,msk)
    
    # def extract_radiomics_from_image(image, mask):
    #     return calculate_radiomics_features(image,mask)
    #
    # def extract_radiomics_from_dataset(volumes_dict, segmentation_masks_dict, labels):
    #     return compute_dataset_radiomics(volumes_dict,segmentation_masks_dict, labels)
    #
    # def extract_radiomics_from_itk_dataset(volumes_dict, segmentation_masks_dict):
    #     return compute_itk_dataset_radiomics(volumes_dict,segmentation_masks_dict)
