from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
import sqlite3, style, os
from PIL import Image

con = sqlite3.connect("mountains.db")
cur = con.cursor()

default_img = "mountain.png"


class AddMountain(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(" Add Mountain")
        self.setWindowIcon(QIcon("icons/mountain.png"))
        self.setGeometry(500, 95, 575, 885)
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
        self.longitude_entry.setPlaceholderText("Enter longitude coordinate")
        self.latitude_entry = QLineEdit()
        self.latitude_entry.setPlaceholderText("Enter latitude coordinate")
        self.area_combo = QComboBox()
        self.area_combo.addItems(["Dublin/Wicklow", "East Coast", "North Midlands", "Snowdonia"])
        self.date_entry = QCalendarWidget()
        self.date_entry.setGridVisible(True)
        self.upload_btn = QPushButton("Upload")
        self.upload_btn.clicked.connect(self.upload_img)
        self.submit_btn = QPushButton("Submit")
        self.submit_btn.clicked.connect(self.add_mountain)

    def layouts(self):
        self.main_layout = QVBoxLayout()
        self.top_layout = QVBoxLayout()
        self.bottom_layout = QFormLayout()
        self.top_frame = QFrame()
        self.top_frame.setStyleSheet(style.top_frame_style())
        self.bottom_frame = QFrame()
        self.bottom_frame.setStyleSheet(style.bottom_frame_style())

        ##### Add Widgets #####
        ##### Top Layout Widgets #####
        self.top_layout.addWidget(self.title_text)
        self.top_layout.addWidget(self.add_mountain_img)
        self.top_frame.setLayout(self.top_layout)

        ##### Bottom Layout Widgets #####
        self.bottom_layout.addRow(QLabel("Name: "), self.name_entry)
        self.bottom_layout.addRow(QLabel("Height (m): "), self.height_entry)
        self.bottom_layout.addRow(QLabel("Prominence (m): "), self.prom_entry)
        self.bottom_layout.addRow(QLabel("Longitude: "), self.longitude_entry)
        self.bottom_layout.addRow(QLabel("Latitude: "), self.latitude_entry)
        self.bottom_layout.addRow(QLabel("Area: "), self.area_combo)
        self.bottom_layout.addRow(QLabel("Climb Date: "), self.date_entry)
        self.bottom_layout.addRow(QLabel("Photo: "), self.upload_btn)
        self.bottom_layout.addRow(QLabel(""), self.submit_btn)
        self.bottom_frame.setLayout(self.bottom_layout)

        self.main_layout.addWidget(self.top_frame)
        self.main_layout.addWidget(self.bottom_frame)

        self.setLayout(self.main_layout)

    def add_mountain(self):
        global default_img
        name = self.name_entry.text()
        height = self.height_entry.text()
        prominence = self.prom_entry.text()
        longitude = self.longitude_entry.text()
        latitude = self.latitude_entry.text()
        area = self.area_combo.currentText()
        date = self.date_entry.selectedDate().toString()

        if name and height and prominence and longitude and latitude != "":
            try:
                height = float(height)
                prominence = float(prominence)
                longitude = float(longitude)
                latitude = float(latitude)
                query = "INSERT INTO 'mountain' (name, height, prominence, longitude, latitude, area, date_climbed, photo) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
                cur.execute(query, (name, height, prominence, longitude, latitude, area, date, default_img))
                con.commit()
                QMessageBox.information(self, "Info", "Mountain has been added")
                self.name_entry.setText("")
                self.height_entry.setText("")
                self.prom_entry.setText("")
                self.latitude_entry.setText("")
                self.longitude_entry.setText("")
            except Exception:
                QMessageBox.warning(self, 'Error', 'Invalid entry, input must be a number')
            except:
                QMessageBox.warning(self, "Info", "Mountain has not been added")
        else:
            QMessageBox.warning(self, "Info", "Fields cannot be empty!")

    def upload_img(self):
        global default_img
        size = (256, 256)
        self.filename, ok = QFileDialog.getOpenFileName(self, "Upload Image", "", "Image Files (*.jpg *.png)")
        if ok:
            default_img = os.path.basename(self.filename)
            img = Image.open(self.filename)
            img = img.resize(size)
            img.save("photos/{0}".format(default_img))
