from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
import sqlite3

con = sqlite3.connect("mountains.db")
cur = con.cursor()


class AddMountain(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(" Add Mountain")
        self.setWindowIcon(QIcon("icons/mountain.png"))
        self.setGeometry(550, 250, 400, 550)
        self.setFixedSize(self.size())
        self.UI()
        self.show()

    def UI(self):
        self.widgets()
        self.layouts()

    def widgets(self):
        ##### Widgets - Top Layout #####
        self.add_mountain_img = QLabel()
        self.img = QPixmap("icons/mountain.png")
        self.add_mountain_img.setPixmap(self.img)
        self.add_mountain_img.setAlignment(Qt.AlignCenter)
        self.title_text = QLabel("Add Mountain")
        self.title_text.setAlignment(Qt.AlignCenter)

        ##### Widgets - Bottom Layout #####
        self.name_entry = QLineEdit()
        self.name_entry.setPlaceholderText("Enter name of mountain")
        self.height_entry = QLineEdit()
        self.height_entry.setPlaceholderText("Enter height of mountain")
        self.prom_entry = QLineEdit()
        self.prom_entry.setPlaceholderText("Enter prominence of mountain")
        self.longitude_entry = QLineEdit()
        self.longitude_entry.setPlaceholderText("Enter longitude of mountain")
        self.latitude_entry = QLineEdit()
        self.latitude_entry.setPlaceholderText("Enter latitude of mountain")
        self.date_entry = QLineEdit()
        self.date_entry.setPlaceholderText("dd/mm/yyyy")
        self.submit_btn = QPushButton("Submit")
        self.submit_btn.clicked.connect(self.add_mountain)

    def layouts(self):
        self.main_layout = QVBoxLayout()
        self.top_layout = QVBoxLayout()
        self.bottom_layout = QFormLayout()
        self.top_frame = QFrame()
        self.bottom_frame = QFrame()

        ##### Add Widgets #####
        ##### Top Layout Widgets #####
        self.top_layout.addWidget(self.title_text)
        self.top_layout.addWidget(self.add_mountain_img)
        self.top_frame.setLayout(self.top_layout)

        ##### Bottom Layout Widgets #####
        self.bottom_layout.addRow(QLabel("Name: "), self.name_entry)
        self.bottom_layout.addRow(QLabel("Height: "), self.height_entry)
        self.bottom_layout.addRow(QLabel("Prominence: "), self.prom_entry)
        self.bottom_layout.addRow(QLabel("Longitude: "), self.longitude_entry)
        self.bottom_layout.addRow(QLabel("Latitude: "), self.latitude_entry)
        self.bottom_layout.addRow(QLabel("Date: "), self.date_entry)
        self.bottom_layout.addRow(QLabel(""), self.submit_btn)
        self.bottom_frame.setLayout(self.bottom_layout)

        self.main_layout.addWidget(self.top_frame)
        self.main_layout.addWidget(self.bottom_frame)

        self.setLayout(self.main_layout)

    def add_mountain(self):
        name = self.name_entry.text()
        height = self.height_entry.text()
        prominence = self.prom_entry.text()
        longitude = self.longitude_entry.text()
        latitude = self.latitude_entry.text()
        date = self.date_entry.text()


        if name and height and prominence and longitude and latitude and date != "":
            try:
                query = "INSERT INTO 'mountain' (name, height, prominence, longitude, latitude, date_climbed) VALUES (?, ?, ?, ?, ?, ?)"
                cur.execute(query, (name, height, prominence, longitude, latitude, date))
                con.commit()
                QMessageBox.information(self, "Info", "Mountain has been added")
                self.name_entry.setText("")
                self.height_entry.setText("")
                self.prom_entry.setText("")
                self.latitude_entry.setText("")
                self.longitude_entry.setText("")
                self.date_entry.setText("")
                con.close()
            except:
                QMessageBox.information(self, "Info", "Mountain has not been added")
        else:
            QMessageBox.information(self, "Info", "Fields cannot be empty!")