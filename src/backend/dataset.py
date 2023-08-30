from backend.node import Node, NodeType
import numpy as np

class Dataset(Node):
    def __init__(self, name : str, data : np.ndarray) -> None:
        super().__init__(name)
        self.__data : np.ndarray = data
        self._node_type : NodeType = NodeType.DATASET
    
    def get_data(self) -> np.ndarray:
        return self.__data