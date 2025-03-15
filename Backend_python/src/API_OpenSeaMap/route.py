
import folium
from folium import plugins


# --- Fonction pour tracer la route GPS ---
def add_route(m, latitudes, longitudes):
    coords = list(zip(latitudes, longitudes))
    folium.PolyLine(coords, color="blue", weight=4, opacity=0.7, dash_array="5, 10").add_to(m)
    plugins.AntPath(coords, color="red", weight=3, delay=500).add_to(m)
