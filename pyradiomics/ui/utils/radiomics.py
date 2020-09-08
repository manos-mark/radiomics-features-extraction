import csv
import os
# import pandas as pd
from PyQt5 import QtGui


def pyradiomics_extraction(self, image, label, dataset_path):
    if image and label:
        os.system('pyradiomics ' + image + ' ' + label + ' --param ../settings/Params.yaml -o results.csv -f csv')
    elif dataset_path:
        os.system('pyradiomics ' + dataset_path + ' --param ../settings/Params.yaml -o results.csv -f csv')
    else:
        return

    with open('results.csv', "r") as fileInput:
        for row in csv.reader(fileInput):
            items = [QtGui.QStandardItem(field) for field in row]
            self.extracted_features_model.appendRow(items)

    os.system('rm results.csv')
