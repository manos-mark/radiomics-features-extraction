import os 
import csv
import collections
import shlex, subprocess

def import_dataset():
    cases_dict = {}
    for _, _, files in os.walk(DATASET_PATH):
        for file in files:
            file_path = os.path.join(DATASET_PATH, file)

            if "_roi" in file:
                filename = file.rsplit("_")[0]
                if filename in cases_dict.keys():
                    cases_dict[filename].update({'Mask': file_path})
                else:
                    cases_dict[filename] = {'Mask': file_path}
            elif file.endswith(".nii"):
                filename = file.rsplit(".")[0]
                if filename in cases_dict.keys():
                    cases_dict[filename].update({'Image': file_path})
                else:
                    cases_dict[filename] = {'Image': file_path}
    return cases_dict


def extract_features(cases):
    # os.system('rm results.csv')
    for key in cases:
        case = cases[key]
        try:
            image_filepath = case['Image']
            mask_filepath = case['Mask']
        except AttributeError as exception:
            print("Feature extraction error. Missing image or mask.")
            print(exception)
            continue

        feature_vector = collections.OrderedDict(case)
        feature_vector['ID'] = image_filepath.rsplit(".")[0]
        feature_vector['Image'] = os.path.basename(image_filepath)
        feature_vector['Mask'] = os.path.basename(mask_filepath)

        try:
            command = EXECUTABLE + ' --ini ' + PARAMETERS_PATH + ' --img ' + image_filepath + ' file --voi ' + mask_filepath + ' file --out ' + OUTPUT_PATH + feature_vector['ID'] + '.csv'
            args = shlex.split(command)
            subprocess.call(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        except Exception as exception:
            print("Failed to extract features.")
            print(exception)

def main():
    # Get the location of the example settings file
    params = os.path.abspath(PARAMETERS_PATH)
    if not os.path.isfile(params):
        print("Failed to import parameters file.")
        return 

    # Import the dataset
    cases = import_dataset()
    if not cases:
        print("Failed to import dataset.")
        return

    # Execute batch processing to extract features
    extract_features(cases)


if __name__ == '__main__':
    
    PARAMETERS_PATH = os.path.join('settings', 'config_CT.ini')
    DATASET_PATH = '/home/manos/Desktop/dataset/'
    OUTPUT_PATH = os.path.join('output')
    EXECUTABLE = os.path.join('settings', 'RaCat_32bit.exe')

    main()
