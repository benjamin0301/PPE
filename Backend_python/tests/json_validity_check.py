import json

json_file_path = "../data/json_data_files/navigation_data.json"

try:
    with open(json_file_path, "r") as file:
        data = json.load(file)
    print("✅ Fichier JSON valide !")
except json.JSONDecodeError as e:
    print(f"❌ ERREUR : Fichier JSON mal formé : {e}")
