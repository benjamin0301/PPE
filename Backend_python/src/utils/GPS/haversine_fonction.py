import math

# Fonction pour calculer la distance entre deux points GPS (formule de Haversine)
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Rayon de la Terre en km
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c  # Distance en km

# Fonction pour convertir une vitesse de km/h en nœuds
def kmh_to_knots(speed_kmh):
    return speed_kmh / 1.852  # 1 nœud = 1.852 km/h

