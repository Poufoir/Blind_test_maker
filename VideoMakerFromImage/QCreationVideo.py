
from PySide6.QtWidgets import QMainWindow, QWidget, QLineEdit, QLabel, QGridLayout, QGroupBox, QPushButton, QVBoxLayout, QFileDialog, QDoubleSpinBox, QSpinBox
from PySide6.QtCore import Qt
from typing import Optional, Dict, Tuple, List, Callable
import os
import subprocess
from VideoMakerFromImage.QDialogTemp import QDialogAnswer, QDialogRemovePath
from VideoMakerFromImage.QDialogShowAnswer import QDialogShowAnswer

class QMainUiWindow(QMainWindow):

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
    
        self.setWindowTitle("Video Maker")
        self.setMinimumSize(700,500)
        self.move(700,0)

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
        self._browse_path_video.clicked.connect(self.browse_path(self._path_Video))

        self._layout_path.addWidget(self._label_path_Video, 1, 0)
        self._layout_path.addWidget(self._path_Video, 1, 1)
        self._layout_path.addWidget(self._browse_path_video, 1, 2)

        self._label_path_output = QLabel(self._path_group, text="Path for Output :")
        path_output = os.getcwd().replace("\\", "/") + "/output.mp4"
        self._path_output = QLineEdit(path_output, self._path_group)
        self._path_output.setPlaceholderText("Enter correct Path for Output")
        self._browse_path_output = QPushButton(self._path_group, text="...")
        self._browse_path_output.clicked.connect(self.browse_path(self._path_output))

        self._layout_path.addWidget(self._label_path_output, 2, 0)
        self._layout_path.addWidget(self._path_output, 2, 1)
        self._layout_path.addWidget(self._browse_path_output, 2, 2)



        self._answer_group = QGroupBox("Music", self._central_widget)
        self._layout.addWidget(self._answer_group)

        self._layout_answer = QGridLayout(self._answer_group)
        self._answer_dialog = QDialogShowAnswer(self)

        self._add_timer_from = QLabel(self._answer_group, text= "Add Answer (in second) from", alignment=Qt.AlignRight)
        self._timer_from = QDoubleSpinBox(self._answer_group, value=6.5)
        self._add_timer_to = QLabel(self._answer_group, text= "To", alignment=Qt.AlignRight)
        self._timer_to = QDoubleSpinBox(self._answer_group, value=10)

        self._layout_answer.addWidget(self._add_timer_from, 0, 0)
        self._layout_answer.addWidget(self._timer_from, 0, 1)
        self._layout_answer.addWidget(self._add_timer_to, 0, 2)
        self._layout_answer.addWidget(self._timer_to, 0, 3)

        self._add_answer = QPushButton(self._answer_group, text="Add Music and Answer")
        self._add_answer.clicked.connect(self.addPath)
        self._layout_answer.addWidget(self._add_answer, 1, 0, 1, 4)

        self._remove_answer = QPushButton(self._answer_group, text="Remove Music")
        self._remove_answer.clicked.connect(self.removePath)
        self._layout_answer.addWidget(self._remove_answer, 2, 0, 1, 4)

        self._show_answer = QPushButton(self._answer_group, text="Show Music and Answer")
        self._show_answer.clicked.connect(self.showPath)
        self._layout_answer.addWidget(self._show_answer, 3, 0, 1, 4)



        self._video_group = QGroupBox("Video", self._central_widget)
        self._layout.addWidget(self._video_group)
        self._layout_video = QGridLayout(self._video_group)

        self._label_color_setting = QLabel(self._video_group, text="Color of Answer :")
        self._color_setting = QLineEdit("red", self._video_group)
        self._layout_video.addWidget(self._label_color_setting, 0, 0)
        self._layout_video.addWidget(self._color_setting, 0, 1)

        self._label_size_setting = QLabel(self._video_group, text="Size of Answer :")
        self._size_setting = QSpinBox(self._video_group, value=90)
        self._layout_video.addWidget(self._label_size_setting, 1, 0)
        self._layout_video.addWidget(self._size_setting, 1, 1)
    


        self._valid_creation_video = QPushButton(self._central_widget, text="Create Video")
        self._valid_creation_video.clicked.connect(self.createVideo)
        self._layout.addWidget(self._valid_creation_video)

    def browse_path_ffmpeg(self) -> None:
        folder_path = QFileDialog.getExistingDirectory(self, 'ffmpeg Caption')

        if folder_path!= '':
            self._path_ffmpeg_bin.setText(folder_path)
        return
    
    def browse_path_Video(self) -> None:
        file_path = QFileDialog.getOpenFileName(self, 'Video Caption', filter="(*.mp4);;(*.*)")

        if file_path[0]!= '':
            self._path_Video.setText(file_path[0])
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
        n = len(self._answer_dialog)
        if n==0:
            return
        try:
            file_to_write = self._path_output.text()
            if os.path.exists(os.path.dirname(file_to_write)):
                myBat = open(file_to_write)
            else:
                myBat = open('./cmd_file.bat','w')
            timer = (self._timer_from.value(), self._timer_to.value())
            size = self._size_setting.value()
            fontcolor = self._color_setting.text()
            path_video_output = "C:/Users/clemeunier/Downloads/Video_test/CountDown_answer.mp4"
            myBat.write(self._path_ffmpeg_bin.text() + "/ffmpeg ")
            music_file =''
            music_separation_seconds = ''
            row_text_cmd = ''
            draw_text_cmd = ""
            for row in range(n):

                music, answer, start = self._answer_dialog.get_row(row)

                myBat.write(f"-i {self._path_Video.text()} ")
                row_text_cmd += f"[{row}:v] "
                draw_text_cmd += f""" ;[outv] drawtext=enable='between(t,{timer[0]+10*row},{timer[1]+10*row})':text='{answer}':x=(w-text_w)/2:y=(h-text_h)/2:fontsize={size}:fontcolor={fontcolor}[outv]"""

                if os.path.exists(music):
                    music = music.replace("\\", "/")
                    music_file += f"""-i "{music}" """
                    music_separation_seconds += f"""[{row+n}:a] atrim=start={start}:duration=10,asetpts=PTS-STARTPTS[music_row{row}];"""
                    row_text_cmd += f"[music_row{row}] "

            if music_file != '':
                myBat.write(music_file)
            myBat.write('-filter_complex "')
            if music_file != '':
                myBat.write(music_separation_seconds)
            myBat.write(row_text_cmd + f"concat=n={n}:v=1:a=1 [outv] [outa]")
            myBat.write(draw_text_cmd)
            myBat.write(""" " -map "[outv]" -map "[outa]" """)
            myBat.write(f"{path_video_output}")
            myBat.close()
        except Exception as e:
            pass
        try:
            path = os.getcwd().replace("\\", "/") + "/cmd_file.bat"
            subprocess.call([path])
        except:
            pass
        return