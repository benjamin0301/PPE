from src.Database.create_db_tables import create_navigation_table
from src.Database.extraction_db import export_data_to_json
from src.Database.insertion_navigation_data import insert_navigation_data
from src.data_esp32.extract_json_data import display_navigation_data, choose_file
from src.data_esp32.call_data_from_esp import call_data_from_esp
from src.utils.GPS.distance_tracker import calculate_distances
from src.utils.GPS.speed_operation import calculate_speeds
from src.API_OpenSeaMap.plot_gps import plot_gps_route
from src.Database.db_connection import get_db_engine

def main():
    # Opérations liées à la base de données
    engine = get_db_engine()
    #navigation_table = create_navigation_table(engine)

    # Appel des fonctions existantes pour récupérer et traiter les données
    call_data_from_esp()
    navigation_data = choose_file()  # Cette fonction affiche aussi un aperçu des données
    #display_navigation_data(navigation_data)  # Affichage complémentaire si besoin

    # Insertion des données dans la base PostgreSQL
    insert_navigation_data(navigation_data, engine)

    # Appel des autres traitements sur les données extraites
    calculate_distances(navigation_data)
    calculate_speeds(navigation_data)
    plot_gps_route(navigation_data)

    #export_data_to_json() marche pas encore



if __name__ == '__main__':
    main()
