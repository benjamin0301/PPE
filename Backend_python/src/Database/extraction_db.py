import json
from sqlalchemy import Table, MetaData, select
from src.Database.db_connection import get_db_engine

def export_data_to_json(filename="Nautikos_db.json"):
    engine = get_db_engine()
    metadata = MetaData()
    navigation_table = Table("navigation_data", metadata, autoload_with=engine)

    with engine.connect() as conn:
        results = conn.execute(select(navigation_table)).fetchall()
        rows = [dict(row) for row in results]

    with open(filename, "w") as f:
        json.dump(rows, f, indent=4, default=str)

    print(f"✅ Données exportées dans {filename}")
