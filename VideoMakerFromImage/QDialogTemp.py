
from PySide6.QtWidgets import QWidget, QLineEdit, QGridLayout, QPushButton, QDialog, QMessageBox, QDoubleSpinBox, QFormLayout, QSpinBox, QLabel, QFileDialog
from typing import Optional, Dict, Tuple, List, Union
import os
import re
from pytube import YouTube
from pytube.exceptions import RegexMatchError

from VideoMakerFromImage.helper_classes import QTimerClock

class QDialogAnswer(QDialog):

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)

        self.setWindowTitle("Adding Music and Answer")
        self.setMinimumSize(700, 200)

        self._layout = QGridLayout(self)

        self._link_path = QLineEdit(self)
        self._link_path.setPlaceholderText("Link or Path")
        self._link_path.textEdited.connect(self._text_edited)
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
        accent = bool(re.search("[\u00C0-\u017F]", self._link_path.text() + self._music_name.text() + self._singer.text()))
        if os.path.exists(self._link_path.text()) and not accent:
            self.accept()
        elif accent:
            ret = QMessageBox.critical(self, "Accents detected", "You cannot add this file\nPlease remove all accents", QMessageBox.No, QMessageBox.No)
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
    
    def _text_edited(self, new_text:str) -> None:
        if new_text.startswith("https://www.youtube.com/"):
            try:
                yt_link = YouTube(new_text)
                yt_title = yt_link.title.split("-")
                yt_music_name, yt_singer = yt_title if len(yt_title) == 2 else yt_title[0], ""
                self._music_name.setText(yt_music_name)
                self._singer.setText(yt_singer)
            except RegexMatchError as e:
                pass
            except Exception as e:
                pass

class QDialogRemovePath(QDialog):

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)

        self.setWindowTitle("Remove Music")

        self._layout = QGridLayout(self)

        self._form_layout = QFormLayout()
        self._layout.addLayout(self._form_layout, 0, 0)

        self._music = QLineEdit(self)
        self._music.setPlaceholderText("Music Name - Singer")
        self._form_layout.addRow("Music to remove :", self._music)
    
        self._first_row = QSpinBox(self, value=1, minimum=1, maximum=999)
        self._end_row = QSpinBox(self, value=1, minimum=1, maximum=999)
        self._form_layout.addRow("First row to remove :", self._first_row)
        self._form_layout.addRow("End row to remove :", self._end_row)
    
        self._remove = QPushButton(self, text= "Valid Removing Music")
        self._remove.clicked.connect(self.remove)
        self._layout.addWidget(self._remove, 2, 0)
    
    def remove(self) -> None:
        self.accept()
    
    def getMusictoRemove(self) -> Union[str, Tuple[int, int]]:
        music_to_remove = self._music.text()
        first_row = self._first_row.value()
        end_row = self._end_row.value() if self._end_row.text() != '' else first_row
        if music_to_remove=='':
            return int(first_row), int(end_row)
        else:
            return music_to_remove