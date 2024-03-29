
from typing import Optional, Dict, Tuple, List, Union
from random import sample
import json

from PySide6.QtWidgets import QWidget, QVBoxLayout, QDialog, QTableView, QHeaderView, QMenuBar, QFileDialog
from PySide6.QtGui import QCloseEvent, QStandardItemModel, QStandardItem, QAction

class QDialogShowAnswer(QDialog):

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)

        self.setWindowTitle("Music Added")
        self.setMinimumSize(700,500)
        self.move(0,0)
        self._layout = QVBoxLayout(self)
        self._block = True

        self._menubar = QMenuBar(self)
        file = self._menubar.addMenu("File")

        self._load_playlist = QAction("Load Playlist")
        self._load_playlist.triggered.connect(self._load)
        file.addAction(self._load_playlist)

        self._save_playlist = QAction("Save Playlist")
        self._save_playlist.triggered.connect(self._save)
        file.addAction(self._save_playlist)

        self._shuffle_action = QAction("Shuffle")
        self._shuffle_action.triggered.connect(self._shuffle)
        file.addAction(self._shuffle_action)

        self._layout.setMenuBar(self._menubar)

        self._model = QStandardItemModel(self)
        self._model.setColumnCount(4)
        self._tab_view = QTableView(self)
        self._tab_view.setEditTriggers(QTableView.NoEditTriggers)
        self._model.setHorizontalHeaderLabels(["Music link", "Answer", "Start of the Music"])
        self._tab_view.setModel(self._model)
        self._tab_view.horizontalHeader().setStretchLastSection(True)
        self._tab_view.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self._tab_view.hideColumn(3)

        self._layout.addWidget(self._tab_view)

        self._answer:Dict[str, Tuple(str, str)] = {}

    def addAnswer(self, music_link:str, answer:str, start:str) -> None:
        if music_link not in self._answer:
            items = [QStandardItem(music_link), QStandardItem(answer), QStandardItem(str(start)), QStandardItem(self._model.rowCount()+1)]
            self._model.appendRow(items)
        else:
            row = self._model.findItems(music_link)[0].row()
            self._model.setItem(row, 1, QStandardItem(answer))
            self._model.setItem(row, 2, QStandardItem(start))
        self._answer[music_link] = (answer, start)
        self._tab_view.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
    
    def deleteAnswer(self, music_link_or_row:Union[str,int]) -> Optional[str]:
        if isinstance(music_link_or_row, int) and music_link_or_row<=self._model.rowCount():
            row = music_link_or_row - 1
            question = self._model.item(row, 0).text()
            self._model.removeRow(row)
            return self._answer.pop(question)
        elif isinstance(music_link_or_row, str) and self._model.findItems(music_link_or_row, column=1) != []:
            item = self._model.findItems(music_link_or_row, column=1)[0]
            row = item.row()
            question = self._model.item(row,0).text()
            self._model.removeRow(row)
            return self._answer.pop(question)
        return None
    
    def closeEvent(self, arg__1: QCloseEvent) -> None:
        if self._block:
            return self.hide()
        return super().closeEvent(arg__1)
    
    def __len__(self) -> int:
        return self._model.rowCount()
    
    def get_row(self, row:int) -> Optional[Tuple[str, str, str]]:
        if row<len(self):
            return (self._model.item(row,0).text(), self._model.item(row,1).text(), self._model.item(row,2).text())
        return None
    
    def _shuffle(self) -> None:
        max_row = self._model.rowCount()
        random_list = sample(range(0, max_row), max_row)
        for row in range(max_row):
            self._model.item(row, 3).setText(str(random_list[row]))
            self._model.sort(3)
    
    def _load(self) -> None:
        loading_file, _ = QFileDialog.getOpenFileName(self, "Loading Playlist", filter="Playlist(*.plm)")
        if loading_file == '':
            return
        with  open(loading_file, "r") as storage_file:
            content:Dict[str, List[str, str]] = json.load(storage_file)
        for directory, [name, timer] in content.items():
            self.addAnswer(directory, name, timer)

    def _save(self) -> None:
        saving_file, _ = QFileDialog.getSaveFileName(self, "Saving Playlist", filter="Playlist(*.plm)")
        if saving_file == '':
            return
        content = {}
        for row in range(self._model.rowCount()):
            row_item = self.get_row(row)
            if row_item != None:
                directory, name, timer = row_item
                content[directory] = (name, timer)
        with open(saving_file, "w") as storage_file:
            json.dump(content, storage_file, indent = 6)