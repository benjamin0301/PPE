import folium


# --- Fonction pour ajouter les couches de fond pertinentes pour la navigation maritime ---
def add_base_layers(m):
    # Esri WorldImagery (vue satellite)
    folium.TileLayer(
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        attr="Tiles © Esri — Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community",
        name="Esri WorldImagery",
        overlay=False,
        control=True
    ).add_to(m)

    # OpenSeaMap en overlay
    folium.TileLayer(
        tiles="https://tiles.openseamap.org/seamark/{z}/{x}/{y}.png",
        attr="OpenSeaMap",
        name="OpenSeaMap",
        overlay=True,
        control=True
    ).add_to(m)
