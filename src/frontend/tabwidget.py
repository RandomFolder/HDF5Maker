import typing
from PyQt5.QtWidgets import QTabWidget, QWidget
from frontend.simple_table import SimpleTable
from backend.node import Node, NodeType
from backend.dataset import Dataset

class TabWidget(QTabWidget):
    def __init__(self, parent : QWidget, editable_node : Node) -> None:
        super().__init__(parent)
        self.__editable_node : Node = editable_node
        if self.__editable_node.get_node_type() == NodeType.DATASET:
            self.__table_widget : QWidget = SimpleTable(self, self.__editable_node)
        else:
            self.__table_widget : QWidget = QWidget(self)
        
        self.addTab(self.__table_widget, 'Data')
    

    def update(self) -> None:
        self.removeTab(0)

        if self.__editable_node.get_node_type() == NodeType.DATASET:
            self.__table_widget = SimpleTable(self, self.__editable_node)
        else:
            self.__table_widget = QWidget(self)
        
        self.addTab(self.__table_widget, 'Data')


    def set_editable_node(self, editable_node : Node) -> None:
        self.__editable_node = editable_node