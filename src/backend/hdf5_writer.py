import h5py
from backend.node import Node, NodeType
from backend.dataset import Dataset
from backend.group import Group

class HDF5Writer():
    def saveFile(root : Group, path : str) -> None:
        file_name_without_extension : str = path.split('/')[-1]
        root.set_name(file_name_without_extension)
        save_file : h5py.Group = h5py.File(path + '.hdf5', 'w')
        for node in root.get_children():
            if node.get_node_type() == NodeType.GROUP:
                group : h5py.Group = save_file.create_group(node.get_name())
                HDF5Writer.__saveGroup(group, node)
            else:
                dataset : h5py.Dataset = save_file.create_dataset(node.get_name(), data=node.get_data())
        save_file.close()
    

    def __saveGroup(current_savefile_group : h5py.Group, group : Group) -> None:
        for node in group.get_children():
            if node.get_node_type() == NodeType.GROUP:
                group : h5py.Group = current_savefile_group.create_group(node.get_name())
                HDF5Writer.__saveGroup(group, node)
            else:
                dataset : h5py.Dataset = current_savefile_group.create_dataset(node.get_name(), data=node.get_data())