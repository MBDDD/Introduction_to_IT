import psycopg2
import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QTabWidget, QAbstractScrollArea,
                             QVBoxLayout, QHBoxLayout, QTableWidget, QGroupBox, QTableWidgetItem)


class MainWindow(QWidget):
    def connect_to_db(self):
        self.conn = psycopg2.connect(database='lab8',
                                     user='postgres',
                                     password='mbdd',
                                     host='localhost',
                                     port='5432')
        self.cursor = self.conn.cursor()

    def __init__(self):
        super(MainWindow, self).__init__()
        # Название окна
        self.setWindowTitle('Shedule')
        # Подгоняем размеры окна
        self.vbox = QVBoxLayout(self)
        self.tabs = QTabWidget(self)  # Добавляем таблицу
        self.vbox.addWidget(self.tabs)

        # Подключаемся к БД
        self.connect_to_db()

        # Запрос на подсчёт количества схем в БД
        self.cursor.execute('SELECT schema_name FROM information_schema.schemata')
        info_schema = list(self.cursor.fetchall())
        schema = []
        for i in range(6, len(info_schema)):
            schema.append(info_schema[i][0])
        for i in range(len(schema)):  # от 1 до 2
            # Создание вкладки и присваивание ей название
            self.shedule_tab = QWidget()
            self.tabs.addTab(self.shedule_tab, schema[i])
            # Запрос на подсчёт количества таблиц в схеме
            self.cursor.execute(f"SELECT * FROM information_schema.tables WHERE table_schema = '{schema[i]}'")
            record = list(self.cursor.fetchall())
            table = []
            for n in range(len(record)):
                table.append(record[n][2])
            for j in range(len(record)):  # от 1 до 2
                self.create_shedule_tab(schema[i], table[j])

    def create_shedule_tab(self, schema, table):
        # Название подвкладки
        self.gbox = QGroupBox(table)
        self.svbox = QVBoxLayout()
        self.shbox1 = QHBoxLayout()
        self.shbox2 = QHBoxLayout()
        self.svbox.addLayout(self.shbox1)
        self.svbox.addLayout(self.shbox2)

        self.shbox1.addWidget(self.gbox)
        self.create_table(schema, table)
        self.shedule_tab.setLayout(self.svbox)
        # # Добавляем кнопки для обработки (Сохранить)
        # self.update_shedule_button = QPushButton('save')
        # self.shbox2.addWidget(self.update_shedule_button)
        # self.update_shedule_button.clicked.connect(self.update_table)

    def create_table(self, schema, table):
        self.table = QTableWidget()
        self.table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        # Запрос на получение названий столбцов
        self.cursor.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table}'")
        info = list(self.cursor.fetchall())
        column = []
        for i in range(len(info)):
            column.append(info[i][0])

        self.table.setColumnCount(len(column))
        self.table.setHorizontalHeaderLabels(column)
        self.update_table(schema, table)
        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(self.table)
        self.gbox.setLayout(self.mvbox)

    def update_table(self, schema, table):
        # Запрос на данные для заполнения в ячейки таблицы
        self.cursor.execute(f"SELECT * FROM {schema}.{table}")
        info = list(self.cursor.fetchall())
        # Количество строчек таблицы
        self.table.setRowCount(len(info))
        for i in range(len(info)):
            for j in range(len(info[0])):
                self.table.setItem(i, j, QTableWidgetItem(info[i][j]))
        self.table.resizeRowsToContents()


app = QApplication(sys.argv)
win = MainWindow()
win.show()
sys.exit(app.exec_())
