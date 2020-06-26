import os

from PyQt5 import QtWidgets


def open_dicom_image(self):
    dialog = open_dialog()

    if dialog.exec_():
        file_name = dialog.selectedFiles()

        # Check if file exists
        if os.path.isfile(file_name[0]):
            # initialize logs and success feedback
            self.label_image_path.setText(f'File {os.path.split(file_name[0])[1]} loaded successfully.')
            self.log_text_edit.append(f'File {os.path.split(file_name[0])[1]} loaded successfully.')
        else:
            self.log_text_edit.append(f'Could not obtain file from path: {file_name} !! \n Try again please ...')

        # Set file path
        self.image_file_path = str(file_name[0])

        # Enable next button if both files (image+mask) are loaded
        if self.ROI_file_path and self.image_file_path:
            self.next_btn.setProperty('enabled', True)
        return

    return -1


def open_dicom_ROI(self):
    dialog = open_dialog()

    if dialog.exec_():
        file_name = dialog.selectedFiles()

        # Check if file exists
        if os.path.isfile(file_name[0]):
            # initialize logs and success feedback
            self.label_ROI_path.setText(f'File {os.path.split(file_name[0])[1]} loaded successfully.')
            self.log_text_edit.append(f'File {os.path.split(file_name[0])[1]} loaded successfully.')
        else:
            self.log_text_edit.append(f'Could not obtain file from path: {file_name} !! \n Try again please ...')

        # Set file path
        self.ROI_file_path = str(file_name[0])

        # Enable next button if both files (image+mask) are loaded
        if self.ROI_file_path and self.image_file_path:
            self.next_btn.setProperty('enabled', True)
        return

    return -1


def open_csv_file(self):
    dialog = open_dialog()
    dialog.setNameFilter("Text (*.txt, *.csv)")

    if dialog.exec_():
        file_name = dialog.selectedFiles()

        # Check if file exists
        if os.path.isfile(file_name[0]):
            # initialize logs and success feedback
            self.label_csv_path.setText(f'File {os.path.split(file_name[0])[1]} loaded successfully.')
            self.log_text_edit.append(f'File {os.path.split(file_name[0])[1]} loaded successfully.')
        else:
            self.log_text_edit.append(f'Could not obtain file from path: {file_name} !! \n Try again please ...')

        # Set file path
        self.csv_file_path = str(file_name[0])
        self.next_btn.setProperty('enabled', True)
        return

    return -1


def open_dialog():
    dialog = QtWidgets.QFileDialog()
    dialog.setWindowTitle("Choose a dicom file to open")
    dialog.setDefaultSuffix('')
    dialog.setFileMode(QtWidgets.QFileDialog.ExistingFile)
    dialog.setNameFilter(" All files (*.nrrd);; Dicom Files (*.dcm,*.dicom)")
    dialog.setViewMode(QtWidgets.QFileDialog.Detail)
    return dialog
