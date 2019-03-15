import folium
import pandas

data = pandas.read_csv("mountains.txt")
latitude = list(data["LAT"])
longitude = list(data["LON"])
mountain_name = list(data["NAME"])
height = list(data["HEIGHT"])
prominence = list(data["PROM"])

html = """<h4>Mountain information:</h4>
Name: %s<br>
Height: %sm<br>
Prominence: %sm<br>
"""
#color based on height
def color_picker(height):
    if height < 600:
        return "green"
    elif height < 700:
        return "orange"
    else:
        return "red"

# color based on arderins, arderin-begs & Vandeleur-Lynams
# def color_picker(height, prominence):
#     if height >=500 and prominence < 30 and prominence > 15:
#         return "red"
#     elif height >= 600 and prominence >= 15 and prominence < 30:
#         return "blue"
#     elif height >= 600 and prominence >= 15:
#         return "blue"

map = folium.Map(location = [53.124, -6.350], zoom_start = 10)

fg = folium.FeatureGroup(name = "My Map")
for lat, lon, name, h, prom in zip(latitude, longitude, mountain_name, height, prominence):
    color = "green"
    if h > 700:
        color = "red"
    iframe = folium.IFrame(html=html % (name, str(h), str(prom)), width=200, height=100)
    #fg.add_child(folium.Marker(location = [lat, lon], popup=folium.Popup(iframe), icon = folium.Icon(color = color_picker(h))))
    fg.add_child(folium.CircleMarker(location = [lat, lon], popup=folium.Popup(iframe), radius = 7, fill = True, fill_color = color_picker(h), color = color_picker(h), fill_opacity = 0.7))
map.add_child(fg)
map.save("Map1.html")
