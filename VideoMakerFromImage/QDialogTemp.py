
from PySide6.QtWidgets import QWidget, QLineEdit, QGridLayout, QPushButton, QDialog, QMessageBox, QDoubleSpinBox, QFormLayout, QSpinBox, QLabel, QFileDialog
from typing import Optional, Dict, Tuple, List, Union
import os
from VideoMakerFromImage.helper_classes import QTimerClock

class QDialogAnswer(QDialog):

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)

        self.setWindowTitle("Adding Music and Answer")
        self.setMinimumSize(700, 200)

        self._layout = QGridLayout(self)

        self._link_path = QLineEdit(self)
        self._link_path.setPlaceholderText("Link or Path")
        self._layout.addWidget(QLabel("Link or Path :"), 0, 0)
        self._layout.addWidget(self._link_path, 0, 1)
        answer_path = QPushButton(self, text="...")
        answer_path.clicked.connect(self.changePath)
        self._layout.addWidget(answer_path, 0, 2)

        self._music_name = QLineEdit(self)
        self._music_name.setPlaceholderText("Music Name")
        self._layout.addWidget(QLabel("Music Name :"), 1, 0)
        self._layout.addWidget(self._music_name, 1, 1)
    
        self._singer = QLineEdit(self)
        self._singer.setPlaceholderText("Singer")
        self._layout.addWidget(QLabel("Singer :"), 2, 0)
        self._layout.addWidget(self._singer, 2, 1)

        self._start = QTimerClock(self)
        self._layout.addWidget(QLabel("Start of the Music :"), 3, 0)
        self._layout.addWidget(self._start, 3, 1)

        self._valid = QPushButton(self, text= "Valid Answer")
        self._valid.clicked.connect(self.valid_answer)
        self._layout.addWidget(self._valid, 4, 0, 1, 2)
    
    def valid_answer(self) -> None:
        if os.path.exists(self._link_path.text()):
            self.accept()
        else:
            ret = QMessageBox.warning(self, "File not found on Local", "Are you sure you wish to add?", QMessageBox.Yes|QMessageBox.No, QMessageBox.Yes)
            if ret == QMessageBox.Yes:
                self.accept()
            else:
                self.close()
    
    def getAnswer(self) -> Tuple[str, str, str]:
        return self._link_path.text(), self._music_name.text() + " - " + self._singer.text(), self._start.getTime()
    
    def changePath(self) -> None:
        folder_path = QFileDialog.getOpenFileName(self, 'Music  Path', filter="(*.mp3);;(*.*)")
        if folder_path[0]!= '':
            self._link_path.setText(folder_path[0])
            basename:str = os.path.basename(folder_path[0])
            name = basename.split(".")[0]
            if "-" in name:
                music_name, singer = name.split("-")
                self._music_name.setText(music_name.rstrip(" "))
                self._singer.setText(singer.lstrip(" "))
            else:
                self._music_name.setText(name)
        return

class QDialogRemovePath(QDialog):

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)

        self.setWindowTitle("Remove Path")

        self._layout = QGridLayout(self)

        self._form_layout = QFormLayout()
        self._layout.addLayout(self._form_layout, 0, 0)

        self._answer = QLineEdit(self)
        self._answer.setPlaceholderText("Answer")
        self._form_layout.addRow("Answer :", self._answer)
    
        self._row = QSpinBox(self, value=1, minimum=1)
        self._form_layout.addRow("Row to remove :", self._row)
    
        self._remove = QPushButton(self, text= "Removing")
        self._remove.clicked.connect(self.remove)
        self._layout.addWidget(self._remove, 2, 0)
    
    def remove(self) -> None:
        self.accept()
    
    def getAnswer(self) -> Union[str, int]:
        answer = self._answer.text()
        row = self._row.text()
        if answer=='':
            return int(row)
        else:
            return answer