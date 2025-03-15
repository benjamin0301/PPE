import folium
from folium import plugins
from folium.plugins import MiniMap

# --- Fonction pour ajouter les contrôles (MiniMap, Measure, LayerControl) ---
def add_controls(m):
    # Ajout d'un MiniMap
    minimap = MiniMap(toggle_display=True)
    m.add_child(minimap)

    # Outil de mesure
    plugins.MeasureControl(primary_length_unit="kilometers").add_to(m)

    # Contrôle des couches
    folium.LayerControl().add_to(m)
