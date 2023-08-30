from enum import Enum

class NodeType(Enum):
    UNKNOWN = 1
    GROUP = 2
    DATASET = 3

class Node():
    def __init__(self, name : str) -> None:
        self._name : str = name
        self._node_type : NodeType = NodeType.UNKNOWN
    
    def get_name(self) -> str:
        return self._name
    
    def get_node_type(self) -> NodeType:
        return self._node_type
    
    def set_name(self, new_name : str) -> None:
        self._name = new_name