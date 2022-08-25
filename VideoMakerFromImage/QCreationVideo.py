
from PySide6.QtWidgets import QMainWindow, QWidget, QLineEdit, QLabel, QGridLayout, QGroupBox, QPushButton, QVBoxLayout, QFileDialog, QSpinBox, QMessageBox, QComboBox
from PySide6.QtCore import Qt
from typing import Optional, Dict, List, Callable
import os
import subprocess
from VideoMakerFromImage.QDialogTemp import QDialogAnswer, QDialogRemovePath
from VideoMakerFromImage.QDialogShowAnswer import QDialogShowAnswer
from VideoMakerFromImage.helper_classes import QTimerClock

class QMainUiWindow(QMainWindow):

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
    
        self.setWindowTitle("Video Maker")
        self.setMinimumSize(810,500)
        self.move(700,0)

        self._central_widget = QWidget(self)
        self.setCentralWidget(self._central_widget)
        self._layout = QVBoxLayout(self._central_widget)

        self._path_group = QGroupBox("Paths", self._central_widget)
        self._path_group.setStyleSheet("QGroupBox {border:1px solid black;}")

        self._layout_path = QGridLayout(self._path_group)

        self._path_ffmpeg_bin = QLineEdit("D:/ffmpeg-2022-04-18-git-d5687236ab-full_build/bin", self._path_group)
        self._path_ffmpeg_bin.setPlaceholderText("Enter correct Path for ffmpeg bin")
        self._browse_path_ffmpeg = QPushButton(self._path_group, text="...")
        self._browse_path_ffmpeg.clicked.connect(self.browse_path_ffmpeg)
        # Layout
        self._layout_path.addWidget(QLabel(self._path_group, text="Path for ffmpeg bin :"), 0, 0)
        self._layout_path.addWidget(self._path_ffmpeg_bin, 0, 1)
        self._layout_path.addWidget(self._browse_path_ffmpeg, 0, 2)

        path_video = os.getcwd().replace("\\", "/") + "/VideoMakerFromImage/5 SECOND TIMER.mp4"
        self._path_video = QLineEdit(path_video, self._path_group)
        self._path_video.setPlaceholderText("Enter correct Path for Video")
        self._browse_path_video = QPushButton(self._path_group, text="...")
        self._browse_path_video.clicked.connect(self.browse_path(self._path_video))

        # Layout
        self._layout_path.addWidget(QLabel(self._path_group, text="Path for Video :"), 1, 0)
        self._layout_path.addWidget(self._path_video, 1, 1)
        self._layout_path.addWidget(self._browse_path_video, 1, 2)

        path_image = os.getcwd().replace("\\", "/") + "/VideoMakerFromImage/sunrise.webp"
        self._path_image = QLineEdit(path_image, self._path_group)
        self._path_image.setPlaceholderText("Image Path")
        self._browse_path_image = QPushButton(self._path_group, text="...")
        self._browse_path_image.clicked.connect(self.browse_path(self._path_image))

        # Layout
        self._layout_path.addWidget(QLabel(self._path_group, text="Path for Image :"), 2, 0)
        self._layout_path.addWidget(self._path_image, 2, 1)
        self._layout_path.addWidget(self._browse_path_image, 2, 2)

        path_output = os.getcwd().replace("\\", "/") + "/VideoMakerFromImage/"
        self._path_output = QLineEdit(path_output, self._path_group)
        self._path_output.setPlaceholderText("Enter correct Path for Output")
        self._browse_path_output = QPushButton(self._path_group, text="...")
        self._browse_path_output.clicked.connect(self.browse_path(self._path_output))

        # Layout
        self._layout_path.addWidget(QLabel(self._path_group, text="Folder for Output :"), 3, 0)
        self._layout_path.addWidget(self._path_output, 3, 1)
        self._layout_path.addWidget(self._browse_path_output, 3, 2)

        self._output_name = QLineEdit("output", self._path_group)
        self._output_name.setPlaceholderText("Enter correct Path for Output")
        list_output_extension = [".mp4", ".avi", ".mkv"]
        self._output_extension = QComboBox(self._path_group)
        self._output_extension.addItems(list_output_extension)
        self._output_extension.setEditable(True)

        # Layout
        self._layout_path.addWidget(QLabel(self._path_group, text="Output Name :"), 4, 0)
        self._layout_path.addWidget(self._output_name, 4, 1)
        self._layout_path.addWidget(self._output_extension, 4, 2)



        self._answer_group = QGroupBox("Music", self._central_widget)
        self._answer_group.setStyleSheet("QGroupBox {border:1px solid black;}")

        self._layout_answer = QGridLayout(self._answer_group)
        self._answer_dialog = QDialogShowAnswer(self)

        layout_timer = QGridLayout()
        duration_answer = QLabel(self._answer_group, text= "Duration of Answer :")
        duration_answer.setMaximumWidth(110)
        self._duration_answer = QTimerClock(self._answer_group, seconds=5, milliseconds=True)
        # Layout
        layout_timer.addWidget(duration_answer, 0, 0, Qt.AlignVCenter)
        layout_timer.addWidget(self._duration_answer, 0, 1, Qt.AlignVCenter)

        self._layout_answer.addLayout(layout_timer, 0, 0, 1, 4)

        self._add_answer = QPushButton(self._answer_group, text="Add Music and Answer")
        self._add_answer.clicked.connect(self.addPath)
        # Layout
        self._layout_answer.addWidget(self._add_answer, 1, 0, 1, 4)

        self._remove_answer = QPushButton(self._answer_group, text="Remove Music")
        self._remove_answer.clicked.connect(self.removePath)
        # Layout
        self._layout_answer.addWidget(self._remove_answer, 2, 0, 1, 4)

        self._show_answer = QPushButton(self._answer_group, text="Show Music and Answer")
        self._show_answer.clicked.connect(self.showPath)
        # Layout
        self._layout_answer.addWidget(self._show_answer, 3, 0, 1, 4)



        self._video_group = QGroupBox("Video", self._central_widget)
        self._video_group.setStyleSheet("QGroupBox {border:1px solid black;}")
        self._layout_video = QGridLayout(self._video_group)

        self._start_video = QTimerClock(self)
        # Layout
        self._layout_video.addWidget(QLabel(self._video_group, text="Time to start Video display :"), 0, 0)
        self._layout_video.addWidget(self._start_video, 0, 1)

        self._timer_video = QTimerClock(self, seconds=6)
        # Layout
        self._layout_video.addWidget(QLabel(self._video_group, text="Duration of Video :"), 1, 0)
        self._layout_video.addWidget(self._timer_video, 1, 1)

        self._color_setting = QLineEdit("red", self._video_group)
        # Layout
        self._layout_video.addWidget(QLabel(self._video_group, text="Color of Answer :"), 2, 0)
        self._layout_video.addWidget(self._color_setting, 2, 1)

        self._size_setting = QSpinBox(self._video_group, value=90)
        # Layout
        self._layout_video.addWidget(QLabel(self._video_group, text="Size of Answer :"), 3, 0)
        self._layout_video.addWidget(self._size_setting, 3, 1)
    

        self._valid_creation_video = QPushButton(self._central_widget, text="Create Video")
        self._valid_creation_video.clicked.connect(self.createVideo)


        self._layout.addWidget(self._path_group)
        self._layout.addWidget(self._video_group)
        self._layout.addWidget(self._answer_group)
        self._layout.addWidget(self._valid_creation_video)

    def browse_path_ffmpeg(self) -> None:
        folder_path = QFileDialog.getExistingDirectory(self, 'ffmpeg Caption')

        if folder_path!= '':
            self._path_ffmpeg_bin.setText(folder_path)
        return
    
    def browse_path_Video(self) -> None:
        file_path = QFileDialog.getOpenFileName(self, 'Video Caption', filter="(*.mp4);;(*.*)")

        if file_path[0]!= '':
            self._path_video.setText(file_path[0])
        return
    
    def browse_path(self, widget:QLineEdit)-> Callable[[], None]:
        def change_text() -> None:
            file_path = QFileDialog.getOpenFileName(self, 'Video Caption', filter="(*.mp4);;(*.*)")

            if file_path[0]!= '':
                widget.setText(file_path[0])
            return
        return change_text
    
    def addPath(self) -> None:
        answer_input_dialog = QDialogAnswer(self)
        ret = answer_input_dialog.exec()
        if ret:
            question, answer, start = answer_input_dialog.getAnswer()
            self._answer_dialog.addAnswer(question, answer, start)
    
    def showPath(self) -> None:
        self._answer_dialog.show()
    
    def removePath(self):
        answer_input_dialog = QDialogRemovePath(self)
        ret = answer_input_dialog.exec()
        if ret:
            answer = answer_input_dialog.getAnswer()
            self._answer_dialog.deleteAnswer(answer)
    
    def createVideo(self) -> None:
        if not self.create_input_video():
            return
        n = len(self._answer_dialog)
        if n==0:
            return
        try:
            myBat = open('./cmd_file.bat','w')
            actual_path = os.getcwd().replace("\\", "/")
            if actual_path.endswith("/"):
                path_video = actual_path + "input_video.mp4"
            else:
                path_video = actual_path + "/input_video.mp4"
            duration = self._duration_answer.getTime()
            timer = (self._timer_video.getTime(), QTimerClock.addTimer(self._timer_video.getTime(), duration))
            size = self._size_setting.value()
            fontcolor = self._color_setting.text()
            path_video_output = self._path_output.text() + self._output_name.text() + self._output_extension.currentText()
            myBat.write(self._path_ffmpeg_bin.text() + "/ffmpeg ")
            music_file =''
            separation_seconds = ''
            row_text_cmd = ''
            draw_text_cmd = ""
            for row in range(n):
                start_music = QTimerClock.multiplyTimer(timer[1], row)
                start_answer = QTimerClock.addTimer(start_music,timer[0])
                end_answer = QTimerClock.addTimer(start_answer,duration)

                music, answer, start = self._answer_dialog.get_row(row)
                music_name, singer = answer.split(" - ")
                start = QTimerClock.toSeconds(start)
                end_music = QTimerClock.toSeconds(timer[1]) + start

                myBat.write(f'-i "{path_video}" ')
                row_text_cmd += f"[video_row{row}] "
                separation_seconds += f"""[{row}:v] trim=start=0:end={QTimerClock.toSeconds(timer[1])},setpts=PTS-STARTPTS[video_row{row}];"""
                draw_text_cmd += f""" ;[outv] drawtext=enable='between(t,{QTimerClock.toSeconds(start_answer)},{QTimerClock.toSeconds(end_answer)})':text='{music_name}':x=(w-text_w)/2:y=(h-text_h)/2:fontsize={size}:fontcolor={fontcolor},"""
                draw_text_cmd += f"""drawtext=enable='between(t,{QTimerClock.toSeconds(start_answer)},{QTimerClock.toSeconds(end_answer)})':text='{singer}':x=(w-text_w)/2:y=(h+text_h)/2:fontsize={size}:fontcolor={fontcolor}[outv]"""

                if os.path.exists(music):
                    music = music.replace("\\", "/")
                    music_file += f"""-i "{music}" """
                    separation_seconds += f"""[{row+n}:a] atrim=start={start}:end={end_music},asetpts=PTS-STARTPTS[music_row{row}];"""
                    row_text_cmd += f"[music_row{row}] "

            if music_file != '':
                myBat.write(music_file)
            myBat.write('-filter_complex "')
            if music_file != '':
                myBat.write(separation_seconds)
            myBat.write(row_text_cmd + f"concat=n={n}:v=1:a=1 [outv] [outa]")
            myBat.write(draw_text_cmd)
            myBat.write(""" " -map "[outv]" -map "[outa]" """)
            myBat.write(f'"{path_video_output}"')
            myBat.close()
        except Exception as e:
            pass
        try:
            path = os.getcwd().replace("\\", "/") + "/cmd_file.bat"
            subprocess.call([path])
            os.remove(f'{path_video}')
        except:
            pass
        return
    
    def create_input_video(self) -> None:
        path_ffmpeg = self._path_ffmpeg_bin.text().replace("\\", "/")
        path_image = self._path_image.text().replace("\\", "/")
        path_video = self._path_video.text().replace("\\", "/")
        actual_path = os.getcwd().replace("\\", "/")
        if actual_path.endswith("/"):
            path_output = actual_path + "input_video.mp4"
        else:
            path_output = actual_path + "/input_video.mp4"
        if not(os.path.exists(path_ffmpeg) and os.path.exists(path_image) and os.path.exists(path_video)):
            QMessageBox.critical(self, "Problem with paths", "Some paths do not exists", QMessageBox.Ok, QMessageBox.Ok)
            return False
        try:
            # Size of video
            subprocess_text = f'"{path_ffmpeg}/ffprobe" -v error -select_streams v:0 -show_entries stream=width,height -of csv=s=x:p=0 "{path_video}"'
            return_size = subprocess.check_output(subprocess_text)
            width, height = return_size.decode().split("\r")[0].split("x")
            width, height = int(width), int(height)


            # Transform image with extension of video
            extension_video = "." +path_video.split(".")[-1]
            subprocess_image_text = f'"{path_ffmpeg}/ffmpeg" -loop 1 -i "{path_image}" -c:v libx264 -t {self._duration_answer.getTime()} -pix_fmt yuv420p -vf scale={width}:{height} "{actual_path}/image{extension_video}"'
            subprocess.call(subprocess_image_text)

            # Transform video
            start = self._start_video.getTime()
            extension_video = "." +path_video.split(".")[-1]
            subprocess_video_text = f'"{path_ffmpeg}/ffmpeg" -i "{path_video}" -ss {start} -to {QTimerClock.addTimer(self._timer_video.getTime(), start)} -c:v libx264 -crf 23 "{actual_path}/video{extension_video}"'
            subprocess.call(subprocess_video_text)

            # Merge video and image
            subprocess_merge = f'"{path_ffmpeg}/ffmpeg" -i "{actual_path}/video{extension_video}" -i "{actual_path}/image{extension_video}" -filter_complex "[0:v][1:v] concat=n=2:v=1:a=0 [outv] " -vsync 2 -map "[outv]" "{path_output}"'
            subprocess.call(subprocess_merge)
            os.remove(f'{actual_path}/video{extension_video}')
            os.remove(f'{actual_path}/image{extension_video}')
            return True
        except Exception as e:
            QMessageBox.critical(self, "Convertion problem", f"{type(e)} - {str(e)}", QMessageBox.Ok, QMessageBox.Ok)
            return False