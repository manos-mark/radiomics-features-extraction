import os, glob
import numpy as np
import json
import BeautifulSoup
import pandas as pd

def compose_files(path):
    os.chdir(path)
    reports = glob.glob('*.xls')
    patient_names = []
    files = []

    # Find unique patient names
    for report in reports:
        patient_names.append(report.split('_')[1])
    patient_names = np.unique(patient_names)

    for name in patient_names:
        files.append({'name': name, 'images':[], 'rois': [], 'report': []})

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
                file['report'].append(report)
                convert_to_xlsx(report)
                
    return files

def convert_to_xlsx(report):
    with open(report + '.xls') as xml_file:
        soup = BeautifulSoup(xml_file.read(), 'xml')
        writer = pd.ExcelWriter('sample.xlsx')
        for sheet in soup.findAll('Worksheet'):
            sheet_as_list = []
            for row in sheet.findAll('Row'):
                sheet_as_list.append([cell.Data.text if cell.Data else '' for cell in row.findAll('Cell')])
            pd.DataFrame(sheet_as_list).to_excel(writer, sheet_name=sheet.attrs['ss:Name'], index=False, header=False)

        writer.save()
        
def export_json(files):
    with open('files.json', 'w') as fp:
        json.dump(files, fp)

if __name__ == '__main__':
    #path = 'C:\\Users\\manosmark\\Desktop\\radiomic_features\\MaZda\\data\\'
    path = '/home/manos/git/radiomics-features-extraction/MaZda/data'
    
    files = compose_files(path)

    export_json(files)
    

    
