
from PySide6.QtWidgets import  QWidget, QGridLayout, QSpinBox, QLabel

from typing import Optional

class QTimerClock(QWidget):
    def __init__(self, parent: Optional[QWidget] = None, seconds:int=0, minutes:int=0, hours:int=0, milliseconds:bool=False) -> None:
        super().__init__(parent)

        self._layout = QGridLayout(self)
        self._hours = QSpinBox(self, minimum=0, value=hours)
        self._hours.setSuffix("h")
        self._minutes = QSpinBox(self, minimum=0, maximum = 59, value=minutes)
        self._minutes.setSuffix("min")
        self._seconds = QSpinBox(self, minimum=0, maximum = 59, value=seconds)
        self._seconds.setSuffix("s")
        if milliseconds:
            self._mseconds = QSpinBox(self, minimum=0, maximum = 999, value=0)
            self._mseconds.setSuffix("ms")
            self._layout.addWidget(self._mseconds, 0, 5)

        self._layout.addWidget(self._hours, 0, 0)
        label = QLabel(self, text=":")
        label.setMaximumWidth(2)
        self._layout.addWidget(label, 0, 1)
        self._layout.addWidget(self._minutes, 0, 2)
        label = QLabel(self, text=":")
        label.setMaximumWidth(2)
        self._layout.addWidget(label, 0, 3)
        self._layout.addWidget(self._seconds, 0, 4)

        self._ms:bool=milliseconds

    def getTime(self) -> str:
        return str(self._hours.value())+":"+str(self._minutes.value())+":"+str(self._seconds.value())
    
    def get_ms(self) -> int:
        if self._ms:
            return self._mseconds.value()
        else:
            return 0

    @staticmethod
    def addTimer(first_time:str, second_time:str) -> str:
        ft = first_time.split(":")
        st = second_time.split(":")
        seconds = int(ft[2])+int(st[2])
        minutes = int(ft[1])+int(st[1])
        hours = int(ft[0])+int(st[0])
        seconds, add_minutes = seconds%60, seconds//60
        minutes += add_minutes
        minutes, add_hours = minutes%60, minutes//60
        hours +=add_hours
        return str(hours)+':'+str(minutes)+":"+str(seconds)
    
    @staticmethod
    def multiplyTimer(first_time:str, multiple:int) -> str:
        ft = first_time.split(":")
        seconds = int(ft[2]) * multiple
        seconds, add_minutes = seconds%60, seconds//60
        minutes = int(ft[1])*multiple + add_minutes
        minutes, add_hours = minutes%60, minutes//60
        hours = int(ft[0]) + add_hours
        return str(hours)+':'+str(minutes)+":"+str(seconds)
    
    @staticmethod
    def subtract(first_time:str, second_time:str) -> str:
        ft = first_time.split(":")
        st = second_time.split(":")
        seconds = int(ft[2])-int(st[2])
        minutes = int(ft[1])-int(st[1])
        hours = int(ft[0])-int(st[0])
        if seconds<0:
            seconds += 60
            minutes -= 1
        if minutes<0:
            minutes += 60
            hours -= 1
        if seconds<0 or minutes<0 or hours<0:
            return "00:00:00"
        return str(hours)+':'+str(minutes)+":"+str(seconds)
    
    @staticmethod
    def toSeconds(obj:str) -> int:
        ft = obj.split(":")
        seconds = int(ft[2])
        minutes = int(ft[1])
        hours = int(ft[0])
        return seconds + minutes*60 + hours *60 *60