from backend.node import Node, NodeType

class Group(Node):
    def __init__(self, name) -> None:
        super().__init__(name)
        self.__children : list[Node] = []
        self._node_type : NodeType = NodeType.GROUP

    
    def get_children(self) -> list[Node]:
        return self.__children


    def get_child(self, child_name : str) -> Node:
        for child in self.get_children():
            if child.get_name() == child_name:
                return child


    def add_child(self, child : Node) -> None:
        self.__children.append(child)


    def delete_child(self, child_name : str) -> None:
        for i in range(len(self.__children)):
            if self.__children[i].get_name() == child_name:
                self.__children.pop(i)
                break