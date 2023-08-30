from PyQt5.QtWidgets import QDialog, QWidget, QLineEdit, QComboBox, QGridLayout, QLabel, QPushButton

class GroupCreator(QDialog):
    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)

        layout : QGridLayout = QGridLayout()
        self.setLayout(layout)

        layout.addWidget(QLabel('Group name'), 0, 0)
        self.__group_name : QLineEdit = QLineEdit(self)
        layout.addWidget(self.__group_name, 0, 1)

        self.__ok_button : QPushButton = QPushButton('Ok', self)
        self.__cancel_button : QPushButton = QPushButton('Cancel', self)
        self.__ok_button.clicked.connect(self.accept)
        self.__cancel_button.clicked.connect(self.reject)
        layout.addWidget(self.__ok_button, 1, 0)
        layout.addWidget(self.__cancel_button, 1, 1)
    

    def get_group_name(self) -> str:
        return self.__group_name.text()
