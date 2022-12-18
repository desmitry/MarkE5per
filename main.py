from listview import Ui_MainWindow
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from settings import Ui_Settings
from entities import Subject, Mark
import copy


class Window(QMainWindow, Ui_MainWindow):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.connectSignalsSlots()
        self.selected_subject = None

    def connectSignalsSlots(self):
        #self.action_Exit.triggered.connect(self.close)
        #self.action_Find_Replace.triggered.connect(self.findAndReplace)
        #self.action_About.triggered.connect(self.about)
        self.tabWidget.setCurrentIndex(0)
        self.settings.triggered.connect(self.show)
        #self.applyButton.clicked.connect(self.update_data)
        self.listWidget.itemActivated.connect(self.setup_tweaking)
        self.fiveSpinBox.valueChanged['int'].connect(self.fiveSlider.setValue)
        self.fourSpinBox.valueChanged['int'].connect(self.fourSlider.setValue)
        self.threeSpinBox.valueChanged['int'].connect(self.threeSlider.setValue)
        self.fiveSlider.sliderMoved['int'].connect(self.fiveSpinBox.setValue)
        self.fourSlider.sliderMoved['int'].connect(self.fourSpinBox.setValue)
        self.threeSlider.sliderMoved['int'].connect(self.threeSpinBox.setValue)
        self.fiveSpinBox.valueChanged.connect(self.update_data)
        self.fourSpinBox.valueChanged.connect(self.update_data)
        self.threeSpinBox.valueChanged.connect(self.update_data)
        self.listWidget_2.itemChanged.connect(self.update_data)
        self.open.triggered.connect(self.open_file)
        self.last_opened.triggered.connect(self.open_bytes)
        self.settings.triggered.connect(self.open_settings)
        self.about.triggered.connect(self.show_about)

    def open_file(self):
        Subject.load_excel(
            QtWidgets.QFileDialog.getOpenFileName(self, 'Открыть', '/home')[0])
        self.setup_list_1_contents()

    def open_bytes(self):
        Subject.load()
        self.setup_list_1_contents()

    def open_settings(self):
        win = Settings_window()
        win.exec()

    def show_about(self):
        QtWidgets.QMessageBox.about(
            self,
            'О приложении',
            '''
            С великим удовольствием
            Приложение создавал @desmitry.
            '''
        )

    def update_data(self):
        subject = copy.deepcopy(self.selected_subject)
        for item in [self.listWidget_2.item(i) for i in range(self.listWidget_2.count())]:
            if item.checkState() == 2:
                for mark in subject.marks:
                    if (
                        int(item.text()[7]) == mark.value
                        and mark.date.isoformat() == item.text()[12:22]
                    ):
                        subject.marks.remove(mark)
        [subject.marks.append(Mark(5)) for i in range(self.fiveSpinBox.value())]
        [subject.marks.append(Mark(4)) for i in range(self.fourSpinBox.value())]
        [subject.marks.append(Mark(3)) for i in range(self.threeSpinBox.value())]
        self.averageLabel.clear()
        self.rFiveLabel.clear()
        self.rFourLabel.clear()
        if subject.marks:
            subject.calculate_average()
            self.averageLabel.setText(f'Средний балл: {subject.average}')
            remaining = subject.return_remaining()
            if remaining[0]:
                self.rFiveLabel.setText(f'Требуется: {remaining[0]}')
            if remaining[1]:
                self.rFourLabel.setText(f'Требуется: {remaining[1]}')


    def setup_tweaking(self, current_item):
        def setup_list_2_contents(value):
            unsatisfs = []
            for mark in subject.marks:
                if mark.value == value:
                    unsatisfs.append(mark)
            for mark in unsatisfs:
                item = QtWidgets.QListWidgetItem()
                item.setCheckState(0)
                item.setText(f'Убрать {value} за {mark.date}')
                self.listWidget_2.addItem(item)
        self.listWidget_2.clear()
        self.fiveSpinBox.setValue(0)        
        self.fourSpinBox.setValue(0)
        self.threeSpinBox.setValue(0)
        self.rFiveLabel.clear()
        self.rFourLabel.clear()
        self.averageLabel.clear()
        for subject in Subject.subjects:
            if subject.name == current_item.text():
                self.selected_subject = subject
                if subject.marks:
                    subject.calculate_average()
                    self.averageLabel.setText(
                        f'Средний балл: {subject.average}'
                    )
                    if subject.average < subject.goal - 1 + Subject.THRESHOLD:
                        remaining = subject.return_remaining()
                        if remaining[0]:
                            self.rFiveLabel.setText(f'Требуется: {remaining[0]}')
                        if remaining[1]:
                            self.rFourLabel.setText(f'Требуется: {remaining[1]}')
                        setup_list_2_contents(2)
                        setup_list_2_contents(3)
                else:
                    QtWidgets.QListWidgetItem(self.listWidget_2).setText(
                        'Оценок по предмету нет'
                    )

                    #    # создай слайдер/спинбокс с координатами (x, y + z)
                    #    # создай метку с количеством пятерок
                    #    # if subject.goal == 4
                    #        # создай слайдер/спинбокс с координатами (x, y + z)
                    #            # создай метку с количеством четверок#

    def setup_list_1_contents(self):
        self.listWidget.clear()
        self.listWidget_2.clear()
        self.fiveSpinBox.setValue(0)        
        self.fourSpinBox.setValue(0)
        self.threeSpinBox.setValue(0)
        self.rFiveLabel.clear()
        self.rFourLabel.clear()
        self.averageLabel.clear()
        for subject in Subject.subjects:
            QtWidgets.QListWidgetItem(self.listWidget).setText(subject.name)

class Settings_window(QtWidgets.QDialog, Ui_Settings):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.loadTweaks()
        self.connectSignalsSlots()

    def connectSignalsSlots(self):
        self.buttonBox.accepted.connect(self.accept) 
        self.buttonBox.rejected.connect(self.reject)

    def load_tweaks(self):
        pass
    
    def write_goals(self):
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())