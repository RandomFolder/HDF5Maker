from PyQt5.QtWidgets import QDialog, QWidget, QLineEdit, QComboBox, QGridLayout, QLabel, QPushButton

class DatasetCreator(QDialog):
    def __init__(self, parent : QWidget) -> None:
        super().__init__(parent)

        layout : QGridLayout = QGridLayout()
        self.setLayout(layout)

        layout.addWidget(QLabel('Dataset name'), 0, 0)
        self.__dataset_name : QLineEdit = QLineEdit(self)
        layout.addWidget(self.__dataset_name, 0, 1)

        self.__rows_count : QLineEdit = QLineEdit(self)
        self.__cols_count : QLineEdit = QLineEdit(self)
        self.__rows_count.setPlaceholderText('Rows')
        self.__cols_count.setPlaceholderText('Columns')
        self.__rows_count.textChanged.connect(self.check_rows_count_text)
        self.__cols_count.textChanged.connect(self.check_cols_count_text)
        layout.addWidget(self.__rows_count, 1, 0)
        layout.addWidget(self.__cols_count, 1, 1)

        layout.addWidget(QLabel('Datatype'), 2, 0)
        self.__data_type : QComboBox = QComboBox(self)
        self.__data_type.addItem('Integer', 'i')
        self.__data_type.addItem('Float', 'f')
        self.__data_type.addItem('String', 'S256')
        self.__data_type.addItem('Boolean', 'b')
        layout.addWidget(self.__data_type, 2, 1)

        self.__ok_button : QPushButton = QPushButton('Ok', self)
        self.__cancel_button : QPushButton = QPushButton('Cancel', self)
        self.__ok_button.clicked.connect(self.accept)
        self.__cancel_button.clicked.connect(self.reject)
        layout.addWidget(self.__ok_button, 3, 0)
        layout.addWidget(self.__cancel_button, 3, 1)
    

    def get_dataset_name(self) -> str:
        return self.__dataset_name.text()
    

    def get_dataset_dims(self) -> list[int]:
        res : list[int] = []
        res.append(int(self.__rows_count.text()))

        if int(self.__cols_count.text()) > 1:
            res.append(int(self.__cols_count.text()))
        
        return res
    

    def get_dataset_datatype(self) -> str:
        return str(self.__data_type.currentData())
    

    def check_rows_count_text(self, text : str) -> None:
        if text.isnumeric() == False:
            self.__rows_count.clear()
    

    def check_cols_count_text(self, text : str) -> None:
        if text.isnumeric() == False:
            self.__cols_count.clear()