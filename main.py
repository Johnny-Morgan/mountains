import sys, os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
import sqlite3
import add_mountain, add_hike, style, map1
from dateutil import parser
from PIL import Image


con = sqlite3.connect("mountains.db")
cur = con.cursor()


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(" My Mountains")
        self.setWindowIcon(QIcon("icons/mountain.png"))
        self.setGeometry(300, 150, 1350, 750)
        self.setFixedSize(self.size())

        self.UI()
        self.show()

    def UI(self):
        self.tool_bar()
        self.tab_widget()
        self.widgets()
        self.layouts()
        self.display_mountains()
        self.display_hikes()
        self.get_statistics()

    def tool_bar(self):
        self.tb = self.addToolBar("Tool Bar")
        self.tb.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        ##### Toolbar Buttons #####
        ##### Add Mountain ########
        self.add_mountain = QAction(QIcon("icons/mountain.png"), "Add Mountain", self)
        self.tb.addAction(self.add_mountain)
        self.add_mountain.triggered.connect(self.func_add_mountain)
        self.tb.addSeparator()

        ##### Add Hike #####
        self.add_hike = QAction(QIcon("icons/hiking.png"), "Add Hike", self)
        self.tb.addAction(self.add_hike)
        self.add_hike.triggered.connect(self.func_add_hike)
        self.tb.addSeparator()

        ##### Generate Map #####
        self.generate_map = QAction(QIcon("icons/map.png"), "Generate Map", self)
        self.tb.addAction(self.generate_map)
        self.generate_map.triggered.connect(self.func_generate_map)
        self.tb.addSeparator()

    def tab_widget(self):
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        self.tab1 = QWidget()
        self.tabs.addTab(self.tab1, "Mountains")
        self.tab2 = QWidget()
        self.tabs.addTab(self.tab2, "Hikes")
        self.tab3 = QWidget()
        self.tabs.addTab(self.tab3, "Statistics")

    def widgets(self):
        ########################
        ##### Tab1 Widgets #####
        ########################

        ##### Main Left Layout Widget #####
        self.mountains_table = QTableWidget()
        self.mountains_table.setSortingEnabled(True)
        self.mountains_table.setColumnCount(8)
        self.mountains_table.setColumnHidden(0, True)
        self.mountains_table.setHorizontalHeaderItem(0, QTableWidgetItem("Mountain Id"))
        self.mountains_table.setHorizontalHeaderItem(1, QTableWidgetItem("Name"))
        self.mountains_table.setHorizontalHeaderItem(2, QTableWidgetItem("Height (m)"))
        self.mountains_table.setHorizontalHeaderItem(3, QTableWidgetItem("Prominence (m)"))
        self.mountains_table.setHorizontalHeaderItem(4, QTableWidgetItem("Longitude"))
        self.mountains_table.setHorizontalHeaderItem(5, QTableWidgetItem("Latitude"))
        self.mountains_table.setHorizontalHeaderItem(6, QTableWidgetItem("Area"))
        self.mountains_table.setHorizontalHeaderItem(7, QTableWidgetItem("Date Climbed"))
        self.mountains_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.mountains_table.horizontalHeader().setSectionResizeMode(6, QHeaderView.ResizeToContents)
        self.mountains_table.doubleClicked.connect(self.selected_mountain)

        ########################
        ##### Tab2 Widgets #####
        ########################

        ##### Main Left Layout Widget #####
        self.hikes_table = QTableWidget()
        self.hikes_table.setSortingEnabled(True)
        self.hikes_table.setColumnCount(7)
        self.hikes_table.setColumnHidden(0, True)
        self.hikes_table.setHorizontalHeaderItem(0, QTableWidgetItem("Hike Id"))
        self.hikes_table.setHorizontalHeaderItem(1, QTableWidgetItem("Length (km)"))
        self.hikes_table.setHorizontalHeaderItem(2, QTableWidgetItem("Duration"))
        self.hikes_table.setHorizontalHeaderItem(3, QTableWidgetItem("Total Ascent (m)"))
        self.hikes_table.setHorizontalHeaderItem(4, QTableWidgetItem("Total Descent (m)"))
        self.hikes_table.setHorizontalHeaderItem(5, QTableWidgetItem("Date"))
        self.hikes_table.setHorizontalHeaderItem(6, QTableWidgetItem("Notes"))
        self.hikes_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.hikes_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)
        self.hikes_table.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeToContents)
        self.hikes_table.horizontalHeader().setSectionResizeMode(6, QHeaderView.Stretch)
        self.hikes_table.doubleClicked.connect(self.selected_hike)

        ########################
        ##### Tab3 Widgets #####
        ########################
        self.total_hikes_label = QLabel()
        self.total_length_label = QLabel()
        self.total_time_label = QLabel()
        self.total_ascent_label = QLabel()
        self.total_descent_label = QLabel()
        self.avg_length_label = QLabel()
        self.avg_time_label = QLabel()
        self.avg_ascent_label = QLabel()
        self.avg_descent_label = QLabel()
        self.total_mountains_label = QLabel()
        self.total_hills_label = QLabel()
        self.dub_wick_label = QLabel()
        self.east_coast_label = QLabel()
        self.north_mid_label = QLabel()
        self.snowdonia_label = QLabel()

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

        ########################
        ##### Tab2 layouts #####
        ########################

        self.main_layout = QHBoxLayout()
        self.main_left_layout = QVBoxLayout()

        ##### Add Widgets #####
        ##### Add Left Main Layout Widgets #####
        self.main_left_layout.addWidget(self.hikes_table)
        self.main_layout.addLayout(self.main_left_layout)
        self.tab2.setLayout(self.main_layout)

        ########################
        ##### Tab3 layouts #####
        ########################
        self.statistics_main_layout = QVBoxLayout()
        self.statistics_left_layout = QFormLayout()
        self.statistics_right_layout = QFormLayout()
        self.main = QHBoxLayout()
        self.main.addLayout(self.statistics_left_layout)
        self.main.addLayout(self.statistics_right_layout)
        self.statistics_groupbox = QGroupBox("Statistics")
        self.statistics_right_layout.addRow(QLabel("\nHikes:"))
        self.statistics_right_layout.addRow("\nTotal Hikes: ", self.total_hikes_label)
        self.statistics_right_layout.addRow("Total Length: ", self.total_length_label)
        self.statistics_right_layout.addRow("Total Time: ", self.total_time_label)
        self.statistics_right_layout.addRow("Total Ascent: ", self.total_ascent_label)
        self.statistics_right_layout.addRow("Total Descent: ", self.total_descent_label)
        self.statistics_right_layout.addRow("Average Time: ", self.avg_time_label)
        self.statistics_right_layout.addRow("Average Length: ", self.avg_length_label)
        self.statistics_right_layout.addRow("Average Ascent: ", self.avg_ascent_label)
        self.statistics_right_layout.addRow("Average Descent: ", self.avg_descent_label)

        self.statistics_left_layout.addRow(QLabel("\nMountains:"))
        self.statistics_left_layout.addRow("\nTotal Mountains: ", self.total_mountains_label)
        self.statistics_left_layout.addRow("Total Hills (<500m): ", self.total_hills_label)
        self.statistics_left_layout.addRow(QLabel("Areas:"))
        self.statistics_left_layout.addRow("    Dublin/Wicklow:", self.dub_wick_label)
        self.statistics_left_layout.addRow("    East Coast:", self.east_coast_label)
        self.statistics_left_layout.addRow("    North Midlands:", self.north_mid_label)
        self.statistics_left_layout.addRow("    Snowdonia:", self.snowdonia_label)

        self.statistics_groupbox.setLayout(self.main)
        self.statistics_groupbox.setFont(QFont("Arial", 14))
        self.statistics_main_layout.addWidget(self.statistics_groupbox)
        self.tab3.setLayout(self.statistics_main_layout)

    def display_mountains(self):
        self.mountains_table.setFont(QFont("Arial", 10))
        for i in reversed(range(self.mountains_table.rowCount())):
            self.mountains_table.removeRow(i)

        query = cur.execute("SELECT id, name, height, prominence, longitude, latitude, area, date_climbed FROM mountain")
        for row_data in query:
            row_number = self.mountains_table.rowCount()
            self.mountains_table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.mountains_table.setItem(row_number, column_number, QTableWidgetItem(str(data)))

        self.mountains_table.setEditTriggers(QAbstractItemView.NoEditTriggers)  # prevents user editing table

    def display_hikes(self):
        self.hikes_table.setFont(QFont("Arial", 10))
        for i in reversed(range(self.hikes_table.rowCount())):
            self.hikes_table.removeRow(i)

        query = cur.execute("SELECT id, length, duration, ascent, descent, date, note FROM hike")
        for row_data in query:
            row_number = self.hikes_table.rowCount()
            self.hikes_table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.hikes_table.setItem(row_number, column_number, QTableWidgetItem(str(data)))

        self.hikes_table.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def func_add_mountain(self):
        self.new_mountain = add_mountain.AddMountain()

    def func_add_hike(self):
        self.new_hike = add_hike.AddHike()

    def func_generate_map(self):
        map1.generate_map()

    def selected_mountain(self):
        global mountain_id
        mountain_list = []
        for i in range(0, 8):
            mountain_list.append(self.mountains_table.item(self.mountains_table.currentRow(), i).text())

        mountain_id = mountain_list[0]
        self.display = DisplayMountain()
        self.display.show()

    def selected_hike(self):
        global hike_id
        hike_list = []
        for i in range(0, 6):
            hike_list.append(self.hikes_table.item(self.hikes_table.currentRow(), i).text())

        hike_id = hike_list[0]
        self.display = DisplayHike()
        self.display.show()

    def get_statistics(self):
        count_hikes = cur.execute("SELECT count(id) FROM hike").fetchall()
        count_length = cur.execute("SELECT SUM(length) FROM hike").fetchall()
        count_ascent = cur.execute("SELECT SUM(ascent) FROM hike").fetchall()
        count_descent = cur.execute("SELECT SUM(descent) FROM hike").fetchall()
        count_mountains = cur.execute("SELECT count(id) FROM mountain WHERE height >= 500").fetchall()
        count_hills = cur.execute("SELECT count(id) FROM mountain WHERE height < 500").fetchall()
        times = cur.execute("SELECT duration FROM hike").fetchall()
        count_dub_wick = cur.execute("SELECT COUNT(area) FROM mountain WHERE area = 'Dublin/Wicklow'").fetchall()
        count_east_coast = cur.execute("SELECT COUNT(area) FROM mountain WHERE area = 'East Coast'").fetchall()
        count_north_mid = cur.execute("SELECT COUNT(area) FROM mountain WHERE area = 'North Midlands'").fetchall()
        count_snowdonia = cur.execute("SELECT COUNT(area) FROM mountain WHERE area = 'Snowdonia'").fetchall()

        count_hikes = count_hikes[0][0]
        count_length = count_length[0][0]
        count_ascent = count_ascent[0][0]
        count_descent = count_descent[0][0]
        count_mountains = count_mountains[0][0]
        count_hills = count_hills[0][0]
        count_dub_wick = count_dub_wick[0][0]
        count_east_coast = count_east_coast[0][0]
        count_north_mid = count_north_mid[0][0]
        count_snowdonia = count_snowdonia[0][0]

        seconds = 0
        minutes = 0
        hours = 0
        # Calculate total time
        for time in times:
            seconds += int(time[0].split(":")[2])
            minutes += int(time[0].split(":")[1])
            hours += int(time[0].split(":")[0])
        minutes += seconds // 60
        seconds %= 60
        hours += minutes // 60
        minutes %= 60

        # Calculate average time
        total_seconds = seconds + minutes * 60 + hours * 3600
        average_seconds = total_seconds / count_hikes

        self.total_hikes_label.setText(str(count_hikes))
        self.total_length_label.setText(str(count_length) + "km")
        self.total_time_label.setText("%d:%d:%d" % (hours, minutes, seconds))
        self.total_ascent_label.setText(str(count_ascent) + "m")
        self.total_descent_label.setText(str(count_descent) + "m")
        self.avg_time_label.setText(str(count_length / count_hikes) + "m")
        self.avg_length_label.setText("{0:.2f}m".format(count_length / count_hikes))
        self.avg_time_label.setText("{0:.2f} hours".format(average_seconds / 3600))
        self.avg_ascent_label.setText("{0:.2f}m".format(count_ascent / count_hikes))
        self.avg_descent_label.setText("{0:.2f}m".format(count_descent / count_hikes))
        self.total_mountains_label.setText(str(count_mountains))
        self.total_hills_label.setText(str(count_hills))
        self.dub_wick_label.setText(str(count_dub_wick))
        self.east_coast_label.setText(str(count_east_coast))
        self.north_mid_label.setText(str(count_north_mid))
        self.snowdonia_label.setText(str(count_snowdonia))


class DisplayMountain(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(" Mountain Details")
        self.setWindowIcon(QIcon("icons/mountain.png"))
        self.setGeometry(400, 175, 950, 669)
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
        self.mountain_area = mountain[7]
        self.date_climbed = mountain[8]
        self.mountain_photo = mountain[9]

    def widgets(self):
        ##### Top Layout Widgets #####
        self.mountain_img = QLabel()
        self.img = QPixmap("photos/{}".format(self.mountain_photo))
        self.mountain_img.setPixmap(self.img)
        self.mountain_img.setAlignment(Qt.AlignCenter)
        self.title_text = QLabel(self.mountain_name)
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
        self.latitude_entry.setText(str(self.mountain_lat))
        self.area_combo = QComboBox()
        self.area_combo.addItems(["Dublin/Wicklow", "East Coast", "North Midlands", "Snowdonia"])
        self.area_combo.setCurrentText(self.mountain_area)
        self.date_entry = QCalendarWidget()
        self.date_entry.setGridVisible(True)
        dc = parser.parse(self.date_climbed)
        self.date_entry.setSelectedDate(dc)
        self.upload_btn = QPushButton("Upload Photo")
        self.upload_btn.clicked.connect(self.upload_img)
        self.delete_btn = QPushButton("Delete Mountain")
        self.delete_btn.clicked.connect(self.delete_mountain)
        self.update_btn = QPushButton("Update Mountain")
        self.update_btn.clicked.connect(self.update_mountain)

    def layouts(self):
        self.main_layout = QVBoxLayout()
        self.top_layout = QVBoxLayout()
        self.middle_layout = QHBoxLayout()
        self.middle_left = QFormLayout()
        self.middle_right = QFormLayout()
        self.bottom_layout = QHBoxLayout()
        self.top_frame = QFrame()
        self.top_frame.setStyleSheet(style.top_frame_style())
        self.middle_frame = QFrame()
        self.middle_frame.setStyleSheet(style.bottom_frame_style())
        self.bottom_frame = QFrame()
        self.bottom_frame.setStyleSheet(style.bottom_frame_style())

        ##### Add Widgets #####
        self.top_layout.addWidget(self.title_text)
        self.top_layout.addWidget(self.mountain_img)
        self.top_frame.setLayout(self.top_layout)
        self.middle_left.addRow(QLabel("Name:"), self.name_entry)
        self.middle_left.addRow(QLabel("Height:"), self.height_entry)
        self.middle_left.addRow(QLabel("Prominence:"), self.prominence_entry)
        self.middle_left.addRow(QLabel("Longitude:"), self.longitude_entry)
        self.middle_left.addRow(QLabel("Latitude:"), self.latitude_entry)
        self.middle_left.addRow(QLabel("Area:"), self.area_combo)
        self.middle_left.addRow(QLabel("Photo: "), self.upload_btn)
        self.bottom_layout.addWidget(self.update_btn)
        self.bottom_layout.addWidget(self.delete_btn)

        self.middle_right.addRow(QLabel("Climb Date: "), self.date_entry)
        self.middle_layout.addLayout(self.middle_left, 65)
        self.middle_layout.addLayout(self.middle_right, 35)
        self.middle_frame.setLayout(self.middle_layout)
        self.bottom_frame.setLayout(self.bottom_layout)
        self.main_layout.addWidget(self.top_frame)
        self.main_layout.addWidget(self.middle_frame)
        self.main_layout.addWidget(self.bottom_frame)

        self.setLayout(self.main_layout)

    def upload_img(self):
        size = (512, 512)
        self.file_name, ok = QFileDialog.getOpenFileName(self, "Upload Image", "", "Image Files (*.jpg *.png)")
        if ok:
            self.mountain_photo = os.path.basename(self.file_name)
            img = Image.open(self.file_name)
            img = img.resize(size)
            img.save("photos/{0}".format(self.mountain_photo))

    def update_mountain(self):
        global mountain_id
        name = self.name_entry.text()
        height = self.height_entry.text()
        prominence = self.prominence_entry.text()
        longitude = self.longitude_entry.text()
        latitude = self.latitude_entry.text()
        area = self.area_combo.currentText()
        date = self.date_entry.selectedDate().toString()
        default_image = self.mountain_photo

        if name and height and prominence and longitude and latitude != "":
            try:
                height = float(height)
                prominence = float(prominence)
                longitude = float(longitude)
                latitude = float(latitude)
                query = "UPDATE mountain SET name = ?, height = ?, prominence = ?, " \
                        "longitude = ?, latitude = ?, area = ?, date_climbed = ?, photo = ? WHERE id = ?"
                cur.execute(query, (name, height, prominence, longitude, latitude, area, date, default_image, mountain_id))
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


class DisplayHike(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(" Hike Details")
        self.setWindowIcon(QIcon("icons/hiking.png"))
        self.setGeometry(500, 95, 575, 835)
        self.setFixedSize(self.size())
        self.UI()
        self.show()

    def UI(self):
        self.hike_details()
        self.widgets()
        self.layouts()

    def hike_details(self):
        global hike_id
        query = "SELECT * FROM hike WHERE id = ?"
        hike = cur.execute(query, (hike_id,)).fetchone()

        self.hike_length = hike[1]
        self.hike_duration = hike[2]
        self.hike_ascent = hike[3]
        self.hike_descent = hike[4]
        self.hike_date = hike[5]
        self.hike_notes = hike[6]

    def widgets(self):
        ##### Top Layout Widgets #####
        self.hike_img = QLabel()
        self.img = QPixmap("icons/hiking.png")
        self.hike_img.setPixmap(self.img)
        self.hike_img.setAlignment(Qt.AlignCenter)
        self.title_text = QLabel("Display Hike")
        self.title_text.setAlignment(Qt.AlignCenter)

        # #### Bottom Layout Widgets #####
        self.length_entry = QLineEdit()
        self.length_entry.setText(str(self.hike_length))
        self.duration_entry = QLineEdit()
        self.duration_entry.setText(str(self.hike_duration))
        self.ascent_entry = QLineEdit()
        self.ascent_entry.setText(str(self.hike_ascent))
        self.descent_entry = QLineEdit()
        self.descent_entry.setText(str(self.hike_descent))
        self.notes_entry = QTextEdit()
        self.notes_entry.setText(self.hike_notes)
        self.date_entry = QCalendarWidget()
        self.date_entry.setGridVisible(True)
        dc = parser.parse(self.hike_date)
        self.date_entry.setSelectedDate(dc)
        self.delete_btn = QPushButton("Delete")
        self.delete_btn.clicked.connect(self.delete_hike)
        self.update_btn = QPushButton("Update")
        self.update_btn.clicked.connect(self.update_hike)

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
        self.top_layout.addWidget(self.hike_img)
        self.top_frame.setLayout(self.top_layout)
        self.bottom_layout.addRow(QLabel("Length:"), self.length_entry)
        self.bottom_layout.addRow(QLabel("Duration:"), self.duration_entry)
        self.bottom_layout.addRow(QLabel("Ascent:"), self.ascent_entry)
        self.bottom_layout.addRow(QLabel("Descent:"), self.descent_entry)
        self.bottom_layout.addRow(QLabel("Notes:"), self.notes_entry)
        self.bottom_layout.addRow(QLabel("Hike Date: "), self.date_entry)
        self.bottom_layout.addRow(QLabel(""), self.delete_btn)
        self.bottom_layout.addRow(QLabel(""), self.update_btn)
        self.bottom_frame.setLayout(self.bottom_layout)
        self.main_layout.addWidget(self.top_frame)
        self.main_layout.addWidget(self.bottom_frame)

        self.setLayout(self.main_layout)

    def update_hike(self):
        global hike_id
        length = self.length_entry.text()
        duration = self.duration_entry.text()
        ascent = self.ascent_entry.text()
        descent = self.descent_entry.text()
        notes = self.notes_entry.toPlainText()
        date = self.date_entry.selectedDate().toString()

        if length and duration and ascent and descent != "":
            try:
                length = float(length)
                ascent = float(ascent)
                descent = float(descent)
                query = "UPDATE hike SET length = ?, duration = ?, ascent = ?, " \
                        "descent = ?, date = ?, note = ? WHERE id = ?"
                cur.execute(query, (length, duration, ascent, descent, date, notes, hike_id))
                con.commit()
                QMessageBox.information(self, "Info", "Hike has been updated")
                self.close()
            except Exception:
                QMessageBox.warning(self, 'Error', 'Invalid entry, input must be a number')
            except:
                QMessageBox.warning(self, "Warning", "Hike has not been updated")
        else:
            QMessageBox.warning(self, "Warning", "Fields cannot be empty")

    def delete_hike(self):
        global hike_id
        mbox = QMessageBox.question(self, "Warning", "Are you sure you want to delete this hike?",
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if mbox == QMessageBox.Yes:
            try:
                query = "DELETE FROM hike WHERE id = ?"
                cur.execute(query, (hike_id,))
                con.commit()
                QMessageBox.information(self, "Info", "Hike has been deleted")
                self.close()
            except:
                QMessageBox.warning(self, "Warning", "Hike has not been deleted")


def main():
    App = QApplication(sys.argv)
    window = Main()
    sys.exit(App.exec_())


if __name__ == "__main__":
    main()

# Icons made by "https://www.flaticon.com/authors/freepik"
