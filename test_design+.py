# надстройка на дизайном для обработки и анализа видео (и по совместительству ОСНОВНАЯ ПРОГА)

import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets, QtGui, QtMultimedia, QtCore
import design  # Это наш конвертированный файл дизайна
import os
import cv2


class ExampleApp(QtWidgets.QMainWindow, design.Ui_MainWindow):
    photoClicked = QtCore.pyqtSignal(QtCore.QPoint)
    rectChanged = QtCore.pyqtSignal(QtCore.QRect)
    moved = QtCore.pyqtSignal(int)    ###########################

    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна

        ########################################################################################################
        self.rubberBand = QtWidgets.QRubberBand(QtWidgets.QRubberBand.Rectangle, self)
        # self.setMouseTracking(True)
        self.origin = QtCore.QPoint()
        self.changeRubberBand = False

        self._zoom = 0
        self._empty = True
        self._scene = QtWidgets.QGraphicsScene(self)  # ???????

        self.var_that_means_nothing = 0

        # self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        # self.setResizeAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        ########################################################################################################

        # ПЕРЕМЕННЫЕ ДЛЯ ЛАП
        self.paw_centers = {1 : [],     ## 1 - Левая задняя
                            2 : [],      # 2 - Левая передняя
                            3 : [],      # 3 - Правая передняя
                            4 : []}     ## 4 - Правая задняя

        # OPEN / SAVE
        self.btnBrowse_3.clicked.connect(self.browse_folder)  # Open file
        self.actionOpen.triggered.connect(self.browse_folder)  # Open option from upper menu
        self.actionOpen.setStatusTip('Open File')  # !Status bar was not created in this version
        self.btnSave.clicked.connect(self.extract_values)  # Save paws coordinates
        self.actionSave_as.triggered.connect(self.extract_values)  # Save option from upper menu
        self.actionSave_as.setStatusTip('Save file as')  # !Status bar was not created in this version



        self.actionAbout.triggered.connect(self.about_popup)

        # self.left = 100
        # self.top = 100
        # self.width = 1080
        # self.height = 480
        # self.setGeometry(self.left, self.top, self.width, self.height)
        self.dial_text = {1:self.label_12.text(),
                        2:self.label_11.text(),
                        3:self.label_13.text(),
                        4:self.label_14.text()}  # устанавливаем соответствие значению DIAL'а и тексту соответствующей метки
        self.dial_3.valueChanged.connect(self.sliderMoved)  # действия при вращении DIAL'а
        self.btnUndo_3.clicked.connect(self.undo_paws)  # очистка всех сохранённых координат лап и лога

        self.videoPlayer = QtMultimedia.QMediaPlayer()  # create media player object
        # print(isinstance(self.videoPlayer, QtMultimedia.QMediaPlayer))
        # print(Viewer.mro())
        # print(issubclass(Viewer, QtMultimedia.QMediaContent))
        # print('\n\n')
        self.videoPlayer.setVideoOutput(self.wgt_player)  # где будет воспроизоводиться видео


        self.btnPlay.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_MediaPlay))  # PLAY
        self.btnPlay.clicked.connect(self.play_video)  # работа кнопки проигрывателя

        self.btnPrevFrame.setIcon(
                self.style().standardIcon(QtWidgets.QStyle.SP_MediaSeekBackward)        # PREV FRAME
            )
        self.btnPrevFrame.clicked.connect(self.prevVideoframe)

        self.btnNextFrame.setIcon(
                self.style().standardIcon(QtWidgets.QStyle.SP_MediaSeekForward)         # PREV FRAME
            )
        self.btnNextFrame.clicked.connect(self.nextVideoframe)



        
        self.videoPlayer.mediaStatusChanged.connect(self.set_position)    ###########################3

        self.duration_vid = 0  # длительность видео в начале, нужно для NEXT FRAME/PREV FRAME
        self.current_pos = 0  # отслеживание текущей позиции скроллера
        self.step_vid = self.duration_vid/1000  # задаём шаг фрэймов = 1cек
        print(self.duration_vid)
        print(self.current_pos)
        print(self.step_vid)
        

        self.videoSlider.sliderMoved[int].connect(self.moved.emit) ##################################################
        self.videoSlider.sliderMoved.connect(self.set_position)  # движение слайдера вручную
        self.videoPlayer.stateChanged.connect(self.mediastate_changed)  # изменение картиночек кнопки
        self.videoPlayer.positionChanged.connect(self.position_changed)
        self.videoPlayer.durationChanged.connect(self.duration_changed)



        self.cmbStyle.activated[str].connect(self.style_choice)  # стиль приложения

        # self.viewer = Viewer(self)  #################################################################
        # VBlayout = QtWidgets.QVBoxLayout(self)  #####################################################
        # self.verticalLayout_12.addWidget(self.viewer)  ############################################################
        # self.viewer.fitInView()



    def browse_folder(self):
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Выберите файл")
        # открыть диалог выбора файла и установить значение переменной
        # равным файлу (кортеж формата file_name = (файл, путь))

        if file_name:  # не продолжать выполнение, если пользователь не выбрал файл
            self.videoPlayer.setMedia(QtMultimedia.QMediaContent(QtCore.QUrl.fromLocalFile(file_name)))  # добавить видео
            self.videoPlayer.play()  # воспроизводить видео

            self.textEdit.clear()  # Clear log field
            self.paw_centers = {1 : [],     ##
                            2 : [],      # CLEAR
                            3 : [],      # DICTIONARY
                            4 : []}     ##

            self.textEdit.append("Открыт файл: "+file_name)  # добавить сообщение об открытии файла в textEdit 
            
        print(self.moved)

    def about_popup(self):
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle("About program...")
        msg.setText("If there is any issue please let me know:\nJust@Kidding.idc")
        x = msg.exec_()


    def extract_values(self):
        file_name, _ = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File')
        if file_name:
            with open(file_name, 'w') as f:
                for i in range(4):
                    f.write(str(self.dial_text[i+1]) 
                        + " лапа: " 
                        + str(self.paw_centers[i+1])
                        + "\n")
                self.textEdit.append("Координаты лап были успешно записаны в " + str(file_name))
        

    def style_choice(self, text):
        QtWidgets.QApplication.setStyle(QtWidgets.QStyleFactory.create(text))


    def play_video(self):
        if self.videoPlayer.state() == QtMultimedia.QMediaPlayer.PlayingState:
            self.videoPlayer.pause()

        else:
            self.videoPlayer.play()
        print('play video')


    def nextVideoframe(self):
        if self.duration_vid - self.current_pos > self.step_vid:  # если ещё не конец видоса -- переходим на NEXT FRAME
            self.current_pos += self.step_vid
            self.videoSlider.setValue(self.current_pos)
            self.videoPlayer.setPosition(self.current_pos)
            self.moved[int].connect(self.videoPlayer.setPosition)
            print(self.current_pos, int(self.current_pos))

        else:  # если уже конец видоса (или до конца меньше чем 1 шаг) -- устанавливаем позицию ползунка в самый конец
            self.current_pos = self.duration_vid
            self.videoSlider.setValue(self.current_pos)
            self.videoPlayer.setPosition(self.current_pos)

    def prevVideoframe(self):
        pass


    def mediastate_changed(self, state):
        if self.videoPlayer.state() == QtMultimedia.QMediaPlayer.PlayingState:
            self.btnPlay.setIcon(
                self.style().standardIcon(QtWidgets.QStyle.SP_MediaPause)
            )

        else:
            self.btnPlay.setIcon(
                self.style().standardIcon(QtWidgets.QStyle.SP_MediaPlay)
            )
        print('mediastate')


    def position_changed(self, position):
        self.videoSlider.setValue(position/1000)
        self.current_pos = position/1000
        print(self.current_pos)


    def duration_changed(self, duration):
        self.videoSlider.setRange(0, duration/1000)
        self.duration_vid = duration/1000  # задаём длительность видео, нужно для перехода на NEXT FRAME\PREV FRAME
        self.step_vid = self.duration_vid/1000  # задаём шаг фрэймов = 1сек
        print(self.duration_vid)


    def set_position(self, position):   #################################################################
        if self.videoPlayer.mediaStatus() == QtMultimedia.QMediaPlayer.BufferedMedia:
            self.videoPlayer.positionChanged.connect(self.position_changed)
            self.moved[int].connect(self.videoPlayer.setPosition)
        # self.videoPlayer.setPosition(position)
        self.current_pos = position/1000


    def sliderMoved(self):
        self.textEdit.append("Dial value = %i, %s" % (self.dial_3.value(), self.dial_text[self.dial_3.value()]))  # добавить сообщение о выборе в textEdit
        self.textEdit.append("Сейчас в ней: " + str(self.paw_centers[self.dial_3.value()]))


    def undo_paws(self):
        self.textEdit.clear()  # Clear log field
        self.paw_centers = {1 : [],     ##
                            2 : [],      # CLEAR
                            3 : [],      # DICTIONARY
                            4 : []}     ##
        self.textEdit.append("Координаты были стёрты, теперь тут пусто: " + str(self.paw_centers))


    #######################################################################################################################################
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.origin = event.pos()
            self.rubberBand.setGeometry(QtCore.QRect(self.origin, QtCore.QSize()))
            self.rectChanged.emit(self.rubberBand.geometry())
            self.rubberBand.show()
            self.changeRubberBand = True
            return
        else:
            self.textEdit.append('Лишние кнопки не жми, э')

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.changeRubberBand = False
            if self.rubberBand.isVisible():
                self.rubberBand.hide()

                # ОБСЧЁТ КООРДИНАТ. МОЖНО КАК СТАВИТЬ ТОЧКУ, ТАК И ВЫДЕЛЯТЬ ЛАПУ В ПРЯМОУГОЛЬНИК
                x_start = self.origin.x()
                y_start = self.origin.y()
                x_finish = event.pos().x()
                y_finish = event.pos().y()
                x_center = (x_finish + x_start)/2
                y_center = (y_finish + y_start)/2
                self.textEdit.append('Выделено от (%d, %d) до (%d, %d). Центр в (%d, %d)' % 
                    (x_start, y_start, x_finish, y_finish, x_center, y_center))

                # ЗАПИСАТЬ ЦЕНТР В СЛОВАРЬ ДЛЯ ЛАПЫ
                self.paw_centers[self.dial_3.value()].append((x_center, y_center))
                self.textEdit.append('Значение центра записано: ' + str(self.paw_centers[self.dial_3.value()]))

    def mouseMoveEvent(self, event):
        if self.changeRubberBand:
            self.rubberBand.setGeometry(QtCore.QRect(self.origin, event.pos()).normalized())
            self.rectChanged.emit(self.rubberBand.geometry())
            # QtWidgets.QGraphicsView.mouseMoveEvent(self, event)
        # super(Viewer, self).mouseMoveEvent(event)
    ###########################################################################################################################################


def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ExampleApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    sys.exit(app.exec_())  # я хер знает нужна ли эта строчка

if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()