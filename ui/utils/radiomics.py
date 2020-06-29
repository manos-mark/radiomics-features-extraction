import csv
import os
import pandas as pd
from PyQt5 import QtGui


def pyradiomics_extraction(self, image, label, csv_file):
    if image and label:
        os.system('pyradiomics ' + image + ' ' + label + ' -o results.csv -f csv --jobs 4')
    elif csv_file:
        os.system('pyradiomics ' + csv_file + ' -o results.csv -f csv --jobs 4')
    else:
        return

    with open('results.csv', "r") as fileInput:
        for row in csv.reader(fileInput):
            items = [QtGui.QStandardItem(field) for field in row]
            self.model.appendRow(items)

    os.system('rm results.csv')
