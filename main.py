import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
import sqlite3
import add_mountain

con = sqlite3.connect("mountains.db")
cur = con.cursor()


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(" My Mountains")
        self.setWindowIcon(QIcon("icons/mountain.png"))
        self.setGeometry(450, 150, 1350, 750)
        self.setFixedSize(self.size())

        self.UI()
        self.show()

    def UI(self):
        self.tool_bar()
        self.tab_widget()
        self.widgets()
        self.layouts()
        self.display_mountains()

    def tool_bar(self):
        self.tb = self.addToolBar("Tool Bar")
        self.tb.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        ##### Toolbar Buttons #####
        ##### Add Mountain #########
        self.add_mountain = QAction(QIcon("icons/mountain.png"), "Add Mountain", self)
        self.tb.addAction(self.add_mountain)
        self.add_mountain.triggered.connect(self.func_add_mountain)
        self.tb.addSeparator()

    def tab_widget(self):
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        self.tab1 = QWidget()
        self.tabs.addTab(self.tab1, "Mountains")

    def widgets(self):
        ########################
        ##### Tab1 Widgets #####
        ########################

        ##### Main Left Layout Widget #####
        self.mountains_table = QTableWidget()
        self.mountains_table.setSortingEnabled(True)
        self.mountains_table.setColumnCount(7)
        self.mountains_table.setColumnHidden(0, True)
        self.mountains_table.setHorizontalHeaderItem(0, QTableWidgetItem("Mountain Id"))
        self.mountains_table.setHorizontalHeaderItem(1, QTableWidgetItem("Name"))
        self.mountains_table.setHorizontalHeaderItem(2, QTableWidgetItem("Height"))
        self.mountains_table.setHorizontalHeaderItem(3, QTableWidgetItem("Prominence"))
        self.mountains_table.setHorizontalHeaderItem(4, QTableWidgetItem("Longitude"))
        self.mountains_table.setHorizontalHeaderItem(5, QTableWidgetItem("Latitude"))
        self.mountains_table.setHorizontalHeaderItem(6, QTableWidgetItem("Date"))
        self.mountains_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.mountains_table.horizontalHeader().setSectionResizeMode(6, QHeaderView.ResizeToContents)
        #self.mountains_table.doubleClicked.connect(self.selected_mountain)

    def layouts(self):
        ########################
        ##### Tab1 layouts #####
        ########################

        self.main_layout = QHBoxLayout()
        self.main_left_layout = QVBoxLayout()

        ##### Add Widgets #####
        ##### Add Left Main Layout Widgets #####
        self.main_left_layout.addWidget(self.mountains_table)
        self.main_layout.addLayout(self.main_left_layout)
        self.tab1.setLayout(self.main_layout)

    def display_mountains(self):
        self.mountains_table.setFont(QFont("Arial", 10))
        for i in reversed(range(self.mountains_table.rowCount())):
            self.mountains_table.removeRow(i)

        query = cur.execute("SELECT id, name, height, prominence, longitude, latitude, date_climbed FROM mountain")
        for row_data in query:
            row_number = self.mountains_table.rowCount()
            self.mountains_table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.mountains_table.setItem(row_number, column_number, QTableWidgetItem(str(data)))

        self.mountains_table.setEditTriggers(QAbstractItemView.NoEditTriggers)  # prevents user editing table

    def func_add_mountain(self):
        self.new_mountain = add_mountain.AddMountain()


def main():
    App = QApplication(sys.argv)
    window = Main()
    sys.exit(App.exec_())


if __name__ == "__main__":
    main()

# Icons made by "https://www.flaticon.com/authors/freepik"
