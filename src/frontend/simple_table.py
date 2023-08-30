import typing
from PyQt5.QtWidgets import QTableView, QWidget
from backend.table_model import TableModel
from backend.dataset import Dataset

class SimpleTable(QTableView):
    def __init__(self, parent : QWidget, editable_node : Dataset) -> None:
        super().__init__(parent)
        self._editable_node : Dataset = editable_node
        self._model : TableModel = TableModel(self, self._editable_node.get_data())

        self.setModel(self._model)