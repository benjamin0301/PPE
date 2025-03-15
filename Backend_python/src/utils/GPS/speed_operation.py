import math
from src.utils.GPS.haversine_fonction import haversine  # Fonction pour calculer la distance entre 2 points GPS

def kmh_to_knots(speed_kmh):
    return speed_kmh / 1.852  # 1 nœud = 1.852 km/h

def calculate_speeds(navigation_data):
    """
    Calcule les vitesses à partir des données GPS extraites.
    :param navigation_data: Dictionnaire contenant les listes des données GPS.
                           La clé "time" doit contenir des objets datetime.
    """
    # Extraction des données
    time_series = navigation_data["time"]         # Objets datetime
    latitude_series = navigation_data["latitude"]
    longitude_series = navigation_data["longitude"]

    speed_series_kmh = []  # Liste des vitesses en km/h
    speed_series_knots = []  # Liste des vitesses en nœuds

    if len(time_series) < 2:
        print("❌ Pas assez de points GPS pour calculer les vitesses.")
        return

    print("✅ Début des calculs des vitesses...\n")

    # Boucle pour calculer les vitesses entre chaque point
    for i in range(1, len(time_series)):
        lat1, lon1, dt1 = latitude_series[i - 1], longitude_series[i - 1], time_series[i - 1]
        lat2, lon2, dt2 = latitude_series[i], longitude_series[i], time_series[i]

        # Calcul de la distance entre les deux points
        distance_km = haversine(lat1, lon1, lat2, lon2)

        # Calcul du temps écoulé en secondes (en utilisant .total_seconds() sur l'objet timedelta)
        time_elapsed = (dt2 - dt1).total_seconds()

        # Calcul des vitesses en km/h et en nœuds
        if time_elapsed > 0:
            speed_kmh = (distance_km / time_elapsed) * 3600  # Conversion en km/h
            speed_knots = kmh_to_knots(speed_kmh)
        else:
            speed_kmh = 0
            speed_knots = 0

        speed_series_kmh.append(speed_kmh)
        speed_series_knots.append(speed_knots)

        # Affichage du résultat pour ce segment
        print(f"📍 Position: ({lat2:.5f}, {lon2:.5f}) | Temps: {dt2.strftime('%Y-%m-%d %H:%M:%S')} | "
              f"🚀 Vitesse: {speed_kmh:.2f} km/h ({speed_knots:.2f} nœuds)")

    # Calcul et affichage des statistiques globales
    avg_speed_kmh = sum(speed_series_kmh) / len(speed_series_kmh)
    avg_speed_knots = sum(speed_series_knots) / len(speed_series_knots)

    print("\n✅ Résumé des vitesses :")
    print(f"⚡ Vitesse moyenne : {avg_speed_kmh:.2f} km/h ({avg_speed_knots:.2f} nœuds)")
