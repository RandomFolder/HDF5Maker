import typing
from PyQt5.QtCore import QAbstractTableModel, Qt, QModelIndex, QObject
import numpy as np

class TableModel(QAbstractTableModel):
    def __init__(self, parent : QObject, data : np.ndarray) -> None:
        super(TableModel, self).__init__(parent)
        self._data : np.ndarray = data
    

    def rowCount(self, index : QModelIndex) -> int:
        return len(self._data)
    

    def columnCount(self, index : QModelIndex) -> int:
        if len(self._data.shape) > 1:
            return len(self._data[0])
        else:
            return 1


    def data(self, index : QModelIndex, role : int = Qt.ItemDataRole.DisplayRole) -> str:
        if role == Qt.ItemDataRole.DisplayRole:
            try:
                if len(self._data.shape) > 1:
                    return str(self._data[index.row(), index.column()])
                else:
                    return str(self._data[index.row()])
            except:
                return ''
    

    def setData(self, index : QModelIndex, value : object, role : int = Qt.ItemDataRole.EditRole) -> bool:
        if role in (Qt.ItemDataRole.DisplayRole, Qt.ItemDataRole.EditRole):
            if not value:
                return False
            if len(self._data.shape) > 1:
                self._data[index.row(), index.column()] = value
            else:
                self._data[index.row()] = value
        return True
    

    def flags(self, index : QModelIndex) -> int:
        return super().flags(index) | Qt.ItemFlag.ItemIsEditable
