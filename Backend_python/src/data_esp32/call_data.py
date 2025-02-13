import os
import requests

# 📌 Adresse IP de l'ESP32 (modifie si nécessaire)
ESP32_IP = "192.168.4.1"
LIST_FILES_URL = f"http://{ESP32_IP}/list"
DOWNLOAD_URL = f"http://{ESP32_IP}/download"

# 📌 Dossier où enregistrer les fichiers téléchargés
LOCAL_SAVE_FOLDER = os.path.join(os.path.dirname(__file__), "../../data/json_data_files/")

# 🔹 Créer le dossier s'il n'existe pas
os.makedirs(LOCAL_SAVE_FOLDER, exist_ok=True)

def get_file_list():
    """Récupère la liste des fichiers stockés sur l'ESP32"""
    try:
        response = requests.get(LIST_FILES_URL, timeout=5)
        if response.status_code == 200:
            file_list = response.json().get("files", [])
            return file_list
        else:
            print("❌ Erreur lors de la récupération de la liste des fichiers.")
            return []
    except requests.exceptions.RequestException as e:
        print(f"🚨 Erreur de connexion à l'ESP32 : {e}")
        return []

def download_file(file_name):
    """Télécharge un fichier depuis l'ESP32 dans le dossier `data/json_data_files/`"""
    file_url = f"{DOWNLOAD_URL}?file={file_name}"
    local_path = os.path.join(LOCAL_SAVE_FOLDER, file_name)

    try:
        response = requests.get(file_url, timeout=10)
        if response.status_code == 200:
            with open(local_path, "wb") as file:
                file.write(response.content)
            print(f"✅ Téléchargé : {file_name} → {local_path}")
        else:
            print(f"❌ Impossible de télécharger {file_name}")
    except requests.exceptions.RequestException as e:
        print(f"🚨 Erreur lors du téléchargement de {file_name} : {e}")

def main():
    print("🔄 Récupération de la liste des fichiers...")
    file_list = get_file_list()

    if not file_list:
        print("❌ Aucun fichier trouvé sur l'ESP32.")
        return

    print(f"📂 {len(file_list)} fichiers trouvés : {file_list}")

    # 📌 Téléchargement de chaque fichier vers `data/json_data_files/`
    for file_name in file_list:
        download_file(file_name)

    print("🎉 Tous les fichiers ont été récupérés avec succès dans :", LOCAL_SAVE_FOLDER)

if __name__ == "__main__":
    main()
