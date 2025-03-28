from sqlalchemy import MetaData, Table
from sqlalchemy.dialects.postgresql import insert

def insert_navigation_data(db_data, engine):
    """
    Insère les données extraites dans la table existante 'navigation_data'.
    """
    # Charger la table existante par son nom
    metadata = MetaData()
    navigation_table = Table('navigation_data', metadata, autoload_with=engine)

    # Convertir le dictionnaire en liste de lignes
    records = []
    n = len(db_data['time'])
    for i in range(n):
        record = {
            'time': db_data['time'][i],
            'yaw': db_data['yaw'][i],
            'pitch': db_data['pitch'][i],
            'roll': db_data['roll'][i],
            'latitude': db_data['latitude'][i],
            'longitude': db_data['longitude'][i],
            'wind_speed': db_data['wind_speed'][i],
            'wind_direction': db_data['wind_direction'][i]
        }
        records.append(record)

    # Insertion avec gestion des doublons
    with engine.begin() as conn:
        for rec in records:
            stmt = insert(navigation_table).values(**rec).on_conflict_do_nothing(index_elements=['time'])
            conn.execute(stmt)

    print("✅ Données insérées dans la table 'navigation_data' (doublons ignorés).")
