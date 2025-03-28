from folium import Element

import folium
import webbrowser

from src.API_OpenSeaMap.controls import add_controls
from src.API_OpenSeaMap.layers import add_base_layers
from src.API_OpenSeaMap.markers import add_markers
from src.API_OpenSeaMap.route import add_route
# La sidebar est ajoutée via add_markers()

def create_map(center, zoom=14, base_tiles="OpenStreetMap"):
    m = folium.Map(location=center, zoom_start=zoom, tiles=base_tiles)

    # Ajouter la définition de la variable 'map' dans le DOM
    m.get_root().html.add_child(Element("""
    <script>
        var map = window.map = L.map(document.querySelector('.leaflet-container'));
    </script>
    """))

    return m


def plot_gps_route(navigation_data):
    latitudes = navigation_data.get("latitude", [])
    longitudes = navigation_data.get("longitude", [])
    if not latitudes or not longitudes:
        print("❌ Aucune donnée GPS disponible.")
        return

    center = [latitudes[0], longitudes[0]]
    m = create_map(center, zoom=14)

    add_base_layers(m)
    add_route(m, latitudes, longitudes)
    add_markers(m, navigation_data)
    add_controls(m)

    map_file = r"C:\Users\gendr\OneDrive\Documents\SUPERIEUR\ING4\PPE\Backend_python\data\gps_routes\gps_route.html"
    m.save(map_file)
    webbrowser.open(map_file)
    print("✅ Carte améliorée générée avec succès !")
