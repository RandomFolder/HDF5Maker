from PyQt5.QtWidgets import QApplication
from frontend.appwindow import AppWindow

if __name__ == '__main__':
    app : QApplication = QApplication([])
    myapp : AppWindow = AppWindow(None)
    myapp.show()

    res : int = app.exec()