from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from dotenv import load_dotenv
import os

# Charger les variables d'environnement depuis .env
load_dotenv()

# Récupérer les informations de connexion depuis .env
DATABASE_URI = os.getenv("DATABASE_URI")

def get_db_engine():
    """
    Crée et retourne un moteur SQLAlchemy connecté à la base de données PostgreSQL.
    """
    try:
        engine = create_engine(DATABASE_URI)
        # Test de la connexion
        with engine.connect() as connection:
            print("Connexion réussie à la base de données.")
        return engine
    except OperationalError as e:
        print(f"Erreur de connexion à la base de données : {e}")
        raise
