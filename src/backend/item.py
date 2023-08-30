from PyQt5.QtGui import QFont, QColor, QStandardItem, QIcon
from backend.node import NodeType

class Item(QStandardItem):
    def __init__(self, text : str='', font_size : int=12, set_bold : bool=False, color : QColor=QColor(0, 0, 0), node_type : NodeType=NodeType.UNKNOWN) -> None:
        super().__init__()

        font : QFont = QFont('Open Sans', font_size)
        font.setBold(set_bold)

        self.setEditable(False)
        self.setForeground(color)
        self.setFont(font)
        self.setText(text)

        if node_type == NodeType.GROUP:
            self.setIcon(QIcon('images/GroupIcon.png'))
        elif node_type == NodeType.DATASET:
            self.setIcon(QIcon('images/DatasetIcon.png'))
        