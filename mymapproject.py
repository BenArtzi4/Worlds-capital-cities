import requests
import zipfile
import pandas as pd
import folium
from io import BytesIO

# Download a zipfile
url = "https://simplemaps.com/static/data/world-cities/basic/simplemaps_worldcities_basicv1.75.zip"
req = requests.get(url)

# Extract files from the downloaded zipfile
with zipfile.ZipFile(BytesIO(req.content)) as z:
    z.extractall(r"C:/Downloads")  # Use raw string for the path

# Initialize FeatureGroup for cities
fgv = folium.FeatureGroup(name="Cities")

# Load city data
df1 = pd.read_excel(r"C:/Downloads/worldcities.xlsx")  # Use raw string for the path
df1 = df1.fillna("0")
data1 = df1[df1['capital'] == "primary"]

latitude = list(data1["lat"])
longitude = list(data1["lng"])
population = list(data1["population"])
city = list(data1["city"])

# Setting the properties of the popup
html = """<h4>Information:</h4>
Capital City: %s"""


# Function to determine marker color based on population
def choosing_color(city_population):
    if city_population < 500000:
        return 'green'
    elif city_population < 1000000:
        return 'orange'
    else:
        return 'red'


# Create map and add features
map = folium.Map(location=[47.28, -116.27], zoom_start=4, tiles="Stamen Terrain",
                 attr="Map tiles by Stamen Design, under CC BY 3.0. Data by OpenStreetMap, under ODbL.")

# Add markers for capital cities
for lt, ln, pl, ct in zip(latitude, longitude, population, city):
    iframe = folium.IFrame(html=html % ct, width=200, height=100)
    fgv.add_child(
        folium.Marker(location=[lt, ln], popup=folium.Popup(iframe), icon=folium.Icon(color=choosing_color(int(pl)))))

# Add country boundary markers
fgc = folium.FeatureGroup(name="Countries")
fgc.add_child(folium.GeoJson(data=open("world.json", 'r', encoding='utf-8-sig').read()))

# Add feature groups to map
map.add_child(fgv)
map.add_child(fgc)

# Add layer control
map.add_child(folium.LayerControl())

# Save map to HTML file
map.save("Map3.html")
