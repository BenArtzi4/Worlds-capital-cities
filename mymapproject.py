import requests, zipfile, pandas, folium
from io import BytesIO

# Download a zipfile
url = "https://simplemaps.com/static/data/world-cities/basic/simplemaps_worldcities_basicv1.75.zip"
filename = url.split('/')[-1]
req = requests.get(url)

#Extracted files from the downloaded zipfile
zipfile = zipfile.ZipFile(BytesIO(req.content))
zipfile.extractall("C:\Downloads")

fgv = folium.FeatureGroup(name = "Cities")

df1 = pandas.read_excel("C:\Downloads\worldcities.xlsx")
df1 = df1.fillna("0")
data1 = df1.loc[(df1['capital'] == "primary")]




latitude = list(data1["lat"])
longitude = list(data1["lng"])
population = list(data1["population"])
city = list(data1["city"])

# Setting the properties of the popup
html = """<h4>Information:</h4>
Capital City: %s"""

# A method that determines the color of the popup according to the height of the volcano
def choosing_color(population):
    if population < 500000:
        return 'green'
    elif population < 1000000:
        return 'orange'
    else:
        return 'red'

# Adding a map and defining its features
map = folium.Map(location=[47.28, -116.27], zoom_start = 4, tiles="Stamen Terrain")

# The representation of the points of the volcanoes on the map
for lt ,ln,pl,ct in zip(latitude,longitude,population,city):
    iframe = folium.IFrame(html=html % ct, width=200, height=100)
    fgv.add_child(folium.Marker(location=[lt, ln], popup=folium.Popup(iframe), icon = folium.Icon(color = choosing_color(int(pl)) )))

# Adding a layer of country boundary markers
fgc = folium.FeatureGroup(name = "Countrys")

# A state will perform according to the number of its inhabitants as called from the JSON file and defined in the conditions
fgc.add_child(folium.GeoJson(data = open("world.json" , 'r' , encoding='utf-8-sig').read() ) )

# Add feature group
map.add_child(fgv)
map.add_child(fgc)

# Setting a control panel 
map.add_child(folium.LayerControl())


map.save("Map3.html")
