import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
import sqlite3
import add_mountain, style
from dateutil import parser


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
        self.mountains_table.setHorizontalHeaderItem(6, QTableWidgetItem("Date climbed"))
        self.mountains_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.mountains_table.horizontalHeader().setSectionResizeMode(6, QHeaderView.ResizeToContents)
        self.mountains_table.doubleClicked.connect(self.selected_mountain)

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

    def selected_mountain(self):
        global mountain_id
        mountain_list = []
        for i in range(0, 7):
            mountain_list.append(self.mountains_table.item(self.mountains_table.currentRow(), i).text())

        mountain_id = mountain_list[0]
        self.display = DisplayMountain()
        self.display.show()


class DisplayMountain(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(" Mountain Details")
        self.setWindowIcon(QIcon("icons/mountain.png"))
        self.setGeometry(500, 95, 575, 885)
        self.setFixedSize(self.size())
        self.UI()
        self.show()

    def UI(self):
        self.mountain_details()
        self.widgets()
        self.layouts()

    def mountain_details(self):
        global mountain_id
        query = "SELECT * FROM mountain WHERE id = ?"
        mountain = cur.execute(query, (mountain_id,)).fetchone()  # single item tuple = (1, )

        self.mountain_name = mountain[1]
        self.mountain_height = mountain[2]
        self.mountain_prom = mountain[3]
        self.mountain_long = mountain[4]
        self.mountain_lat = mountain[5]
        self.date_climbed = mountain[7]

    def widgets(self):
        ##### Top Layout Widgets #####
        self.mountain_img = QLabel()
        self.img = QPixmap("icons/mountain.png")
        self.mountain_img.setPixmap(self.img)
        self.mountain_img.setAlignment(Qt.AlignCenter)
        self.title_text = QLabel("Display Mountain")
        self.title_text.setAlignment(Qt.AlignCenter)

        # #### Bottom Layout Widgets #####
        self.name_entry = QLineEdit()
        self.name_entry.setText(self.mountain_name)
        self.height_entry = QLineEdit()
        self.height_entry.setText(str(self.mountain_height))
        self.prominence_entry = QLineEdit()
        self.prominence_entry.setText(str(self.mountain_prom))
        self.longitude_entry = QLineEdit()
        self.longitude_entry.setText(str(self.mountain_long))
        self.latitude_entry = QLineEdit()
        self.latitude_entry.setText(str(self.mountain_long))
        self.date_entry = QCalendarWidget()
        self.date_entry.setGridVisible(True)
        dc = parser.parse(self.date_climbed)
        self.date_entry.setSelectedDate(dc)
        self.delete_btn = QPushButton("Delete")
        self.delete_btn.clicked.connect(self.delete_mountain)
        self.update_btn = QPushButton("Update")
        self.update_btn.clicked.connect(self.update_mountain)

    def layouts(self):
        self.main_layout = QVBoxLayout()
        self.top_layout = QVBoxLayout()
        self.bottom_layout = QFormLayout()
        self.top_frame = QFrame()
        self.top_frame.setStyleSheet(style.top_frame_style())
        self.bottom_frame = QFrame()
        self.bottom_frame.setStyleSheet(style.bottom_frame_style())

        ##### Add Widgets #####
        self.top_layout.addWidget(self.title_text)
        self.top_layout.addWidget(self.mountain_img)
        self.top_frame.setLayout(self.top_layout)
        self.bottom_layout.addRow(QLabel("Name:"), self.name_entry)
        self.bottom_layout.addRow(QLabel("Height:"), self.height_entry)
        self.bottom_layout.addRow(QLabel("Prominence:"), self.prominence_entry)
        self.bottom_layout.addRow(QLabel("Longitude:"), self.longitude_entry)
        self.bottom_layout.addRow(QLabel("Latitude:"), self.latitude_entry)
        self.bottom_layout.addRow(QLabel("Climb Date: "), self.date_entry)
        self.bottom_layout.addRow(QLabel(""), self.delete_btn)
        self.bottom_layout.addRow(QLabel(""), self.update_btn)
        self.bottom_frame.setLayout(self.bottom_layout)
        self.main_layout.addWidget(self.top_frame)
        self.main_layout.addWidget(self.bottom_frame)

        self.setLayout(self.main_layout)

    def update_mountain(self):
        global mountain_id
        name = self.name_entry.text()
        height = self.height_entry.text()
        prominence = self.prominence_entry.text()
        longitude = self.longitude_entry.text()
        latitude = self.latitude_entry.text()
        date = self.date_entry.selectedDate().toString()

        if name and height and prominence and longitude and latitude != "":
            try:
                height = float(height)
                prominence = float(prominence)
                longitude = float(longitude)
                latitude = float(latitude)
                query = "UPDATE mountain SET name = ?, height = ?, prominence = ?, " \
                        "longitude = ?, latitude = ?, date_climbed = ? WHERE id = ?"
                cur.execute(query, (name, height, prominence, longitude, latitude, date, mountain_id))
                con.commit()
                QMessageBox.information(self, "Info", "Mountain has been updated")
                self.close()
            except Exception:
                QMessageBox.warning(self, 'Error', 'Invalid entry, input must be a number')
            except:
                QMessageBox.warning(self, "Warning", "Mountain has not been updated")
        else:
            QMessageBox.warning(self, "Warning", "Fields cannot be empty")

    def delete_mountain(self):
        global mountain_id
        mbox = QMessageBox.question(self, "Warning", "Are you sure you want to delete this mountain?",
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if mbox == QMessageBox.Yes:
            try:
                query = "DELETE FROM mountain WHERE id = ?"
                cur.execute(query, (mountain_id,))
                con.commit()
                QMessageBox.information(self, "Info", "Mountain has been deleted")
                self.close()
            except:
                QMessageBox.warning(self, "Warning", "Mountain has not been deleted")


def main():
    App = QApplication(sys.argv)
    window = Main()
    sys.exit(App.exec_())


if __name__ == "__main__":
    main()

# Icons made by "https://www.flaticon.com/authors/freepik"
