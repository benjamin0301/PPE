import folium
import webbrowser

from src.API_OpenSeaMap.controls import add_controls
from src.API_OpenSeaMap.layers import add_base_layers
from src.API_OpenSeaMap.markers import add_markers
from src.API_OpenSeaMap.route import add_route
from src.API_OpenSeaMap.sidebar import add_sidebar


# --- Fonction pour créer et retourner la carte de base ---
def create_map(center, zoom=14, base_tiles="OpenStreetMap"):
    return folium.Map(location=center, zoom_start=zoom, tiles=base_tiles)

# --- Fonction principale qui assemble tous les éléments ---
def plot_gps_route(navigation_data):
    # Vérifier la disponibilité des données GPS
    latitudes = navigation_data.get("latitude", [])
    longitudes = navigation_data.get("longitude", [])
    if not latitudes or not longitudes:
        print("❌ Aucune donnée GPS disponible.")
        return

    # Création de la carte (centrée sur le premier point)
    center = [latitudes[0], longitudes[0]]
    m = create_map(center, zoom=14)

    # Ajout des couches de fond et overlays
    add_base_layers(m)

    # Tracé de la route
    add_route(m, latitudes, longitudes)

    # Ajout des marqueurs
    add_markers(m, navigation_data)

    # Ajout des contrôles (MiniMap, Measure, LayerControl)
    add_controls(m)

    # Ajout de la sidebar pour les infos dynamiques
    #add_sidebar(m)

    # Sauvegarde et ouverture de la carte
    map_file = r"C:\Users\gendr\OneDrive\Documents\SUPERIEUR\ING4\PPE\Backend_python\data\gps_routes\gps_route.html"
    m.save(map_file)
    webbrowser.open(map_file)
    print("✅ Carte améliorée générée avec succès !")

