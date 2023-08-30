from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import QModelIndex, QObject
from backend.hierarchytree import HierarchyTree
from backend.item import Item
from backend.node import Node, NodeType
from backend.group import Group
from backend.dataset import Dataset
import numpy as np

class TreeViewModel(QStandardItemModel):
    def __init__(self, parent : QObject, root_node_name : str='', hierarchy_tree : HierarchyTree=None) -> None:
        super().__init__(parent)
        invisible_node : QStandardItem = self.invisibleRootItem()

        if hierarchy_tree == None:
            new_item : Item = Item(root_node_name, node_type=NodeType.GROUP)
            invisible_node.appendRow(new_item)
            self.__hierarchy_tree : HierarchyTree = HierarchyTree(Group(root_node_name))
        else:
            self.__hierarchy_tree : HierarchyTree = hierarchy_tree
            self.__fill_model(self.__hierarchy_tree.get_root(), invisible_node)
    

    def add_group(self, node_index : QModelIndex, group_name : str) -> None:
        item_from_index : QStandardItem = self.itemFromIndex(node_index)
        abs_path : list[str] = []
        self.__get_abs_path(item_from_index, abs_path)
        
        if self.__hierarchy_tree.add_node(abs_path, Group(group_name)) == True:
            item_from_index.appendRow(Item(group_name, node_type=NodeType.GROUP))


    def add_dataset(self, node_index : QModelIndex, dataset_name : str, shape : tuple, dataset_dtype : str) -> None:
        item_from_index : QStandardItem = self.itemFromIndex(node_index)
        abs_path : list[str] = []
        self.__get_abs_path(item_from_index, abs_path)
        
        if self.__hierarchy_tree.add_node(abs_path, Dataset(dataset_name, np.zeros(shape=shape, dtype=dataset_dtype))) == True:
            item_from_index.appendRow(Item(dataset_name, node_type=NodeType.DATASET))
    

    def delete_node(self, node_index : QModelIndex, row : int) -> None:
        item_from_index : QStandardItem = self.itemFromIndex(node_index)
        abs_path : list[str] = []
        self.__get_abs_path(item_from_index, abs_path)

        self.__hierarchy_tree.delete_node(abs_path)
        item_from_index.parent().removeRow(row)
    

    def __get_abs_path(self, cur_node : QStandardItem, path : list[str]) -> None:
        path.append(cur_node.text())

        if cur_node.parent() is not None:
            self.__get_abs_path(cur_node.parent(), path)
        else:
            path.reverse()
    

    def __fill_model(self, node : Node, cur_item : QStandardItem) -> None:
        new_item : Item = Item(node.get_name(), node_type=node.get_node_type())
        cur_item.appendRow(new_item)

        if node.get_node_type() == NodeType.GROUP:
            for n in node.get_children():
                self.__fill_model(n, new_item)
    

    def get_hierarchy_tree(self) -> HierarchyTree:
        return self.__hierarchy_tree

