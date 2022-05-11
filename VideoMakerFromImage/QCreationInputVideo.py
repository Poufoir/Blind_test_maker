
from PySide6.QtWidgets import  QWidget, QLineEdit, QGridLayout, QDialog, QFormLayout, QPushButton, QMessageBox, QComboBox
from typing import Optional, Dict, List
import os
import subprocess
import pytube
from VideoMakerFromImage.helper_classes import QTimerClock


class QCreationInputVideo(QDialog):

    def __init__(self, parent: Optional[QWidget] = None, modal:bool=True) -> None:
        super().__init__(parent, modal=modal)

        self.setWindowTitle("Creation of input Video")
        self.setMinimumSize(500, 300)
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

        self._start_video = QTimerClock(self)
        self._form_layout.addRow("Time to start Video display :", self._start_video)

        self._timer_video = QTimerClock(self, seconds=5)
        self._form_layout.addRow("Duration for Video display :", self._timer_video)

        self._timer_image = QTimerClock(self, seconds=5)
        self._form_layout.addRow("Duration for Image display :", self._timer_image)

        self._path_output = QLineEdit("", self)
        self._path_output.setPlaceholderText("Output Path")
        self._form_layout.addRow("Output Path :", self._path_output)

        self._name_output = QLineEdit("", self)
        self._name_output.setPlaceholderText("Output Name")
        self._form_layout.addRow("Output Name :", self._name_output)

        self._extension_output = QComboBox(self)
        self._extension_output.setEditable(True)
        self._extension_output.addItems(["mp4", "avi", "mkv"])
        self._form_layout.addRow("Output Name :", self._extension_output)
    
        self._valid_creation = QPushButton(self, text="Valid Creation of video")
        self._valid_creation.clicked.connect(self.create_video)
        self._layout.addWidget(self._valid_creation, 5, 0)

    def create_video(self) -> None:
        path_ffmpeg = self._path_ffmpeg_bin.text().replace("\\", "/")
        path_image = self._path_image.text().replace("\\", "/")
        path_video = self._path_video.text().replace("\\", "/")
        path_output = self._path_output.text().replace("\\", "/").replace('\u202a', '')
        if not(os.path.exists(path_ffmpeg) and os.path.exists(path_image) and os.path.exists(path_video) and os.path.exists(path_output)):
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
            subprocess_image_text = f'"{path_ffmpeg}/ffmpeg" -loop 1 -i "{path_image}" -c:v libx264 -t {self._timer_image.getTime()} -pix_fmt yuv420p -vf scale={width}:{height} "{actual_path}/image{extension_video}"'
            subprocess.call(subprocess_image_text)

            # Transform video
            start = self._start_video.getTime()
            extension_video = "." +path_video.split(".")[-1]
            subprocess_video_text = f'"{path_ffmpeg}/ffmpeg" -i "{path_video}" -ss {start} -to {QTimerClock.addTimer(self._timer_video.getTime(), start)} -c:v libx264 -crf 23 "{actual_path}/video{extension_video}"'
            subprocess.call(subprocess_video_text)

            # Merge video and image
            extension = self._extension_output.currentText()
            output_name = self._name_output.text()
            if not path_output.endswith("/"):
                path_output += "/"
            subprocess_merge = f'"{path_ffmpeg}/ffmpeg" -i "{actual_path}/video{extension_video}" -i "{actual_path}/image{extension_video}" -filter_complex "[0:v][1:v] concat=n=2:v=1:a=0 [outv] " -vsync 2 -map "[outv]" "{path_output+output_name}.{extension}"'
            subprocess.call(subprocess_merge)
            os.remove(f'{actual_path}/video{extension_video}')
            os.remove(f'{actual_path}/image{extension_video}')
            QMessageBox.information(self, "Sucess", "Video Created", QMessageBox.Ok, QMessageBox.Ok)
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Convertion problem", f"{type(e)} - {str(e)}", QMessageBox.Ok, QMessageBox.Ok)