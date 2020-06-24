from PyQt5 import QtWidgets


def open_dicom_image(self):
    dialog = QtWidgets.QFileDialog()
    dialog.setWindowTitle("Choose a dicom file to open")
    dialog.setDefaultSuffix('')
    dialog.setFileMode(QtWidgets.QFileDialog.ExistingFile)
    dialog.setNameFilter(" All files (*);; Dicom Files (*.dcm,*.dicom);;Text (*.txt, *.csv)")
    dialog.setViewMode(QtWidgets.QFileDialog.Detail)

    if dialog.exec_():
        file_name = dialog.selectedFiles()
        self.image_file_path = str(file_name[0])
        if self.ROI_file_path and self.image_file_path:
            self.next_btn.setProperty('enabled', True)
        return
    else:
        print(f'dialog.exec modal window for file selection failed')
    return -1


def open_dicom_ROI(self):
    dialog = QtWidgets.QFileDialog()
    dialog.setWindowTitle("Choose a dicom file to open")
    dialog.setDefaultSuffix('')
    dialog.setFileMode(QtWidgets.QFileDialog.ExistingFile)
    dialog.setNameFilter(" All files (*);; Dicom Files (*.dcm,*.dicom);;Text (*.txt, *.csv)")
    dialog.setViewMode(QtWidgets.QFileDialog.Detail)

    if dialog.exec_():
        file_name = dialog.selectedFiles()
        self.ROI_file_path = str(file_name[0])
        if self.ROI_file_path and self.image_file_path:
            self.next_btn.setProperty('enabled', True)
        return
    else:
        print(f'dialog.exec modal window for file selection failed')
    return -1


def open_csv_file(self):
    dialog = QtWidgets.QFileDialog()
    dialog.setWindowTitle("Choose a csv file to open")
    dialog.setDefaultSuffix('')
    dialog.setFileMode(QtWidgets.QFileDialog.ExistingFile)
    dialog.setNameFilter("Text (*.txt, *.csv)")
    dialog.setViewMode(QtWidgets.QFileDialog.Detail)

    if dialog.exec_():
        file_name = dialog.selectedFiles()
        self.csv_file_path = str(file_name[0])
        self.next_btn.setProperty('enabled', True)
        return
    else:
        print(f'dialog.exec modal window for file selection failed')
    return -1
