import random
import time

# Simulation des données GPS
def simulate_gps_data():
    lat = 48.8566  # Latitude initiale (Paris)
    lon = 2.3522  # Longitude initiale
    timestamp = time.time()  # Temps initial (en secondes)

    while True:
        # Simule un déplacement aléatoire (petit changement de latitude/longitude)
        lat += random.uniform(-0.0001, 0.0001)
        lon += random.uniform(-0.0001, 0.0001)
        new_timestamp = time.time()

        yield lat, lon, new_timestamp

        time.sleep(1)  # Simule un intervalle de 1 seconde entre chaque point
