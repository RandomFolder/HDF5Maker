import h5py
from backend.node import Node, NodeType
from backend.dataset import Dataset
from backend.group import Group
from backend.hierarchytree import HierarchyTree
import numpy as np


class HDF5Reader():
    def openFile(path_to_file : str) -> HierarchyTree:
        file_name_with_extension : str = path_to_file.split('/')[-1]
        file_name_without_extension : str = file_name_with_extension.split('.')[0]
        root_node : Group = Group(file_name_without_extension)
        res : HierarchyTree = HierarchyTree(root_node)

        file : h5py.Group = h5py.File(path_to_file, 'r')
        for key in file.keys():
            if type(file[key]) == h5py.Group:
                new_group : Group = Group(key)
                root_node.add_child(new_group)
                HDF5Reader.__add_data_to_tree(file[key], new_group)
            else:
                new_dataset : Dataset = Dataset(key, np.array(list(file[key])))
                root_node.add_child(new_dataset)
        file.close()

        return res
    

    def __add_data_to_tree(h5_group : h5py.Group, hierarchy_tree_group : Group) -> None:
        for key in h5_group.keys():
            if type(h5_group[key]) == h5py.Group:
                new_group : Group = Group(key)
                hierarchy_tree_group.add_child(new_group)
                HDF5Reader.__add_data_to_tree(h5_group[key], new_group)
            else:
                new_dataset : Dataset = Dataset(key, np.array(list(h5_group[key])))
                hierarchy_tree_group.add_child(new_dataset)
