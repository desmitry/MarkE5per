from main_window import Ui_MainWindow
from settings_window import Ui_Settings
import sys
from PyQt5 import QtWidgets
from entities import SLASH, SCRIPT_PATH, Subject, Mark
from copy import deepcopy
import pickle

class Window(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.connectSignalsSlots()

        self.selected_subject = 0 #Subject('', [], 0, 0, [], [])
        try:
            self.load_bytes()
        except FileNotFoundError:
            pass

    def closeEvent(self, event):
        Subject.save()

    def connectSignalsSlots(self):
        self.tabWidget.setCurrentIndex(0)
        self.tabWidget.currentChanged.connect(self.setup_totalList_1_contents)
        self.settings.triggered.connect(self.show)
        self.listWidget.itemActivated.connect(self.setup_tweaking)
        self.totalList.itemActivated.connect(self.setup_totalList_2_contents)
        self.fiveSpinBox.valueChanged['int'].connect(self.fiveSlider.setValue)
        self.fourSpinBox.valueChanged['int'].connect(self.fourSlider.setValue)
        self.threeSpinBox.valueChanged['int'].connect(self.threeSlider.setValue)
        self.fiveSlider.valueChanged['int'].connect(self.fiveSpinBox.setValue)
        self.fourSlider.valueChanged['int'].connect(self.fourSpinBox.setValue)
        self.threeSlider.valueChanged['int'].connect(self.threeSpinBox.setValue)
        self.fiveSpinBox.valueChanged.connect(self.update_data)
        self.fourSpinBox.valueChanged.connect(self.update_data)
        self.threeSpinBox.valueChanged.connect(self.update_data)
        self.listWidget_2.itemChanged.connect(self.update_data)
        #self.saveButton.clicked.connect(self.save_tweaks)
        self.open.triggered.connect(self.load_file)
        self.last_opened.triggered.connect(self.load_bytes)
        self.settings.triggered.connect(self.open_settings)
        self.about.triggered.connect(self.show_about)

    def load_file(self):
        '''Load marks from .xlsx and configuration from bytes.'''
        Subject.load_excel(
            QtWidgets.QFileDialog.getOpenFileName(self, 'Открыть', filter='Excel files (*.xlsx)')[0]
        )
        try:
            with open(f'{SCRIPT_PATH}{SLASH}subjects', 'rb') as f:
                subjects_conf = pickle.load(f)
                subjects_conf.pop(-1)
                for subject_conf in subjects_conf:
                    for subject in Subject.subjects:
                        if subject_conf.name == subject.name:
                            subject.goal = subject_conf.goal
                            break
        except FileNotFoundError:
            pass
        Subject.save()
        self.setup_list_1_contents()

    def load_bytes(self):
        try:
            Subject.load()
            self.setup_list_1_contents()
        except FileNotFoundError:
            pass

    def open_settings(self):
        win = SettingsWindow()
        win.exec()
        self.setup_list_1_contents()

    def show_about(self):
        QtWidgets.QMessageBox.about(
            self,
            'О приложении',
            'Создано @desmitry.'
        )

    def update_rLabels(self, subject):
        goal = subject.goal - 1 + Subject.threshold
        self.averageLabel.setText(
            f'Средний балл: {subject.average:.2f}\nЦель: {goal}'
            )
        if subject.average >= goal:
            self.averageLabel.setStyleSheet('color: green; font: 24px;')
        else:
            self.averageLabel.setStyleSheet('font: 24px;')
        remaining = subject.return_remaining()
        if remaining[0]:
            self.rFiveLabel.setText(f'Требуется: {remaining[0]}')
        if remaining[1]:
            self.rFourLabel.setText(f'Требуется: {remaining[1]}')

    def update_data(self):
        '''Read user tweaks and update averageLabel and rLabel labels.'''
        subject = deepcopy(self.selected_subject)
        self.selected_subject.to_add.clear()
        self.selected_subject.to_remove.clear()
        for item in [self.listWidget_2.item(i) for i in range(self.listWidget_2.count())]:
            if item.checkState() == 2:
                for mark in subject.marks:
                    if (
                        item.text()[10] == str(mark.value)
                        and mark.date.isoformat() == item.text()[15:]
                    ):
                        self.selected_subject.to_remove.append(mark)
                        subject.marks.remove(mark)
                        break
                    elif (
                        mark.is_backlog
                        and mark.date.isoformat() == item.text()[16:]
                    ):
                        self.selected_subject.to_remove.append(mark)
                        subject.marks.remove(mark)
                        break
        for i in range(self.fiveSpinBox.value()):
            mark = Mark(5)
            self.selected_subject.to_add.append(Mark(5))
            subject.marks.append(mark)
        for i in range(self.fourSpinBox.value()):
            mark = Mark(4)
            self.selected_subject.to_add.append(Mark(4))
            subject.marks.append(mark)
        for i in range(self.threeSpinBox.value()):
            mark = Mark(3)
            self.selected_subject.to_add.append(Mark(3))
            subject.marks.append(mark)
        self.averageLabel.clear()
        self.rFiveLabel.clear()
        self.rFourLabel.clear()
        if subject.marks:
            subject.calculate_average()
            self.update_rLabels(subject)

#    def save_tweaks(self): # for saving tweaks with button
#        self.selected_subject.to_add.clear()
#        self.selected_subject.to_remove.clear()
#        for i in range(self.fiveSpinBox.value()):
#            self.selected_subject.to_add.append(Mark(5))
#        for i in range(self.fourSpinBox.value()):
#            self.selected_subject.to_add.append(Mark(4))
#        for i in range(self.threeSpinBox.value()):
#            self.selected_subject.to_add.append(Mark(3))
#        for item in [self.listWidget_2.item(i) for i in range(self.listWidget_2.count())]:
#            if item.checkState() == 2:
#                for mark in self.selected_subject.marks:
#                    if (
#                        int(item.text()[10]) == mark.value
#                        and mark.date.isoformat() == item.text()[15:25]
#                    ):
#                        self.selected_subject.to_remove.append(mark)
#                        break

    def setup_tweaking(self, current_item):
        '''Set up Slider and SpinBox widgets.'''
        def setup_list_2_contents(value):
            for mark in [mark for mark in subject.marks if mark.value == value]:
                item = QtWidgets.QListWidgetItem()
                if mark in subject.to_remove:
                    item.setCheckState(2)
                    subject.to_remove.remove(mark)
                else:
                    item.setCheckState(0)
                if not mark.is_backlog:
                    item.setText(f'Исправить {value} за {mark.date}')
                else:
                    item.setText(f'Закрыть долг за {mark.date}')
                self.listWidget_2.addItem(item)
        self.listWidget_2.clear()
        self.rFiveLabel.clear()
        self.rFourLabel.clear()
        self.averageLabel.clear()
        for subject in Subject.subjects:
            if subject.name == current_item.text():
                self.selected_subject = subject
                # apply saved values
                self.fiveSpinBox.blockSignals(True)
                self.fourSpinBox.blockSignals(True)
                self.threeSpinBox.blockSignals(True)
                self.fiveSpinBox.setValue(len([mark for mark in subject.to_add if mark.value == 5]))
                self.fourSpinBox.setValue(len([mark for mark in subject.to_add if mark.value == 4]))
                self.threeSpinBox.setValue(len([mark for mark in subject.to_add if mark.value == 3]))
                self.fiveSpinBox.blockSignals(False)
                self.fourSpinBox.blockSignals(False)
                self.threeSpinBox.blockSignals(False)
                if subject.marks:
                    setup_list_2_contents(2)
                    setup_list_2_contents(3)
                self.fiveSpinBox.valueChanged.emit(self.fiveSpinBox.value())
                self.fourSpinBox.valueChanged.emit(self.fourSpinBox.value())
                self.threeSpinBox.valueChanged.emit(self.threeSpinBox.value())
                if len([mark for mark in subject.marks if not mark.is_backlog]) < 3:
                    QtWidgets.QListWidgetItem(self.listWidget_2).setText(
                        f'Оценок до аттестации: {3 - len(subject.marks)}'
                    )
                break

    def setup_list_1_contents(self):
        '''Append relevant subjects to listWidget in tab_1.'''
        self.listWidget.clear()
        self.listWidget_2.clear()
        self.fiveSpinBox.setValue(0)
        self.fourSpinBox.setValue(0)
        self.threeSpinBox.setValue(0)
        self.rFiveLabel.clear()
        self.rFourLabel.clear()
        self.averageLabel.clear()
        for subject in Subject.subjects:
            if subject.goal:
                QtWidgets.QListWidgetItem(self.listWidget).setText(subject.name)
        self.listWidget.setCurrentRow(0)

    def setup_totalList_1_contents(self, current_tab):
        if current_tab == 1:
            self.totalList.clear()
            self.totalList_2.clear()
            for subject in Subject.subjects:
                if subject.to_add or subject.to_remove:
                    QtWidgets.QListWidgetItem(self.totalList).setText(subject.name)

    def setup_totalList_2_contents(self, current_item):
        self.totalList_2.clear()
        for subject in Subject.subjects:
            if subject.name == current_item.text():
                fives = len([mark for mark in subject.to_add if mark.value == 5])
                fours = len([mark for mark in subject.to_add if mark.value == 4])
                threes = len([mark for mark in subject.to_add if mark.value == 3])
                if fives:
                    QtWidgets.QListWidgetItem(self.totalList_2).setText(
                        f'Заработай "пять" в количестве: {fives}'
                    )
                if fours:
                    QtWidgets.QListWidgetItem(self.totalList_2).setText(
                        f'Заработай "четыре" в количестве: {fours}'
                    )
                if threes:
                    QtWidgets.QListWidgetItem(self.totalList_2).setText(
                        f'Заработай "три" в количестве: {threes}'
                    )
                for mark in subject.to_remove:
                    if not mark.is_backlog:
                        QtWidgets.QListWidgetItem(self.totalList_2).setText(
                            f'Исправь {mark.value} за {mark.date}'
                        )
                    else:
                        QtWidgets.QListWidgetItem(self.totalList_2).setText(
                            f'Закрой долг за {mark.date}'
                        )

class SettingsWindow(QtWidgets.QDialog, Ui_Settings):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.load_tweaks()
        self.connectSignalsSlots()
    def connectSignalsSlots(self):
        self.button_apply.clicked.connect(self.accept)
        self.button_cancel.clicked.connect(self.reject)

    def load_tweaks(self):
        '''Fill tableWidget with subjects and goals.'''
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(len(Subject.subjects))
        # first column
        for row, subject in enumerate(Subject.subjects, 0):
            item = QtWidgets.QTableWidgetItem(subject.name)
            self.tableWidget.setItem(row, 0, item)
        # second column
        for row, subject in enumerate(Subject.subjects):
            widget = QtWidgets.QComboBox()
            widget.addItems(('5', '4', 'Не учитывать'))
            text = subject.goal
            if not text:
                widget.setCurrentIndex(2)
            else:
                widget.setCurrentText(str(text))
            self.tableWidget.setCellWidget(row, 1, widget)

    def accept(self):
        '''Read values from the second column and write them to subjects.'''
        for row, subject in enumerate(Subject.subjects):
            selected = self.tableWidget.cellWidget(row, 1).currentText()
            if selected.isdigit():
                subject.goal = int(selected)
            else:
                subject.goal = 0
        Subject.threshold = self.doubleSpinBox.value()
        Subject.save()
        self.close()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())
