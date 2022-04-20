
from PySide6.QtWidgets import QApplication
from VideoMakerFromImage.QCreationVideo import QMainUiWindow

class VideoMakerApp():

    def __init__(self) -> None:

        app = QApplication()

        self.__master_wnd = QMainUiWindow()
    
    def run(self) -> None:

        self.__master_wnd.show()
        exit(QApplication.instance().exec())