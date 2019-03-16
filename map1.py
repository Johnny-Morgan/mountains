import folium
import pandas

data = pandas.read_csv("mountains.txt")
latitude = list(data["LAT"])
longitude = list(data["LON"])
mountain_name = list(data["NAME"])
height = list(data["HEIGHT"])
prominence = list(data["PROM"])
fact = list(data["FACT"])

html = """
<b>Name:</b> %s<br>
<b>Height:</b> %sm<br>
<b>Prominence:</b> %sm<br>
<b>Fun fact:</b> %s
"""
#color based on height
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

# color based on arderins, arderin-begs & Vandeleur-Lynams
# def color_picker(height, prominence):
#     if height >=500 and prominence < 30 and prominence > 15:
#         return "red"
#     elif height >= 600 and prominence >= 15 and prominence < 30:
#         return "blue"
#     elif height >= 600 and prominence >= 15:
#         return "blue"

map = folium.Map(location = [53.124, -6.350], zoom_start = 10)

fg_mountains = folium.FeatureGroup(name = "Mountains")
fg_hills = folium.FeatureGroup(name = "Hills")
for lat, lon, name, h, prom, f in zip(latitude, longitude, mountain_name, height, prominence, fact):
    iframe = folium.IFrame(html=html % (name, str(h), str(prom), f), width=200, height=100)
    #fg.add_child(folium.Marker(location = [lat, lon], popup=folium.Popup(iframe), icon = folium.Icon(color = color_picker(h))))
    if h > 500:
        fg_mountains.add_child(folium.CircleMarker(location = [lat, lon], popup=folium.Popup(iframe),
        radius = 9, fill = True, fill_color = color_picker(h), color = "black", fill_opacity = 0.8))
    else:
        fg_hills.add_child(folium.CircleMarker(location = [lat, lon], popup=folium.Popup(iframe),
        radius = 9, fill = True, fill_color = color_picker(h), color = "black", fill_opacity = 0.8))

map.add_child(fg_mountains)
map.add_child(fg_hills)
map.add_child(folium.LayerControl())
map.save("Map1.html")
