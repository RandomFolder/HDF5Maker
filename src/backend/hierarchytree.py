from backend.group import Group
from backend.dataset import Dataset
from backend.node import Node, NodeType

class HierarchyTree():
    def __init__(self, root_node : Group) -> None:
        self.__root_node : Group = root_node
    

    def add_node(self, path : list[str], child : Node) -> bool:
        current_node : Node = self.__root_node
        path_without_root : list[str] = path[1:]

        for node_name in path_without_root:
            current_node = current_node.get_child(node_name)
        
        if current_node.get_node_type() == NodeType.GROUP:
            children : list[str] = [n.get_name() for n in current_node.get_children()]
            if child.get_name() in children:
                return False
            else:
                current_node.add_child(child)
                return True
        return False


    def delete_node(self, path : list[str]) -> None:
        current_node : Node = self.__root_node
        path_without_root : list[str] = path[1:]

        for i in range(0, len(path_without_root) - 1):
            current_node = current_node.get_child(path_without_root[i])
        
        current_node.delete_child(path[-1])
    

    def get_node_by_path(self, path : list[str]) -> Node:
        current_node : Node = self.__root_node
        path_without_root : list[str] = path[1:]

        for node_name in path_without_root:
            current_node = current_node.get_child(node_name)
        
        return current_node


    def get_root(self) -> Group:
        return self.__root_node