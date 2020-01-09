from UI.mainUI import Ui_MainWindow
from UI.addEditCoffeeForm import Ui_Form
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QWidget
import sqlite3


class MyWidget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        self.pushButton.clicked.connect(self.start)
        self.pushButton_2.clicked.connect(self.new_form)

    def loadTable(self, what, table_name="data/coffee.db"):
        con = sqlite3.connect(table_name)
        cur = con.cursor()
        result = cur.execute(f"""SELECT * FROM coffee
                            WHERE {what} = ?""", (self.lineEdit.text(),)).fetchall()
        result.sort(key=lambda x: x[0])
        self.tableWidget.setRowCount(1)
        for j, elem in enumerate(result[0]):
            self.tableWidget.setItem(0, j, QTableWidgetItem(str(elem)))
        self.tableWidget.resizeColumnsToContents()
        con.close()

    def start(self):
        if self.lineEdit.text() != '':
            self.loadTable(self.comboBox.currentText())
        else:
            self.loadTable(f"ID = 1")

    def new_form(self):
        self.second_form = SecondForm()
        self.second_form.show()


class SecondForm(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        self.pushButton.clicked.connect(self.new)
        self.pushButton_2.clicked.connect(self.update_data)

    def new(self):
        con = sqlite3.connect("data/coffee.db")
        cur = con.cursor()
        cur.execute(f"""INSERT INTO coffee VALUES({int(self.lineEdit.text())}, '{str(self.lineEdit_2.text())}',
         {int(self.lineEdit_3.text())}, '{str(self.lineEdit_4.text())}', '{str(self.lineEdit_5.text())}',
         {int(self.lineEdit_6.text())}, {float(self.lineEdit_7.text())})""")
        con.commit()

    def update_data(self):
        con = sqlite3.connect("data/coffee.db")
        cur = con.cursor()
        my_list = [int(self.lineEdit.text()), str(self.lineEdit_2.text()),
                   int(self.lineEdit_3.text()), str(self.lineEdit_4.text()), str(self.lineEdit_5.text()),
                   int(self.lineEdit_6.text()), float(self.lineEdit_7.text())]
        cur.execute(f"""UPDATE coffee SET NAME = '{my_list[1]}'
                             WHERE ID={my_list[0]}""")
        cur.execute(f"""UPDATE coffee SET degree_of_roasting = {my_list[2]}
                                     WHERE ID={my_list[0]}""")
        cur.execute(f"""UPDATE coffee SET ground_grains = '{my_list[3]}'
                                             WHERE ID={my_list[0]}""")
        cur.execute(f"""UPDATE coffee SET description_of_tasty = '{my_list[4]}'
                                             WHERE ID={my_list[0]}""")
        cur.execute(f"""UPDATE coffee SET PRICE = {my_list[5]}
                                             WHERE ID={my_list[0]}""")
        cur.execute(f"""UPDATE coffee SET V = {my_list[6]}
                                             WHERE ID={my_list[0]}""")
        con.commit()


app = QApplication(sys.argv)
ex = MyWidget()
ex.show()
sys.exit(app.exec_())
