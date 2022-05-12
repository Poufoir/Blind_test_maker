
from PySide6.QtWidgets import QWidget, QVBoxLayout, QDialog, QTableView, QHeaderView
from PySide6.QtGui import QCloseEvent, QStandardItemModel, QStandardItem
from typing import Optional, Dict, Tuple, List, Callable, Union

class QDialogShowAnswer(QDialog):

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)

        self.setWindowTitle("Show Answer")
        self.setMinimumSize(700,500)
        self.move(0,0)
        self._layout = QVBoxLayout(self)
        self._block = True

        self._model = QStandardItemModel(self)
        self._model.setColumnCount(2)
        self._tab_view = QTableView(self)
        self._tab_view.setEditTriggers(QTableView.NoEditTriggers)
        self._model.setHorizontalHeaderLabels(["Music link", "Answer", "Start of the Music"])
        self._tab_view.setModel(self._model)
        self._tab_view.horizontalHeader().setStretchLastSection(True)
        self._tab_view.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        self._layout.addWidget(self._tab_view)

        self._answer:Dict[str, Tuple(str, str)] = {}

    def addAnswer(self, question:str, answer:str, start:str) -> None:
        if question not in self._answer:
            items = [QStandardItem(question), QStandardItem(answer), QStandardItem(str(start))]
            self._model.appendRow(items)
        else:
            row = self._model.findItems(question)[0].row()
            self._model.setItem(row, 1, QStandardItem(answer))
            self._model.setItem(row, 2, QStandardItem(start))
        self._answer[question] = (answer, start)
        self._tab_view.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
    
    def deleteAnswer(self, question_or_row:Union[str,int]) -> Optional[str]:
        if isinstance(question_or_row, int) and question_or_row<=self._model.rowCount():
            row = question_or_row-1
            question = self._model.item(row, 1).text()
            self._model.removeRow(row)
            return self._answer.pop(question)
        elif isinstance(question_or_row, str) and self._model.findItems(question_or_row, column=1)!=[]:
            item = self._model.findItems(question_or_row, column=1)[0]
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