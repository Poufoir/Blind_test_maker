
from tkinter import E
from PySide6.QtWidgets import QWidget, QLineEdit, QGridLayout, QPushButton, QDialog, QMessageBox, QDoubleSpinBox, QFormLayout, QSpinBox
from typing import Optional, Dict, Tuple, List, Union
import os

from numpy import minimum

class QDialogAnswer(QDialog):

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)

        self.setWindowTitle("Answer")

        self._layout = QGridLayout(self)

        self._form_layout = QFormLayout()
        self._layout.addLayout(self._form_layout, 0, 0)

        self._link_path = QLineEdit(self)
        self._link_path.setPlaceholderText("Link or Path")
        self._form_layout.addRow("Link or Path :", self._link_path)

        self._answer = QLineEdit(self)
        self._answer.setPlaceholderText("Answer")
        self._form_layout.addRow("Answer :", self._answer)

        self._start = QDoubleSpinBox(self, value=0)
        self._form_layout.addRow("Start of music :", self._start)

        self._valid = QPushButton(self, text= "Valid Answer")
        self._valid.clicked.connect(self.valid_answer)
        self._layout.addWidget(self._valid, 3, 0, 1, 2)
    
    def valid_answer(self) -> None:
        if os.path.exists(self._link_path.text()):
            self.accept()
        else:
            ret = QMessageBox.warning(self, "File not found on Local", "Are you sure you wish to add?", QMessageBox.Yes|QMessageBox.No, QMessageBox.Yes)
            if ret == QMessageBox.Yes:
                self.accept()
            else:
                self.close()
    
    def getAnswer(self) -> Tuple[str, str, float]:
        return self._link_path.text(), self._answer.text(), self._start.value()

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