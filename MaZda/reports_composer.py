import os, glob
import numpy as np

def compose_files():
    return

if __name__ == '__main__':
    path = 'C:\\Users\\manosmark\\Desktop\\radiomic_features\\MaZda\\reports\\'

    os.chdir(path)
    reports = glob.glob('*.xls')
    patient_names = []
    files = []

    # Find unique patient names
    for report in reports:
        patient_names.append(report.split('_')[1])
    patient_names = np.unique(patient_names)

    for name in patient_names:
        files.append({'name': name, 'images':[], 'rois': []})

    for report in reports:
        patient_name = (report.split('_')[1])
        image_slice = patient_name + "_slice_" + report.split('_')[-1].split('.')[0]
        image_slice_file = image_slice + '.dcm'

        roi_slice = patient_name + "_roi_slice_" + report.split('_')[-1].split('.')[0]
        roi_slice_file = roi_slice + '.bmp'

        for file in files:
            if file.get('name', patient_name):
                file['images'].append(image_slice_file)
                file['rois'].append(roi_slice_file)

    print(files)

    compose_files()
