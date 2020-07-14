"""
Created on Tue Jul 14 14:11:11 2020

@author: manos
"""

import os
import collections
from sklearn.pipeline import Pipeline
from radiomics import featureextractor

def import_dataset():
    cases_dict = {}
    patients = []
    for _, dirs, _ in os.walk(DATASET_PATH):
        if len(dirs) != 0:
            patients = dirs
    for i, patient in enumerate(patients):
        for _, _, files in os.walk(os.path.join(DATASET_PATH, patient)):
            for file in files:
                filename = file.rsplit("_")[0]
                filetype = file.rsplit("_")[1]
    
                # Skip case when there is duplicate file in any patient directory
                if filename in cases_dict.keys() and 'Image' in cases_dict[filename].keys() \
                        and 'Mask' in cases_dict[filename].keys():
                    #self.logger.warning('Batch %s: Already exists, skipping this case...', filename)
                    continue
    
                file_path = os.path.join(DATASET_PATH, patient, file)
    
                if filetype == IMAGE_TYPE:
                    if filename in cases_dict.keys():
                        cases_dict[filename].update({'Image': file_path})
                    else:
                        cases_dict[filename] = {'Image': file_path}
    
                elif filetype == MASK_TYPE:
                    if filename in cases_dict.keys():
                        cases_dict[filename].update({'Mask': file_path})
                    else:
                        cases_dict[filename] = {'Mask': file_path}
    return cases_dict


def batch_processing(extractor, cases):
    for key in cases:
        case = cases[key]
        image_filepath = case['Image']
        mask_filepath = case['Mask']
    
        if (image_filepath is not None) and (mask_filepath is not None):
          featureVector = collections.OrderedDict(case)
          featureVector['Image'] = os.path.basename(image_filepath)
          featureVector['Mask'] = os.path.basename(mask_filepath)
    
          try:
            featureVector.update(extractor.execute(imageFilepath, maskFilepath))
    
            with open(outputFilepath, 'a') as outputFile:
              writer = csv.writer(outputFile, lineterminator='\n')
              if headers is None:
                headers = list(featureVector.keys())
                writer.writerow(headers)
    
              row = []
              for h in headers:
                row.append(featureVector.get(h, "N/A"))
              writer.writerow(row)
          except Exception:
            continue
            #logger.error('FEATURE EXTRACTION FAILED', exc_info=True)    

def main():
    # Get the location of the example settings file
    params = os.path.abspath(PARAMETERS_PATH)
    if not os.path.isfile(params):
        return 
    
    # Import the dataset
    cases = import_dataset()
    if not cases:
        return
    
    # Initialize feature extractor using the settings file
    extractor = featureextractor.RadiomicsFeatureExtractor(params)
    
    # Execute batch processing
    results = batch_processing(extractor, cases)
    



if __name__ == '__main__':
    
    PARAMETERS_PATH = 'settings/Params.yaml'
    DATASET_PATH = 'data/input-images/patients'
    IMAGE_TYPE = 'image.nrrd'
    MASK_TYPE = 'label.nrrd'
    
    main()
