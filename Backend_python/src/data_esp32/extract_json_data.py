import json
import os
import math
from datetime import datetime

def choose_file():
    """
    Liste les fichiers JSON disponibles dans le dossier, demande à l'utilisateur d'en choisir un,
    extrait les données via load_navigation_data() et affiche un aperçu via display_navigation_data().
    """
    # Définir le dossier contenant les fichiers JSON (modifiez le chemin si nécessaire)
    json_directory = os.path.join(os.path.dirname(__file__), "../../data/json_data_files/")

    # Lister tous les fichiers JSON présents dans le dossier
    json_files = [f for f in os.listdir(json_directory) if f.endswith('.json')]

    if not json_files:
        print("❌ Aucun fichier JSON trouvé dans le dossier :", json_directory)
        return

    print("Fichiers JSON disponibles :")
    for idx, file in enumerate(json_files, start=1):
        print(f"{idx}. {file}")

    # Sélectionner le premier fichier par défaut pour les tests (vous pouvez activer la saisie utilisateur)
    selected_file = json_files[0]
    file_path = os.path.join(json_directory, selected_file)
    print(f"Vous avez choisi : {selected_file}")

    # Extraction des données à partir du fichier choisi
    navigation_data = load_navigation_data(file_path)
    display_navigation_data(navigation_data)
    return navigation_data


def load_navigation_data(json_file):
    """
    Charge les données de navigation depuis un fichier JSON et convertit la date dans 'time'
    en objet datetime (format attendu : "YYYY-MM-DD HH:MM:SS").

    :param json_file: Chemin du fichier JSON contenant les données de navigation.
    :return: Dictionnaire contenant les listes de données extraites.
    """
    if not os.path.exists(json_file):
        print(f"❌ ERREUR : Le fichier {json_file} n'existe pas.")
        return None

    # Vérifier si le fichier est vide
    if os.stat(json_file).st_size == 0:
        print(f"❌ ERREUR : Le fichier {json_file} est vide.")
        return None

    with open(json_file, "r") as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError as e:
            print(f"❌ ERREUR : Fichier JSON mal formé : {e}")
            return None

    # Stockage des données sous forme de listes
    time_series = []
    yaw_series = []
    pitch_series = []
    roll_series = []
    latitude_series = []
    longitude_series = []
    wind_speed_series = []
    wind_direction_series = []

    for entry in data:
        # Conversion de la date (attendu : "YYYY-MM-DD HH:MM:SS")
        time_str = entry["time"]
        try:
            dt = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
        except Exception as e:
            print(f"❌ Erreur de conversion de la date '{time_str}': {e}")
            dt = None
        time_series.append(dt)

        yaw_series.append(entry["yaw"])
        pitch_series.append(entry["pitch"])
        roll_series.append(entry["roll"])
        latitude_series.append(entry["lat"])
        longitude_series.append(entry["lon"])

        # Vérification et remplacement de `inf` pour windSpeed
        wind_speed = entry["windSpeed"]
        if isinstance(wind_speed, (float, int)) and math.isinf(wind_speed):
            wind_speed = 99999.99  # Remplacement d'inf par une valeur arbitraire

        wind_speed_series.append(wind_speed)
        wind_direction_series.append(entry["windDir"])

    return {
        "time": time_series,
        "yaw": yaw_series,
        "pitch": pitch_series,
        "roll": roll_series,
        "latitude": latitude_series,
        "longitude": longitude_series,
        "wind_speed": wind_speed_series,
        "wind_direction": wind_direction_series,
    }


def display_navigation_data(navigation_data, max_entries=5):
    """Affiche les premières lignes des données extraites pour vérification."""
    if not navigation_data:
        print("❌ Aucune donnée à afficher.")
        return

    print("✅ Vérification des données extraites :\n")
    for key, values in navigation_data.items():
        if key == "time":
            # Formater les dates en chaîne pour l'affichage
            formatted_values = [v.strftime("%Y-%m-%d %H:%M:%S") if v is not None else "N/A" for v in values]
        else:
            formatted_values = values
        print(f"{key}: {formatted_values[:max_entries]} {'...' if len(values) > max_entries else ''}")
