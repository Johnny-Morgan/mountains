import folium
import sqlite3
import csv
import os


con = sqlite3.connect("mountains.db")
cur = con.cursor()

##############################################################
##### create sqlite database using existing txt database #####
##############################################################

# cur.execute("CREATE TABLE mountain (name TEXT, height REAL, prominence REAL, longitude REAL, latitude REAL, fact TEXT)")
# with open('mountains.txt') as f:
#     next(f) # skip header
#     reader = csv.reader(f)
#     data = []
#     for row in reader:
#         data.append(row)
#
# cur.executemany("INSERT INTO mountain (name, height, prominence, longitude, latitude, fact) VALUES (?, ?, ?, ?, ?, ?);", data)
# con.commit()

query = "SELECT * FROM mountain"
mountain = cur.execute(query).fetchall()

mountain_name = []
mountain_height = []
mountain_prom = []
mountain_long = []
mountain_lat = []
mountain_fact = []

for i in range(0, len(mountain)):
    mountain_name.append(mountain[i][0])
    mountain_height.append(mountain[i][1])
    mountain_prom.append(mountain[i][2])
    mountain_long.append(mountain[i][3])
    mountain_lat.append(mountain[i][4])
    mountain_fact.append(mountain[i][5])

html = """
<b>Name:</b> %s<br>
<b>Height:</b> %sm<br>
<b>Prominence:</b> %sm<br>
<b>Fun fact:</b> %s
"""


# color based on height
def color_picker(height):
    if height < 300:
        return "lightgreen"
    elif height < 500:
        return "green"
    elif height < 600:
        return "darkgreen"
    elif height < 700:
        return "orange"
    elif height < 800:
        return "red"
    else:
        return "darkred"


map = folium.Map(location = [53.124, -5.650], zoom_start = 9)

fg_mountains = folium.FeatureGroup(name = "Mountains")
fg_hills = folium.FeatureGroup(name = "Hills")

for lat, lon, name, h, prom, f in zip(mountain_lat, mountain_long, mountain_name, mountain_height, mountain_prom, mountain_fact):
    iframe = folium.IFrame(html = html % (name, str(h), str(prom), f), width = 200, height = 100)
    if h > 500:
        fg_mountains.add_child(folium.CircleMarker(location = [lat, lon], popup = folium.Popup(iframe),
        radius = 9, fill = True, fill_color = color_picker(h), color = "black", fill_opacity = 0.8))
    else:
        fg_hills.add_child(folium.CircleMarker(location = [lat, lon], popup = folium.Popup(iframe),
        radius = 9, fill = True, fill_color = color_picker(h), color = "black", fill_opacity = 0.8))

map.add_child(fg_mountains)
map.add_child(fg_hills)
map.add_child(folium.LayerControl())
map.save("Map1.html")

# open map in browser
os.system("start Map1.html")
