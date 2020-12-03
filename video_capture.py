import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import QVideoWidget

class SongSlider(QWidget):

    moved = pyqtSignal(int)
    print('initialize '+str(moved))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.slider = QSlider(Qt.Horizontal)
        self.slider.sliderMoved[int].connect(self.moved.emit)
        self.pos_lbl = QLabel()
        self.len_lbl = QLabel()

        hbox = QHBoxLayout(self)
        hbox.addWidget(self.pos_lbl)
        hbox.addWidget(self.slider)
        hbox.addWidget(self.len_lbl)

        print('__init__ '+str(self.moved))

    def setRange(self, value):
        self.slider.setRange(0, value)
        time = value / 1000
        self.len_lbl.setText('%02d:%02d' % (time // 60, time % 60))
        print('setRange '+str(self.moved))

    def setPos(self, value):
        self.slider.setValue(value)
        time = value / 1000
        self.pos_lbl.setText('%02d:%02d' % (time // 60, time % 60))
        print('setPos '+str(self.moved))


class Template(QWidget):

    def __init__(self):
        super().__init__()

        self.player = QMediaPlayer()

        self.slider = SongSlider()
        self.player.mediaStatusChanged.connect(self.set_slider)

        # self.playlist = QMediaPlaylist()
        self.playlist = QVideoWidget()

        # self.player.setPlaylist(self.playlist)
        self.player.setVideoOutput(self.playlist)

        btn = QPushButton('Open')
        btn.clicked.connect(self.load_song)

        btnNext = QPushButton('Next frame')
        btnNext.clicked.connect(self.next_frame)

        grid = QGridLayout(self)
        grid.addWidget(self.playlist, 0, 0)
        grid.addWidget(self.slider, 1, 0)
        grid.addWidget(btn, 2, 0, Qt.AlignLeft)
        grid.addWidget(btnNext, 2, 1, Qt.AlignLeft)
        self.playlist.setMinimumSize(QSize(431, 391))


    def set_slider(self):
        if self.player.mediaStatus() == QMediaPlayer.BufferedMedia:
            self.player.positionChanged.connect(self.slider.setPos)
            self.slider.moved[int].connect(self.player.setPosition)
            self.slider.setRange(self.player.duration())
            print('set slider '+str(self.slider.moved))

    def load_song(self):
        file, _ = QFileDialog.getOpenFileUrl(self, 'Choose song')
        if file:
            # self.playlist.addMedia(QMediaContent(file))
            self.player.setMedia(QMediaContent(file))

            self.player.play()
            print('load song'+str(self.slider.moved))


    def next_frame(self):             #################################################################3#
        if self.player.mediaStatus() == QMediaPlayer.BufferedMedia:
            self.player.positionChanged.connect(self.slider.setPos)
            self.slider.moved[int].connect(self.player.setPosition)
            self.slider.setRange(self.player.duration())
            print('set slider '+str(self.slider.moved))
###############################################

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = Template()
    gui.show()
    sys.exit(app.exec_())