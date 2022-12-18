# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
import functions
from entities import *


class Ui_MainWindow(object):
    def setup_tab_1_contents(self, Subject):
        for subject in Subject.subjects:
            if subject.average < subject.goal - 1 + Subject.THRESHOLD:
                last_ordinate = -20 # тут начальные координаты (x,y)
                shift = 30
                if 2 in [mark.value for mark in Subject.marks]:
                    twos = []
                    self.twoCheckBox_1 = None
                    self.twoCheckBox_2 = None
                    self.twoCheckBox_3 = None
                    self.twoCheckBox_4 = None
                    self.twoCheckBox_5 = None
                    checkboxes = [
                        self.twoCheckBox_1,
                        self.twoCheckBox_2,
                        self.twoCheckBox_3,
                        self.twoCheckBox_4,
                        self.twoCheckBox_5
                    ]
                    for mark in Subject.marks:
                        if mark.value == 2:
                            twos.append(mark)
                    for mark, checkbox in twos, checkboxes:
                        self.checkbox = QtWidgets.QCheckBox(self.tab_1)
                        self.checkbox.setGeometry(
                            QtCore.QRect(
                                10, last_ordinate + shift, 85, 22
                            )
                        )
                        self.checkbox.setObjectName("twoCheckBox")
                        self.checkbox.setText(f'Исправить двойку за {mark.date}')
                        #checked_action = subject.add_mark()
                        #unchecked_action = subject.add_mark()
                        #при изменении, сигналь объекту средний балл - обновиться
                remaining = subject.return_remaining()
                # создай слайдер/спинбокс с координатами (x, y + z)
                # создай метку с количеством пятерок
                # if subject.goal == 4
                    # создай слайдер/спинбокс с координатами (x, y + z)
                        # создай метку с количеством четверок#
    
    
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(650, 402)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(650, 402))
        MainWindow.setMaximumSize(QtCore.QSize(650, 402))
        MainWindow.setWindowTitle("MarkE5per")

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 651, 321))
        self.tabWidget.setObjectName("tabWidget")

        self.tab_1 = QtWidgets.QWidget()
        self.tab_1.setObjectName("tab_1")

        self.checkBox = QtWidgets.QCheckBox(self.tab_1)
        self.checkBox.setGeometry(QtCore.QRect(10, 10, 85, 22))
        self.checkBox.setObjectName("checkBox")

        
        
        self.horizontalSlider = QtWidgets.QSlider(self.tab_1)
        self.horizontalSlider.setGeometry(QtCore.QRect(10, 36, 261, 20))
        self.horizontalSlider.setFocusPolicy(QtCore.Qt.WheelFocus)
        self.horizontalSlider.setAutoFillBackground(False)
        self.horizontalSlider.setMaximum(10)
        self.horizontalSlider.setPageStep(1)
        self.horizontalSlider.setProperty("value", 0)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setTickPosition(QtWidgets.QSlider.NoTicks)
        self.horizontalSlider.setObjectName("horizontalSlider")
        
        self.spinBox = QtWidgets.QSpinBox(self.tab_1)
        self.spinBox.setGeometry(QtCore.QRect(280, 30, 51, 32))
        self.spinBox.setObjectName("spinBox")
        
        self.averageLabel = QtWidgets.QLabel(self.tab_1)
        self.averageLabel.setGeometry(QtCore.QRect(340, 10, 291, 261))
        self.averageLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.averageLabel.setWordWrap(False)
        self.averageLabel.setObjectName("averageLabel")
        
        self.tabWidget.addTab(self.tab_1, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tabWidget.addTab(self.tab_2, "")
        
        self.applyButton = QtWidgets.QPushButton(self.centralwidget)
        self.applyButton.setGeometry(QtCore.QRect(550, 330, 84, 34))
        self.applyButton.setObjectName("applyButton")
        
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 650, 30))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        MainWindow.setMenuBar(self.menubar)
        self.open = QtWidgets.QAction(MainWindow)
        self.open.setObjectName("open")
        self.settings = QtWidgets.QAction(MainWindow)
        self.settings.setObjectName("settings")
        self.menu.addAction(self.open)
        self.menu.addAction(self.settings)
        self.menubar.addAction(self.menu.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        self.spinBox.valueChanged['int'].connect(self.horizontalSlider.setValue) # type: ignore
        self.horizontalSlider.sliderMoved['int'].connect(self.spinBox.setValue) # type: ignore
        self.applyButton.clicked['int'].connect(self.averageLabel.update(functions.)) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        self.checkBox.setText(_translate("MainWindow", "CheckBox"))
        self.averageLabel.setText(_translate("MainWindow", "TextLabel"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_1), _translate("MainWindow", "Требуемые действия"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Допустимые действия"))
        self.applyButton.setText(_translate("MainWindow", "Применить"))
        self.menu.setTitle(_translate("MainWindow", "Файл"))
        self.open.setText(_translate("MainWindow", "Открыть..."))
        self.open.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.settings.setText(_translate("MainWindow", "Настройки"))
