from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
import sqlite3, style, os
from PIL import Image

con = sqlite3.connect("mountains.db")
cur = con.cursor()

default_img = "hiking.png"


class AddHike(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(" Add Hike")
        self.setWindowIcon(QIcon("icons/hiking.png"))
        self.setGeometry(500, 95, 575, 827)
        self.setFixedSize(self.size())
        self.UI()
        self.show()

    def UI(self):
        self.widgets()
        self.layouts()

    def widgets(self):
        ##### Widgets - Top Layout #####
        self.add_hike_img = QLabel()
        self.img = QPixmap("icons/hiking.png")
        self.add_hike_img.setPixmap(self.img)
        self.add_hike_img.setAlignment(Qt.AlignCenter)
        self.title_text = QLabel("Add Hike")
        self.title_text.setAlignment(Qt.AlignCenter)

        ##### Widgets - Bottom Layout #####
        self.length_entry = QLineEdit()
        self.length_entry.setPlaceholderText("Enter length of hike")
        self.duration_entry = QLineEdit()
        self.duration_entry.setPlaceholderText("hh:mm:ss")
        self.ascent_entry = QLineEdit()
        self.ascent_entry.setPlaceholderText("Enter total ascent")
        self.descent_entry = QLineEdit()
        self.descent_entry.setPlaceholderText("Enter total descent")
        self.note_entry = QTextEdit()
        self.note_entry.setPlaceholderText("Notes on hike go here.")
        self.note_entry.setStyleSheet(style.notes_style())
        self.date_entry = QCalendarWidget()
        self.date_entry.setGridVisible(True)
        self.upload_btn = QPushButton("Upload")
        self.upload_btn.clicked.connect(self.upload_img)
        self.submit_btn = QPushButton("Submit")
        self.submit_btn.clicked.connect(self.add_hike)

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
        self.top_layout.addWidget(self.add_hike_img)
        self.top_frame.setLayout(self.top_layout)

        ##### Bottom Layout Widgets #####
        self.bottom_layout.addRow(QLabel("Length (km): "), self.length_entry)
        self.bottom_layout.addRow(QLabel("Duration: "), self.duration_entry)
        self.bottom_layout.addRow(QLabel("Total ascent (m): "), self.ascent_entry)
        self.bottom_layout.addRow(QLabel("Total descent (m): "), self.descent_entry)
        self.bottom_layout.addRow(QLabel("Notes: "), self.note_entry)
        self.bottom_layout.addRow(QLabel("Hike Date: "), self.date_entry)
        self.bottom_layout.addRow(QLabel("Image: "), self.upload_btn)
        self.bottom_layout.addRow(QLabel(""), self.submit_btn)
        self.bottom_frame.setLayout(self.bottom_layout)

        self.main_layout.addWidget(self.top_frame)
        self.main_layout.addWidget(self.bottom_frame)

        self.setLayout(self.main_layout)

    def add_hike(self):
        length = self.length_entry.text()
        duration = self.duration_entry.text()
        ascent = self.ascent_entry.text()
        descent = self.descent_entry.text()
        note = self.note_entry.toPlainText()
        date = self.date_entry.selectedDate().toString()

        if length and duration and ascent and descent != "":
            try:
                length = float(length)
                ascent = float(ascent)
                descent = float(descent)
                query = "INSERT INTO 'hike' (length, duration, ascent, descent, note, date, image) VALUES (?, ?, ?, ?, ?, ?, ?)"
                cur.execute(query, (length, duration, ascent, descent, note, date, default_img))
                con.commit()
                QMessageBox.information(self, "Info", "Hike has been added")
                self.length_entry.setText("")
                self.duration_entry.setText("")
                self.ascent_entry.setText("")
                self.descent_entry.setText("")
                self.note_entry.setText("Notes on hike go here.")
            except Exception:
                QMessageBox.warning(self, 'Error', 'Invalid entry, input must be a number')
            except:
                QMessageBox.warning(self, "Info", "Hike has not been added")
        else:
            QMessageBox.warning(self, "Info", "Fields cannot be empty!")

    def upload_img(self):
        global default_img
        size = (512, 512)
        self.filename, ok = QFileDialog.getOpenFileName(self, "Upload Image", "", "Image Files (*.jpg *.png)")
        if ok:
            default_img = os.path.basename(self.filename)
            img = Image.open(self.filename)
            img = img.resize(size)
            img.save("images/{0}".format(default_img))