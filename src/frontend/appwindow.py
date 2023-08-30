from PyQt5.QtWidgets import QWidget, QGridLayout, QMainWindow, QAction, QMenuBar, QMenu, QFileDialog
from PyQt5.QtCore import QDir
from frontend.treeview import TreeView
from frontend.tabwidget import TabWidget
from frontend.group_creator import GroupCreator
from backend.group import Group
from backend.node import Node
from backend.hdf5_writer import HDF5Writer
from backend.hdf5_reader import HDF5Reader
from backend.hierarchytree import HierarchyTree

class AppWindow(QMainWindow):
    def __init__(self, parent : QWidget) -> None:
        super().__init__(parent)

        self.__tab_widget : TabWidget = None
        self.__tree_view : TreeView = None

        self.__layout : QGridLayout = QGridLayout()
        self.__widget : QWidget = QWidget()

        self.__init_gui()
    

    def __init_gui(self) -> None:
        self.setWindowTitle("HDF5Maker")
        self.setMinimumSize(800, 600)

        menuBar : QMenuBar = self.menuBar()
        fileMenu : QMenu = menuBar.addMenu("&File")

        newAction : QAction = QAction('&New', self)
        newAction.setShortcut('Ctrl+N')
        newAction.triggered.connect(self.__createNewFile)
        fileMenu.addAction(newAction)

        openAction : QAction = QAction('&Open', self)
        openAction.setShortcut('Ctrl+O')
        openAction.triggered.connect(self.__openFile)
        fileMenu.addAction(openAction)

        saveAction : QAction = QAction('&Save', self)
        saveAction.setShortcut('Ctrl+S')
        saveAction.triggered.connect(self.__saveFile)
        fileMenu.addAction(saveAction)

        self.__widget.setLayout(self.__layout)
        self.setCentralWidget(self.__widget)


    def update_tab_widget(self, cur_node : Node) -> None:
        self.__tab_widget.set_editable_node(cur_node)
        self.__tab_widget.update()


    def __createNewFile(self) -> None:
        if self.__tab_widget != None:
            self.__layout.removeWidget(self.__tab_widget)
            self.__tab_widget.destroy()
            self.__tab_widget = None
        
        if self.__tree_view != None:
            self.__layout.removeWidget(self.__tree_view)
            self.__tree_view.destroy()
            self.__tree_view = None
        
        self.__tree_view = TreeView(self, 'New File')
        self.__tab_widget = TabWidget(self, self.__tree_view.get_root_node())
        self.__tree_view.update_tab_widget_signal.connect(self.update_tab_widget)
        self.__layout.addWidget(self.__tab_widget, 0, 0, 2, 1)
        self.__layout.addWidget(self.__tree_view, 0, 1, 2, 2)

        #group_cr : GroupCreator = GroupCreator(self)
        #res : int = group_cr.exec()
        #if res == 1:
        #    self.__tree_view = TreeView(self, group_cr.get_group_name())
        #    self.__tab_widget = TabWidget(self, self.__tree_view.get_root_node())
        #    self.__tree_view.update_tab_widget_signal.connect(self.update_tab_widget)
        #    self.__layout.addWidget(self.__tab_widget, 0, 0, 2, 1)
        #    self.__layout.addWidget(self.__tree_view, 0, 1, 2, 2)


    def __openFile(self) -> None:
        dialog : QFileDialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        dialog.setFilter(QDir.Filter.Files)

        if dialog.exec():
            file_name : list[str] = dialog.selectedFiles()

            if file_name[0].endswith('.hdf5'):
                hierarchy_tree : HierarchyTree = HDF5Reader.openFile(file_name[0])

                if self.__tab_widget != None:
                    self.__layout.removeWidget(self.__tab_widget)
                    self.__tab_widget.destroy()
                    self.__tab_widget = None
                
                if self.__tree_view != None:
                    self.__layout.removeWidget(self.__tree_view)
                    self.__tree_view.destroy()
                    self.__tree_view = None
                
                self.__tree_view = TreeView(self, ' ', hierarchy_tree)
                self.__tab_widget = TabWidget(self, self.__tree_view.get_root_node())
                self.__tree_view.update_tab_widget_signal.connect(self.update_tab_widget)
                self.__layout.addWidget(self.__tab_widget, 0, 0, 2, 1)
                self.__layout.addWidget(self.__tree_view, 0, 1, 2, 2)



    def __saveFile(self) -> None:
        if self.__tab_widget != None:
            dialog : QFileDialog = QFileDialog(self, filter='HDF5 File (*.hdf5)')
            dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
            dialog.setNameFilter('HDF5 File (*.hdf5)')
            #dialog.setFilter("HDF5 File (*.hdf5)")
            res : tuple = dialog.getSaveFileName(self)
            self.__tree_view.change_root_item_text(res[0].split('/')[-1])
            HDF5Writer.saveFile(self.__tree_view.get_root_node(), res[0])