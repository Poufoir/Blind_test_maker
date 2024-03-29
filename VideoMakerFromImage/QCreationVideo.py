
from typing import Optional, Callable
import os
import subprocess
from pytube import YouTube

from PySide6.QtWidgets import QMainWindow, QWidget, QLineEdit, QLabel, QGridLayout, QGroupBox, QPushButton, QVBoxLayout, QFileDialog, QSpinBox, QMessageBox, QComboBox, QApplication
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon

from VideoMakerFromImage.QDialogTemp import QDialogAnswer, QDialogRemovePath
from VideoMakerFromImage.QDialogShowAnswer import QDialogShowAnswer
from VideoMakerFromImage.helper_classes import QTimerClock

class QMainUiWindow(QMainWindow):

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
    
        self.setWindowTitle("Video Maker")
        self.setMinimumSize(810,500)
        self.move(700,0)
        QApplication.setWindowIcon(QIcon(os.getcwd().replace("\\", "/") + "/VideoMakerFromImage/clipboard_image.png"))

        self._central_widget = QWidget(self)
        self.setCentralWidget(self._central_widget)
        self._layout = QVBoxLayout(self._central_widget)

        self._path_group = QGroupBox("Paths", self._central_widget)
        self._path_group.setStyleSheet("QGroupBox {border:1px solid black;}")

        self._layout_path = QGridLayout(self._path_group)

        self._path_windows_font = QLineEdit("C:/Windows", self._path_group, readOnly=True)
        self._path_windows_font.setPlaceholderText("Enter correct Path for Windows")
        self._browse_path_windows_font = QPushButton(self._path_group, text="...")
        self._browse_path_windows_font.clicked.connect(self.browse_path_windows_font)
        # Layout
        self._layout_path.addWidget(QLabel(self._path_group, text="Path for Windows :"), 0, 0)
        self._layout_path.addWidget(self._path_windows_font, 0, 1)
        self._layout_path.addWidget(self._browse_path_windows_font, 0, 2)

        self._path_ffmpeg_bin = QLineEdit("D:/ffmpeg-2022-04-18-git-d5687236ab-full_build/bin", self._path_group)
        self._path_ffmpeg_bin.setPlaceholderText("Enter correct Folder for ffmpeg bin")
        self._browse_path_ffmpeg = QPushButton(self._path_group, text="...")
        self._browse_path_ffmpeg.clicked.connect(self.browse_path_ffmpeg)
        # Layout
        self._layout_path.addWidget(QLabel(self._path_group, text="Path for ffmpeg bin :"), 1, 0)
        self._layout_path.addWidget(self._path_ffmpeg_bin, 1, 1)
        self._layout_path.addWidget(self._browse_path_ffmpeg, 1, 2)

        path_video = os.getcwd().replace("\\", "/") + "/VideoMakerFromImage/5 SECOND TIMER.mp4"
        self._path_video = QLineEdit(path_video, self._path_group)
        self._path_video.setPlaceholderText("Enter correct Path for Video")
        self._browse_path_video = QPushButton(self._path_group, text="...")
        self._browse_path_video.clicked.connect(self.browse_path(self._path_video))
        # Layout
        self._layout_path.addWidget(QLabel(self._path_group, text="Path for Video :"), 2, 0)
        self._layout_path.addWidget(self._path_video, 2, 1)
        self._layout_path.addWidget(self._browse_path_video, 2, 2)

        path_image = os.getcwd().replace("\\", "/") + "/VideoMakerFromImage/sunrise.webp"
        self._path_image = QLineEdit(path_image, self._path_group)
        self._path_image.setPlaceholderText("Image Path")
        self._browse_path_image = QPushButton(self._path_group, text="...")
        self._browse_path_image.clicked.connect(self.browse_path(self._path_image))
        # Layout
        self._layout_path.addWidget(QLabel(self._path_group, text="Path for Image :"), 3, 0)
        self._layout_path.addWidget(self._path_image, 3, 1)
        self._layout_path.addWidget(self._browse_path_image, 3, 2)

        path_output = os.getcwd().replace("\\", "/") + "/VideoMakerFromImage"
        self._path_output = QLineEdit(path_output, self._path_group)
        self._path_output.setPlaceholderText("Enter correct Path for Output")
        self._browse_path_output = QPushButton(self._path_group, text="...")
        self._browse_path_output.clicked.connect(self.browse_path(self._path_output, False))
        # Layout
        self._layout_path.addWidget(QLabel(self._path_group, text="Folder for Output :"), 4, 0)
        self._layout_path.addWidget(self._path_output, 4, 1)
        self._layout_path.addWidget(self._browse_path_output, 4, 2)

        self._output_name = QLineEdit("output", self._path_group)
        self._output_name.setPlaceholderText("Enter correct Path for Output")
        list_output_extension = [".mp4", ".avi", ".mkv"]
        self._output_extension = QComboBox(self._path_group)
        self._output_extension.addItems(list_output_extension)
        self._output_extension.setEditable(True)
        # Layout
        self._layout_path.addWidget(QLabel(self._path_group, text="Output Name :"), 5, 0)
        self._layout_path.addWidget(self._output_name, 5, 1)
        self._layout_path.addWidget(self._output_extension, 5, 2)



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

        self._color_setting = QComboBox(self._video_group, editable=True)
        color_list = ["Beige", "Black", "Blue", "Brown", "Cyan", "Gray", "Green", "Magenta", "Orange", "Pink", "Red", "Violet", "White", "Yellow", "0xFFFFFF"]
        self._color_setting.addItems(color_list)
        self._color_setting.setCurrentText("Red")
        # Layout
        self._layout_video.addWidget(QLabel(self._video_group, text="Color of Answer :"), 2, 0)
        self._layout_video.addWidget(self._color_setting, 2, 1)

        self._size_setting = QSpinBox(self._video_group, value=90, maximum = 500, minimum = 10)
        # Layout
        self._layout_video.addWidget(QLabel(self._video_group, text="Size of Answer :"), 3, 0)
        self._layout_video.addWidget(self._size_setting, 3, 1)

        self._font_setting = QComboBox(self._video_group)
        self._change_fonts_display()
        # Layout
        self._layout_video.addWidget(QLabel(self._video_group, text="Font of Answer :"), 4, 0)
        self._layout_video.addWidget(self._font_setting, 4, 1)

        self._layout_video.setColumnStretch(1, 4)

        self._valid_creation_video = QPushButton(self._central_widget, text="Create Video")
        self._valid_creation_video.clicked.connect(self.createVideo)


        self._layout.addWidget(self._path_group)
        self._layout.addWidget(self._video_group)
        self._layout.addWidget(self._answer_group)
        self._layout.addWidget(self._valid_creation_video)

    def browse_path_windows_font(self) -> None:
        folder_path = QFileDialog.getExistingDirectory(self, 'Windows Caption')

        if folder_path != '' and "Fonts" in os.listdir(folder_path):
            self._path_windows_font.setText(folder_path)
            self._change_fonts_display()
        return

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
    
    def browse_path(self, widget:QLineEdit, file:bool = True)-> Callable[[], None]:
        def change_text() -> None:
            text = ""
            if file:
                file_path = QFileDialog.getOpenFileName(self, 'Video Caption', filter="(*.mp4);;(*.*)")

                if file_path[0] != '':
                    text = file_path[0]
            else:
                folder_path = QFileDialog.getExistingDirectory(self, 'Video Caption')

                if folder_path != '':
                    text = folder_path
            widget.setText(text)
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
            answer = answer_input_dialog.getMusictoRemove()
            if not isinstance(answer, str):
                for row in range(answer[0], answer[1]+1):
                    self._answer_dialog.deleteAnswer(answer[0])
            else:
                self._answer_dialog.deleteAnswer(answer)
    
    def _change_fonts_display(self) -> None:
        font_path = self._path_windows_font.text()
        if os.path.isdir(font_path) and "Fonts" in os.listdir(font_path):
            font_files = [file for file in os.listdir(font_path + "/Fonts") if file.endswith(".ttf")]
            current_font = self._font_setting.currentText()
            self._font_setting.clear()
            self._font_setting.addItems(font_files)
            self._font_setting.setCurrentText(current_font) if current_font != '' else self._font_setting.setCurrentText("arial.ttf")
    
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
            fontcolor = self._color_setting.currentText()
            fontfile_no_escape = self._path_windows_font.text() + "/Fonts/" + self._font_setting.currentText()
            temp_font_file = fontfile_no_escape.split(":")
            if len(temp_font_file) == 1 :
                fontfile = fontfile_no_escape
            elif len(temp_font_file) == 2:
                fontfile = temp_font_file[0] + "\\\\:" + temp_font_file[1]
            else:
                raise
            path_video_output = self._path_output.text() + "//" + self._output_name.text() + self._output_extension.currentText()
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
                draw_text_cmd += f""" ;[outv] drawtext=enable='between(t,{QTimerClock.toSeconds(start_answer)},{QTimerClock.toSeconds(end_answer)})':fontfile={fontfile}:text='{music_name}':x=(w-text_w)/2:y=(h-text_h)/2:fontsize={size}:fontcolor={fontcolor},"""
                draw_text_cmd += f"""drawtext=enable='between(t,{QTimerClock.toSeconds(start_answer)},{QTimerClock.toSeconds(end_answer)})':fontfile={fontfile}:text='{singer}':x=(w-text_w)/2:y=(h+text_h)/2:fontsize={size}:fontcolor={fontcolor}[outv]"""

                def add_music(music:str, music_file:str, separation_seconds:str, row_text_cmd:str):
                    music = music.replace("\\", "/")
                    music_file += f"""-i "{music}" """
                    separation_seconds += f"""[{row+n}:a] atrim=start={start}:end={end_music},asetpts=PTS-STARTPTS[music_row{row}];"""
                    row_text_cmd += f"[music_row{row}] "
                    return music_file, separation_seconds, row_text_cmd

                if os.path.exists(music):
                    music_file, separation_seconds, row_text_cmd = add_music(music, music_file, separation_seconds, row_text_cmd)
                elif music.startswith("https://www.youtube.com/"):
                    try:
                        yt = YouTube(music)
                        title = f"{music_name} - {singer}.mp3"
                        music_directory = os.getcwd().replace("\\", "/") + f"/VideoMakerFromImage/Download_Youtube_Music"
                        music = music_directory + "/" + title
                        if not os.path.exists(music):
                            video_downloaded = yt.streams.filter(only_audio=True).first().download(music_directory)
                            print(f"video download : {title}")
                            os.rename(video_downloaded, music)
                        music_file, separation_seconds, row_text_cmd = add_music(music, music_file, separation_seconds, row_text_cmd)
                    except Exception as e:
                        pass

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
        except Exception as e:
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