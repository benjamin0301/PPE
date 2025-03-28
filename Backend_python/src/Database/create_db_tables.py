
from sqlalchemy import MetaData, Table, Column, Integer, Float, String, TIMESTAMP, UniqueConstraint


def create_navigation_table(engine):
    """
    Crée la table 'navigation_data' avec les colonnes adaptées et une contrainte UNIQUE sur la colonne time.
    """
    metadata = MetaData()
    navigation_table = Table(
        'navigation_data', metadata,
        Column('id', Integer, primary_key=True, autoincrement=True),
        Column('time', TIMESTAMP, unique=True, nullable=False),
        Column('yaw', Float),
        Column('pitch', Float),
        Column('roll', Float),
        Column('latitude', Float),
        Column('longitude', Float),
        Column('wind_speed', Float),
        Column('wind_direction', String(10)),
        UniqueConstraint('time', name='uq_navigation_time')
    )
    metadata.create_all(engine)
    print("Table 'navigation_data' créée (si elle n'existait pas déjà).")
    return navigation_table
