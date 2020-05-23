from PyQt5 import QtWidgets
import main.ui as design
import main.work_with_text as wt


class MyApp(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setup_ui(self)  # Включение интерфейса
        self.browser_1.clicked.connect(self.browse_folder_1)  # Если браузер1 нажата
        self.lineEdit_1.textChanged.connect(self.activate_browser_2)  # Активация браузер2 после указания 1го файла
        self.browser_2.clicked.connect(self.browse_folder_2)  # Если браузер2 нажата
        # Попытка активации кнопки старт после изменения текста в полях
        # Активирует, только если оба текста существуют
        self.lineEdit_2.textChanged.connect(self.activate_work_button)
        self.lineEdit_1.textChanged.connect(self.activate_work_button)
        self.workButton.clicked.connect(self.start_work)  # Если кнопка старта нажата
        self.comboBox.activated[str].connect(self.activate_check_box)  # Гистограмы только для варианта "Все"

    # Поиск первого файла
    def browse_folder_1(self):
        self.plainTextEdit_1.clear()
        file = QtWidgets.QFileDialog.getOpenFileName(self, 'Оберіть папку', filter='Exes (*.txt )')[0]
        if not file:
            self.lineEdit_1.clear()
            return
        self.lineEdit_1.setText(file)
        with open(file, 'r', encoding='utf8') as file:
            self.plainTextEdit_1.setPlainText(file.read())

    # Поиск второго файла
    def browse_folder_2(self):
        self.plainTextEdit_2.clear()
        file = QtWidgets.QFileDialog.getOpenFileName(self, 'Оберіть папку', filter='Exes (*.txt )')[0]
        if not file:
            self.lineEdit_2.clear()
            return
        self.lineEdit_2.setText(file)
        with open(file, 'r', encoding='utf8') as file:
            self.plainTextEdit_2.setPlainText(file.read())

    # Активация браузер2
    def activate_browser_2(self):
        self.browser_2.setEnabled(True)

    # Активация старта
    def activate_work_button(self):
        if self.lineEdit_2.text() != '' and self.lineEdit_1.text() != '':
            self.workButton.setEnabled(True)
        else:
            self.workButton.setEnabled(False)

    # Контроль доступности активации гистограм
    def activate_check_box(self):
        if self.comboBox.currentText() == 'Демонстрація усіх способів':
            self.checkBox.setEnabled(True)
        else:
            self.checkBox.setChecked(False)
            self.checkBox.setEnabled(False)

    # Выполнение основной задачи
    def start_work(self):
        wt.start_work(self)