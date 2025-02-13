import math
from src.utils.GPS.haversine_fonction import haversine  # Fonction pour calculer la distance entre 2 points GPS


# 📌 Fonction pour convertir une vitesse de km/h en nœuds
def kmh_to_knots(speed_kmh):
    return speed_kmh / 1.852  # 1 nœud = 1.852 km/h


# 📌 Fonction principale de calcul des vitesses
def calculate_speeds(navigation_data):
    """
    Calcule les vitesses à partir des données GPS extraites.

    :param navigation_data: Dictionnaire contenant les listes des données GPS.
    """
    # 📌 Extraction des données
    time_series = navigation_data["time"]
    latitude_series = navigation_data["latitude"]
    longitude_series = navigation_data["longitude"]

    # 📌 Initialisation des variables
    speed_series_kmh = []  # Liste des vitesses en km/h
    speed_series_knots = []  # Liste des vitesses en nœuds

    # 📌 Vérification du nombre de points
    if len(time_series) < 2:
        print("❌ Pas assez de points GPS pour calculer les vitesses.")
        return

    print("✅ Début des calculs des vitesses...\n")

    # 📌 Boucle pour calculer les vitesses entre chaque point
    for i in range(1, len(time_series)):
        lat1, lon1, time1 = latitude_series[i - 1], longitude_series[i - 1], time_series[i - 1]
        lat2, lon2, time2 = latitude_series[i], longitude_series[i], time_series[i]

        # 📌 Calcul de la distance parcourue
        distance_km = haversine(lat1, lon1, lat2, lon2)

        # 📌 Calcul du temps écoulé
        time_elapsed = time2 - time1  # Temps en secondes

        # 📌 Calcul des vitesses
        if time_elapsed > 0:
            speed_kmh = (distance_km / time_elapsed) * 3600  # Convertit en km/h
            speed_knots = kmh_to_knots(speed_kmh)  # Convertit en nœuds
        else:
            speed_kmh = 0
            speed_knots = 0

        # 📌 Stockage des résultats
        speed_series_kmh.append(speed_kmh)
        speed_series_knots.append(speed_knots)

        # 📌 Affichage des résultats
        print(f"📍 Position: ({lat2:.5f}, {lon2:.5f}) | "
              f"⏱ Temps: {time2}s | "
              f"🚀 Vitesse: {speed_kmh:.2f} km/h ({speed_knots:.2f} nœuds)")

    # 📌 Affichage des statistiques globales
    avg_speed_kmh = sum(speed_series_kmh) / len(speed_series_kmh)
    avg_speed_knots = sum(speed_series_knots) / len(speed_series_knots)

    print("\n✅ Résumé des vitesses :")
    print(f"⚡ Vitesse moyenne : {avg_speed_kmh:.2f} km/h ({avg_speed_knots:.2f} nœuds)")

