from PyQt5.uic.Compiler.qtproxies import QtGui


def OpenDicomFile():
    dialog = QtGui.QFileDialog()
    dialog.setWindowTitle("Choose a dicom file to open")
    dialog.setDefaultSuffix('')
    dialog.setFileMode(QtGui.QFileDialog.ExistingFile)
    dialog.setNameFilter(" All files (*);; Dicom Files (*.dcm,*.dicom);;Text (*.txt, *.csv)")
    dialog.setViewMode(QtGui.QFileDialog.Detail)

    # useless filename = QtCore.QStringList()

    # because of UnboundLocalError: local variable 'file_name' referenced before assignment
    # if the if statement is false and file_name gets initialized only if a condition is met,
    # so the code doesn't reach the point where file_name gets a value
    file_name = None
    if dialog.exec_():
        file_name = dialog.selectedFiles()
        print(file_name)
        # self.__class__.fileDicomPath = str(file_name[0])
    else:
        print(f'dialog.exec modal window for file selection failed')
        return -1
