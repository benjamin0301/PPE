import folium
import pandas as pd
import webbrowser
from folium import plugins
import os

def plot_gps_route():
    # 📌 Charger le fichier CSV contenant les données GPS
    csv_file = os.path.join(os.path.dirname(__file__), "../../data/gps_data.csv")
    df = pd.read_csv(csv_file)

    # 📌 Création de la carte avec OpenStreetMap + OpenSeaMap
    m = folium.Map(
        location=[df["latitude"].iloc[0], df["longitude"].iloc[0]],
        zoom_start=14,
        tiles="OpenStreetMap"
    )

    # 📌 Ajouter OpenSeaMap en couche superposée
    folium.TileLayer(
        tiles="https://tiles.openseamap.org/seamark/{z}/{x}/{y}.png",
        attr="OpenSeaMap",
        name="OpenSeaMap"
    ).add_to(m)

    # 📌 Ajouter une couche satellite pour basculer entre les vues
    folium.TileLayer(
        tiles="https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png",
        attr="OpenTopoMap",
        name="Relief"
    ).add_to(m)

    # 📌 Ajouter une trace GPS plus visible
    coords = list(zip(df["latitude"], df["longitude"]))
    folium.PolyLine(
        coords, color="blue", weight=4, opacity=0.7, dash_array="5, 10"
    ).add_to(m)

    # 📌 Ajouter une animation de mouvement le long du trajet
    plugins.AntPath(
        coords, color="red", weight=3, delay=500
    ).add_to(m)

    # 📌 Ajouter des marqueurs pour chaque point GPS
    for idx, row in df.iterrows():
        folium.Marker(
            location=[row["latitude"], row["longitude"]],
            popup=f"📍 Heure: {row['timestamp']}s | 🚀 {row['speed_kmh']} km/h",
            icon=folium.Icon(color="blue" if idx != len(df)-1 else "red")
        ).add_to(m)

    # 📌 Ajouter des marqueurs spéciaux pour le départ et l’arrivée
    folium.Marker(
        location=[df["latitude"].iloc[0], df["longitude"].iloc[0]],
        popup="🚀 Départ",
        icon=folium.Icon(color="green", icon="play")
    ).add_to(m)

    folium.Marker(
        location=[df["latitude"].iloc[-1], df["longitude"].iloc[-1]],
        popup="🏁 Arrivée",
        icon=folium.Icon(color="red", icon="flag")
    ).add_to(m)

    # 📌 Ajouter une échelle de distance
    plugins.MeasureControl(primary_length_unit="kilometers").add_to(m)

    # 📌 Ajouter un contrôle pour basculer entre les différentes cartes
    folium.LayerControl().add_to(m)

    # 📌 Sauvegarder et afficher la carte
    map_file = "data/gps_routes/gps_route.html"
    m.save(map_file)
    webbrowser.open(map_file)

    print("✅ Carte améliorée générée avec succès !")

