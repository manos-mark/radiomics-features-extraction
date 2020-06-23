from PyQt5 import QtWidgets, uic
from ui.utils.dicom import *
import sys


class init_UI(QtWidgets.QMainWindow):
    def __init__(self):
        super(init_UI, self).__init__()  # Call the inherited classes __init__ method
        uic.loadUi('radiomics-feature-extractor.ui', self)  # Load the .ui file

        # Initialize main window
        self._init_main_window()

        # Initialize tabs
        self.input_images_tab = self.findChild(QtWidgets.QWidget, 'input_images_tab')
        self.settings_customization_tab = self.findChild(QtWidgets.QWidget, 'settings_customization_tab')

        self._init_input_images_tab()

        self.show()  # Show the GUI

    def _init_main_window(self):
        # Init back and next buttons
        self.next_btn = self.findChild(QtWidgets.QPushButton, 'next_btn')
        self.back_btn = self.findChild(QtWidgets.QPushButton, 'back_btn')

        self.next_btn.clicked.connect(lambda a: print("NEXT"))
        self.back_btn.clicked.connect(lambda a: print("BACK"))

    def _init_input_images_tab(self):
        # Init input buttons
        self.upload_image_btn = self.findChild(QtWidgets.QPushButton, 'upload_image_btn')
        self.upload_ROI_btn = self.findChild(QtWidgets.QPushButton, 'upload_ROI_btn')
        self.upload_csv_btn = self.findChild(QtWidgets.QPushButton, 'upload_csv_btn')

        self.upload_image_btn.clicked.connect(lambda l: OpenDicomFile())


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    view = init_UI()
    app.exec_()