from sqlalchemy import select, MetaData, Table
from db_connection import get_db_engine


def retrieve_data(engine):
    """
    Récupère et affiche toutes les lignes de la table navigation_data.
    """
    metadata = MetaData(bind=engine)
    navigation_table = Table('navigation_data', metadata, autoload_with=engine)

    stmt = select(navigation_table).order_by(navigation_table.c.time)
    with engine.connect() as conn:
        results = conn.execute(stmt).fetchall()
        for row in results:
            print(dict(row))


def main():
    engine = get_db_engine()
    retrieve_data(engine)


if __name__ == "__main__":
    main()
