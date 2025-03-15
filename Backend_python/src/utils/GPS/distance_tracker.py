import math
from src.utils.GPS.speed_operation import haversine  # Fonction pour calculer la distance entre 2 points GPS


# 📌 Fonction pour convertir une distance en milles nautiques
def km_to_nautical_miles(distance_km):
    return distance_km / 1.852  # 1 mille nautique = 1.852 km


# 📌 Fonction principale de calcul des distances
def calculate_distances(navigation_data):
    """
    Calcule les distances parcourues à partir des données GPS.

    :param navigation_data: Dictionnaire contenant les listes des données GPS.
    """
    # 📌 Extraction des données
    time_series = navigation_data["time"]
    latitude_series = navigation_data["latitude"]
    longitude_series = navigation_data["longitude"]

    # 📌 Initialisation des métriques
    total_distance_km = 0.0  # Distance totale en km
    total_distance_nm = 0.0  # Distance totale en milles nautiques

    # 📌 Vérification de la longueur des données
    if len(time_series) < 2:
        print("❌ Pas assez de points GPS pour effectuer les calculs.")
        return

    print("\n✅ Début des calculs des distances...\n")

    # 📌 Boucle pour calculer les distances entre chaque point
    for i in range(1, len(time_series)):
        lat1, lon1, time1 = latitude_series[i - 1], longitude_series[i - 1], time_series[i - 1]
        lat2, lon2, time2 = latitude_series[i], longitude_series[i], time_series[i]

        # 📌 Calcul de la distance parcourue
        distance_km = haversine(lat1, lon1, lat2, lon2)
        distance_nm = km_to_nautical_miles(distance_km)

        # 📌 Mise à jour des distances totales
        total_distance_km += distance_km
        total_distance_nm += distance_nm

        # 📌 Affichage des résultats pour chaque point
        print(f"📍 Position: ({lat2}, {lon2}) | "
              f"⏱ Temps: {time2}s | "
              f"📏 Distance instantanée: {distance_km:.5f} km ({distance_nm:.5f} MN)")

    # 📌 Affichage du résumé
    print("\n✅ Résumé des distances :")
    print(f"📏 Distance totale parcourue : {total_distance_km:.2f} km ({total_distance_nm:.2f} MN)")

