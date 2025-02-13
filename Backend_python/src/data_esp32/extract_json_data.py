import json
import os
import math


def load_navigation_data(json_file):
    """
    Charge les données de navigation depuis un fichier JSON et remplace les valeurs invalides.

    :param json_file: Chemin du fichier JSON contenant les données de navigation.
    :return: Dictionnaire contenant les listes de données extraites.
    """
    if not os.path.exists(json_file):
        print(f"❌ ERREUR : Le fichier {json_file} n'existe pas.")
        return None

    # 📌 Vérifier si le fichier est vide
    if os.stat(json_file).st_size == 0:
        print(f"❌ ERREUR : Le fichier {json_file} est vide.")
        return None

    with open(json_file, "r") as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError as e:
            print(f"❌ ERREUR : Fichier JSON mal formé : {e}")
            return None

    # 📌 Stockage des données sous forme de listes
    time_series = []
    yaw_series = []
    pitch_series = []
    roll_series = []
    latitude_series = []
    longitude_series = []
    wind_speed_series = []
    wind_direction_series = []

    for entry in data:
        time_series.append(entry["time"])
        yaw_series.append(entry["yaw"])
        pitch_series.append(entry["pitch"])
        roll_series.append(entry["roll"])
        latitude_series.append(entry["lat"])
        longitude_series.append(entry["lon"])

        # 📌 Vérification et remplacement de `inf`
        wind_speed = entry["windSpeed"]
        if isinstance(wind_speed, (float, int)) and math.isinf(wind_speed):
            wind_speed = 99999.99  # Remplace inf par une valeur arbitraire

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
    """ Affiche les premières lignes des données extraites pour vérification. """
    if not navigation_data:
        print("❌ Aucune donnée à afficher.")
        return

    print("✅ Vérification des données extraites :\n")
    for key, values in navigation_data.items():
        print(f"{key}: {values[:max_entries]} {'...' if len(values) > max_entries else ''}")


