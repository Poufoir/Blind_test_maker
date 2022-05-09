
from PySide6.QtWidgets import  QWidget, QLineEdit, QGridLayout, QDialog, QFormLayout, QDoubleSpinBox, QPushButton, QMessageBox
from PySide6.QtCore import Qt
from typing import Optional, Dict, Tuple, List, Callable
import os
import subprocess
import pytube

class QCreationInputVideo(QDialog):

    def __init__(self, parent: Optional[QWidget] = None, modal:bool=True) -> None:
        super().__init__(parent, modal=modal)

        self.setWindowTitle("Creation of input Video")
        self._layout = QGridLayout(self)

        self._form_layout = QFormLayout()

        self._layout.addLayout(self._form_layout, 0, 0, 5, 1)

        self._path_ffmpeg_bin = QLineEdit("D:/ffmpeg-2022-04-18-git-d5687236ab-full_build/bin", self)
        self._path_ffmpeg_bin.setPlaceholderText("Path for ffmpeg bin")
        self._form_layout.addRow("Path ffmpeg bin :", self._path_ffmpeg_bin)

        self._path_video = QLineEdit("", self)
        self._path_video.setPlaceholderText("Path or Video Link")
        self._form_layout.addRow("Path or Video Link :", self._path_video)

        self._path_image = QLineEdit("", self)
        self._path_image.setPlaceholderText("Image Path")
        self._form_layout.addRow("Image Path :", self._path_image)

        self._timer_video = QDoubleSpinBox(self, value=5.0)
        self._form_layout.addRow("Time for Video display :", self._timer_video)

        self._timer_image = QDoubleSpinBox(self, value=5.0)
        self._form_layout.addRow("Time for Image display :", self._timer_image)

        self._path_output = QLineEdit("", self)
        self._path_output.setPlaceholderText("Output Path")
        self._form_layout.addRow("Output Path :", self._path_output)
    
        self._valid_creation = QPushButton(self, text="Valid Creation of video")
        self._valid_creation.clicked.connect(self.create_video)
        self._layout.addWidget(self._valid_creation, 5, 0)

    def create_video(self) -> None:
        path_ffmpeg = self._path_ffmpeg_bin.text().replace("\\", "/")
        path_image = self._path_image.text().replace("\\", "/")
        path_video = self._path_video.text().replace("\\", "/")
        path_output = self._path_output.text().replace("\\", "/").replace('\u202a', '')
        if not(os.path.exists(path_ffmpeg) and os.path.exists(path_image) and os.path.exists(path_video)):
            QMessageBox.critical(self, "Problem with paths", "Some paths do not exists", QMessageBox.Ok, QMessageBox.Ok)
            return
        try:
            actual_path = os.getcwd().replace("\\", "/")
            # Size of video
            subprocess_text = f'"{path_ffmpeg}/ffprobe" -v error -select_streams v:0 -show_entries stream=width,height -of csv=s=x:p=0 "{path_video}"'
            return_size = subprocess.check_output(subprocess_text)
            width, height = return_size.decode().split("\r")[0].split("x")
            width, height = int(width), int(height)


            # Transform image with extension of video
            extension_video = "." +path_video.split(".")[-1]
            subprocess_image_text = f'"{path_ffmpeg}/ffmpeg" -loop 1 -i "{path_image}" -c:v libx264 -t {self._timer_image.value()} -pix_fmt yuv420p -vf scale={width}:{height} "{actual_path}/image{extension_video}"'
            subprocess.call(subprocess_image_text)

            # Transform video
            extension_video = "." +path_video.split(".")[-1]
            subprocess_video_text = f'"{path_ffmpeg}/ffmpeg" -i "{path_video}" -c copy -t {self._timer_video.value()} "{actual_path}/video{extension_video}"'
            subprocess.call(subprocess_video_text)

            # Merge video and image
            
            subprocess_merge = f'"{path_ffmpeg}/ffmpeg" -i "{actual_path}/video{extension_video}" -i "{actual_path}/image{extension_video}" -filter_complex "[0:v][1:v] concat=n=2:v=1:a=0 [outv] " -vsync 2 -map "[outv]" "{path_output}"'
            subprocess.call(subprocess_merge)
            os.remove(f'{actual_path}/video{extension_video}')
            os.remove(f'{actual_path}/image{extension_video}')
            QMessageBox.information(self, "Sucess", "Video Created", QMessageBox.Ok, QMessageBox.Ok)
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Convertion problem", f"{type(e)} - {str(e)}", QMessageBox.Ok, QMessageBox.Ok)