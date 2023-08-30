from PyQt5.QtWidgets import QTreeView, QMenu, QWidget, QAction, QDialog
from backend.treeview_model import TreeViewModel
from backend.hierarchytree import HierarchyTree
from backend.node import Node, NodeType
from frontend.dataset_creator import DatasetCreator
from frontend.group_creator import GroupCreator
from PyQt5.QtCore import Qt, QModelIndex, QPoint, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QStandardItem

class TreeView(QTreeView):
    update_tab_widget_signal = pyqtSignal(Node)
    def __init__(self, parent : QWidget, root_node_name : str, hierarchy_tree : HierarchyTree=None) -> None:
        super().__init__(parent)
        self.setHeaderHidden(True)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)

        self.__model : TreeViewModel = TreeViewModel(self, root_node_name, hierarchy_tree)
        
        self.setModel(self.__model)
        self.expandAll()
        self.customContextMenuRequested.connect(self.__contextMenu)
        self.clicked.connect(self.__active_item_changed)
    

    def __contextMenu(self, position : QPoint) -> None:
        item_index : QModelIndex = self.indexAt(position)
        path : list[str] = []
        self.__get_abs_path(item_index, path)
        node : Node = self.__model.get_hierarchy_tree().get_node_by_path(path)

        menu : QMenu = QMenu(self)
        if node.get_node_type() == NodeType.GROUP:
            action1 : QAction = QAction('Add group')
            action2 : QAction = QAction('Add dataset')
            action3 : QAction = QAction('Delete')
            menu.addAction(action1)
            menu.addAction(action2)
            if self.__model.itemFromIndex(item_index.parent()) != None:
                menu.addAction(action3)
            action : QAction = menu.exec_(self.mapToGlobal(position))
            
            if action == action1:
                group_cr : GroupCreator = GroupCreator(self)
                res : int = group_cr.exec()
                if res == 1:
                    self.__model.add_group(item_index, group_cr.get_group_name())
            elif action == action2:
                dataset_cr : DatasetCreator = DatasetCreator(self)
                res : int = dataset_cr.exec()
                if res == 1:
                    dataset_shape : tuple = tuple(dataset_cr.get_dataset_dims())
                    self.__model.add_dataset(item_index, dataset_cr.get_dataset_name(), dataset_shape, dataset_cr.get_dataset_datatype())
            elif action == action3:
                self.__model.delete_node(item_index, item_index.row())
        elif node.get_node_type() == NodeType.DATASET:
            action1 : QAction = QAction('Export to .csv')
            action2 : QAction = QAction('Delete')
            menu.addAction(action1)
            menu.addAction(action2)

            action : QAction = menu.exec_(self.mapToGlobal(position))

            if action == action1:
                pass
            elif action == action2:
                self.__model.delete_node(item_index, item_index.row())

    
    def __get_abs_path(self, cur_index : QModelIndex, path : list[str]) -> None:
        path.append(cur_index.data())

        if cur_index.parent() != QModelIndex():
            self.__get_abs_path(cur_index.parent(), path)
        else:
            path.reverse()


    def __active_item_changed(self, index : QModelIndex) -> None:
        path : list[str] = []
        self.__get_abs_path(index, path)
        node : Node = self.__model.get_hierarchy_tree().get_node_by_path(path)

        self.update_tab_widget_signal.emit(node)
    

    def get_root_node(self) -> None:
        hierarchy_tree = self.__model.get_hierarchy_tree()
        
        return hierarchy_tree.get_root()
    

    def change_root_item_text(self, text : str) -> None:
        root_item : QStandardItem = self.__model.item(0, 0)
        root_item.setText(text)