from PyQt5 import QtWidgets, uic, QtCore, QtGui

from ui.utils.dialogs import *
from ui.utils.radiomics import *
import sys


class initUI(QtWidgets.QMainWindow):

    features = ['first_order', 'glcm', 'gldm', 'glrlm', 'glszm', 'ngtdm', 'shape', 'shape_2D']

    def __init__(self):
        super(initUI, self).__init__()  # Call the inherited classes __init__ method
        uic.loadUi('radiomics-feature-extractor.ui', self)  # Load the .ui file

        # Initialize main window
        self._init_main_window()

        # Initialize tabs
        self._init_input_tab()
        self._init_settings_tab()
        self._init_features_tab()
        self._init_feature_analysis_tab()

        self.show()  # Show the GUI

    def _init_main_window(self):
        # Init tab widget
        self.tab_widget = self.findChild(QtWidgets.QTabWidget, 'tabWidget')
        self.tab_widget.setTabVisible(0, True)
        self.tab_widget.setTabVisible(1, False)
        self.tab_widget.setTabVisible(2, False)
        self.tab_widget.setTabVisible(3, False)

        # Disable click on the widget bar using the eventFilter
        self.tab_widget.tabBar().installEventFilter(self)

        # Init push buttons
        self.next_btn = self.findChild(QtWidgets.QPushButton, 'next_btn')
        self.back_btn = self.findChild(QtWidgets.QPushButton, 'back_btn')
        self.reset_btn = self.findChild(QtWidgets.QPushButton, 'reset_btn')

        self.next_btn.clicked.connect(self.next_button_clicked)
        self.back_btn.clicked.connect(self.back_button_clicked)
        self.reset_btn.clicked.connect(self.reset_button_clicked)

        # Init debug mode
        self.debug_mode_checkbox = self.findChild(QtWidgets.QCheckBox, 'debug_mode_checkbox')
        self.log_text_edit = self.findChild(QtWidgets.QTextEdit, 'log_text_edit')
        self.log_label = self.findChild(QtWidgets.QLabel, 'log_label')

        self.log_text_edit.setProperty('visible', False)
        self.log_label.setProperty('visible', False)
        self.debug_mode_checkbox.toggled.connect(self.debug_mode_checkbox_toggled)

    def _init_input_tab(self):
        self.input_tab = self.findChild(QtWidgets.QWidget, 'input_tab')

        # Initialize variables
        self.image_file_path = None
        self.ROI_file_path = None
        self.csv_file_path = None

        # Init radio buttons
        self.single_image_radio = self.findChild(QtWidgets.QRadioButton, 'single_image_radio')
        self.single_image_radio.toggled.connect(lambda l: {
            self.upload_image_btn.setProperty('enabled', True),
            self.upload_ROI_btn.setProperty('enabled', True),
            self.upload_csv_btn.setProperty('enabled', False),
            self._clear_input()
        })

        self.batch_images_radio = self.findChild(QtWidgets.QRadioButton, 'batch_images_radio')
        self.batch_images_radio.toggled.connect(lambda l: {
            self.upload_image_btn.setProperty('enabled', False),
            self.upload_ROI_btn.setProperty('enabled', False),
            self.upload_csv_btn.setProperty('enabled', True),
            self._clear_input()
        })

        # Init push buttons
        self.upload_image_btn = self.findChild(QtWidgets.QPushButton, 'upload_image_btn')
        self.upload_ROI_btn = self.findChild(QtWidgets.QPushButton, 'upload_ROI_btn')
        self.upload_csv_btn = self.findChild(QtWidgets.QPushButton, 'upload_csv_btn')

        self.upload_image_btn.clicked.connect(lambda l: open_dicom_image(self))
        self.upload_ROI_btn.clicked.connect(lambda l: open_dicom_ROI(self))
        self.upload_csv_btn.clicked.connect(lambda l: open_csv_file(self))

        # Init path labels
        self.label_image_path = self.findChild(QtWidgets.QLabel, 'label_image_path')
        self.label_ROI_path = self.findChild(QtWidgets.QLabel, 'label_ROI_path')
        self.label_csv_path = self.findChild(QtWidgets.QLabel, 'label_csv_path')

    def _init_settings_tab(self):
        self.settings_tab = self.findChild(QtWidgets.QWidget, 'settings_tab')

        # Initialize variables
        self.is_any_feature_checkbox_selected = False

        # Initialize checkboxes
        for feature in self.features:
            self.__setattr__('checkbox_' + feature, self.findChild(QtWidgets.QCheckBox, 'checkbox_' + feature))
            self.__getattribute__('checkbox_' + feature).toggled.connect(self.feature_checkbox_toggled)

        # Initialize buttons
        self.select_all_none_btn = self.findChild(QtWidgets.QPushButton, 'select_all_none_btn')
        self.select_all_none_btn.clicked.connect(self.select_all_none_btn_clicked)

    def _init_features_tab(self):
        self.extracted_features_table_view = self.findChild(QtWidgets.QTableView, 'extracted_features_table_view')
        self.extracted_features_model = QtGui.QStandardItemModel(self)
        self.extracted_features_table_view.setModel(self.extracted_features_model)

    def _init_feature_analysis_tab(self):
        self.feature_importance_column_view = self.findChild(QtWidgets.QColumnView, 'feature_importance_column_view')

        self.feature_importance_model = QtGui.QStandardItemModel(self)
        self.feature_importance_column_view.setModel(self.feature_importance_model)


    @QtCore.pyqtSlot()
    def feature_checkbox_toggled(self):
        if self._is_any_feature_selected():
            self.next_btn.setProperty('enabled', True)
        else:
            self.next_btn.setProperty('enabled', False)

    @QtCore.pyqtSlot()
    def select_all_none_btn_clicked(self):
        if self.select_all_none_btn.text() == 'Select All':
            self.select_all_none_btn.setText('Select None')
            self.next_btn.setProperty('enabled', True)
            for feature in self.features:
                self.__getattribute__('checkbox_' + feature).setProperty('checked', True)
        else:
            self.select_all_none_btn.setText('Select All')
            self.next_btn.setProperty('enabled', False)
            for feature in self.features:
                self.__getattribute__('checkbox_' + feature).setProperty('checked', False)

    @QtCore.pyqtSlot()
    def next_button_clicked(self):
        # Go to the next tab if current is ready
        if self._is_tab_ready():

            # For each specific tab execute the logic
            # Settings tab
            if self.tab_widget.currentIndex() == 1:
                # Execute pyradiomics feature extraction
                pyradiomics_extraction(self, self.image_file_path, self.ROI_file_path, self.csv_file_path)

            # Go to the next tab if exists
            if self.tab_widget.currentIndex() < self.tab_widget.count() - 1:  # -1 because it is not zero based
                self.tab_widget.setTabVisible(self.tab_widget.currentIndex() + 1, True)
                self.tab_widget.setCurrentIndex(self.tab_widget.currentIndex() + 1)

                if not self._is_tab_ready():
                    # Disable next button
                    self.next_btn.setProperty('enabled', False)
                # Enable back button
                self.back_btn.setProperty('enabled', True)

    @QtCore.pyqtSlot()
    def back_button_clicked(self):
        # Go to the previous tab if it exists
        if self.tab_widget.currentIndex() > 0:
            self.tab_widget.setTabVisible(self.tab_widget.currentIndex(), False)
            # self.tab_widget.setCurrentIndex(self.tab_widget.currentIndex() - 1)
            # Disable back button if you are on the first tab
            if self.tab_widget.currentIndex() == 0:
                self.back_btn.setProperty('enabled', False)
            # Enable next button
            self.next_btn.setProperty('enabled', True)

    @QtCore.pyqtSlot()
    def debug_mode_checkbox_toggled(self):
        self.log_text_edit.setProperty('visible', not self.log_text_edit.property('visible'))
        self.log_label.setProperty('visible', not self.log_label.property('visible'))

    @QtCore.pyqtSlot()
    def reset_button_clicked(self):
        self._clear_input()
        self._hide_tabs()
        self.log_text_edit.clear()

    def _is_tab_ready(self):
        # Input tab
        if self.tab_widget.currentIndex() == 0:
            return (self.image_file_path and self.ROI_file_path) or self.csv_file_path
        # Settings tab
        elif self.tab_widget.currentIndex() == 1:
            return self._is_any_feature_selected()
        # Features tab
        elif self.tab_widget.currentIndex() == 2:
            return True

    def _hide_tabs(self):
        # Hide all tabs and move on the first one
        tabs_count = self.tab_widget.count()  # because it is not zero based
        for index in range(tabs_count):
            self.tab_widget.setTabVisible(index + 1, False)
        self.tab_widget.setCurrentIndex(0)

    def _clear_input(self):
        self.image_file_path = None
        self.ROI_file_path = None
        self.csv_file_path = None
        self.next_btn.setProperty('enabled', False)
        self.label_image_path.setText('')
        self.label_ROI_path.setText('')
        self.label_csv_path.setText('')

    def _is_any_feature_selected(self):
        for feature in self.features:
            feature_checkbox = self.__getattribute__('checkbox_' + feature)
            if feature_checkbox.property('checked'):
                return True
        return False

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.KeyPress and (event.key() == 16777217 or event.key() == 16777218):
            return True  # eat alt+tab or alt+shift+tab key
        if event.type() in (QtCore.QEvent.MouseButtonPress, QtCore.QEvent.MouseButtonDblClick):
            return True  # eat mouse click
        else:
            # standard event processing
            return super(initUI, self).eventFilter(obj, event)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    view = initUI()
    app.exec_()
