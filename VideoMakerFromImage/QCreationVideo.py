
from optparse import Option
from pickle import TRUE
from tkinter import E
from PySide6.QtWidgets import QMainWindow, QWidget, QLineEdit, QLabel, QGridLayout, QGroupBox, QPushButton, QVBoxLayout, QDialog, QTableView, QHeaderView
from PySide6.QtGui import QCloseEvent, QStandardItemModel, QStandardItem
from typing import Optional, Dict, Tuple
import os

class QDialogAnswer(QDialog):

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)

        self.setWindowTitle("Answer")

        self._layout = QGridLayout(self)

        self._label_link = QLabel(self, text="Link or Path :")
        self._link_path = QLineEdit(self)
        self._link_path.setPlaceholderText("Link or Path")
        self._layout.addWidget(self._label_link, 0, 0)
        self._layout.addWidget(self._link_path, 0, 1)

        self._label_answer = QLabel(self, text="Answer :")
        self._answer = QLineEdit(self)
        self._answer.setPlaceholderText("Answer")
        self._layout.addWidget(self._label_answer, 1, 0)
        self._layout.addWidget(self._answer, 1, 1)

        self._valid = QPushButton(self, text= "Valid Answer")
        self._valid.clicked.connect(self.valid_answer)
        self._layout.addWidget(self._valid, 3, 0, 1, 2)
    
    def valid_answer(self) -> None:
        self.accept()
    
    def getAnswer(self) -> Tuple[str, str]:
        return self._link_path.text(), self._answer.text()
    
class QDialogShowAnswer(QDialog):

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)

        self.setWindowTitle("Show Answer")
        self.setMinimumSize(200,500)
        self.move(0,0)
        self._layout = QVBoxLayout(self)
        self._block = True

        self._model = QStandardItemModel(self)
        self._model.setColumnCount(2)
        self._tab_view = QTableView(self)
        self._tab_view.setEditTriggers(QTableView.NoEditTriggers)
        self._model.setHorizontalHeaderLabels(["Music link", "Answer"])
        self._tab_view.setModel(self._model)
        self._tab_view.horizontalHeader().setStretchLastSection(True)
        self._tab_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self._layout.addWidget(self._tab_view)

        self._answer:Dict[str,str] = {}

    def addAnswer(self, question:str, answer:str) -> None:
        if question not in self._answer:
            items = [QStandardItem(question), QStandardItem(answer)]
            self._model.appendRow(items)
        else:
            row = self._model.findItems(question)[0].row()
            self._model.setItem(row, 1, QStandardItem(answer))
        self._answer[question] = answer
    
    def deleteAnswer(self, question:str) -> Optional[str]:
        return self._answer.pop(question)
    
    def closeEvent(self, arg__1: QCloseEvent) -> None:
        if self._block:
            return self.hide()
        return super().closeEvent(arg__1)

class QMainUiWindow(QMainWindow):

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
    
        self.setWindowTitle("Video Maker")
        self.setMinimumSize(700,500)
        self.move(500,0)

        self._central_widget = QWidget(self)
        self.setCentralWidget(self._central_widget)
        self._layout = QVBoxLayout(self._central_widget)

        self._path_group = QGroupBox("Paths", self._central_widget)
        self._layout.addWidget(self._path_group)

        self._layout_path = QGridLayout(self._path_group)

        self._label_path_ffmpeg = QLabel(self._path_group, text="Path for ffmpeg bin :")
        self._path_ffmpeg_bin = QLineEdit("D:/ffmpeg-2022-04-18-git-d5687236ab-full_build/bin", self._path_group)
        self._path_ffmpeg_bin.setPlaceholderText("Enter correct Path for ffmpeg bin")
        self._browse_path_ffmpeg = QPushButton(self._path_group, text="...")
        self._browse_path_ffmpeg.clicked.connect(self.browse_path_ffmpeg)

        self._layout_path.addWidget(self._label_path_ffmpeg, 0, 0)
        self._layout_path.addWidget(self._path_ffmpeg_bin, 0, 1)
        self._layout_path.addWidget(self._browse_path_ffmpeg, 0, 2)

        self._label_path_Video = QLabel(self._path_group, text="Path for Video :")
        path_video = os.getcwd().replace("\\", "/") + "/CountDown.mp4"
        self._path_Video = QLineEdit(path_video, self._path_group)
        self._path_Video.setPlaceholderText("Enter correct Path for Video")
        self._browse_path_video = QPushButton(self._path_group, text="...")
        self._browse_path_video.clicked.connect(self.browse_path_Video)

        self._layout_path.addWidget(self._label_path_Video, 1, 0)
        self._layout_path.addWidget(self._path_Video, 1, 1)
        self._layout_path.addWidget(self._browse_path_video, 1, 2)
    

        self._answer_group = QGroupBox("Answer", self._central_widget)
        self._layout.addWidget(self._answer_group)

        self._layout_answer = QGridLayout(self._answer_group)
        self._answer_dialog = QDialogShowAnswer(self)

        self._add_answer = QPushButton(self._answer_group, text="Add Question and Answer")
        self._add_answer.clicked.connect(self.addPath)
        self._layout_answer.addWidget(self._add_answer, 0, 0)

        self._show_answer = QPushButton(self._answer_group, text="Show Question and Answer")
        self._show_answer.clicked.connect(self.showPath)
        self._layout_answer.addWidget(self._show_answer, 1, 0)

    def browse_path_ffmpeg(self) -> None:
        return
    
    def browse_path_Video(self) -> None:
        return
    
    def addPath(self) -> None:
        answer_input_dialog = QDialogAnswer(self)
        ret = answer_input_dialog.exec()
        if ret:
            question, answer = answer_input_dialog.getAnswer()
            self._answer_dialog.addAnswer(question, answer)
    
    def showPath(self) -> None:
        self._answer_dialog.show()