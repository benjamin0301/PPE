import os
import requests

# 📌 Adresse IP de l'ESP32 (modifie si nécessaire)
ESP32_IP = "192.168.4.1"
DOWNLOAD_URL = f"http://{ESP32_IP}/download"

# 📌 Dossier où enregistrer les fichiers téléchargés
LOCAL_SAVE_FOLDER = os.path.join(os.path.dirname(__file__), "../../data/json_data_files/")
os.makedirs(LOCAL_SAVE_FOLDER, exist_ok=True)


def get_file_list():
    """Récupère la liste des fichiers stockés sur l'ESP32"""
    try:
        print(f"🔄 Envoi de la requête GET à : {DOWNLOAD_URL}")
        response = requests.get(DOWNLOAD_URL, timeout=2)
        print(f"Réponse du serveur (code) : {response.status_code}")

        if response.status_code == 200:
            try:
                json_data = response.json()
                print("Contenu JSON reçu :", json_data)
            except Exception as e:
                print("🚨 Erreur lors de la conversion de la réponse en JSON :", e)
                return []
            file_list = json_data.get("files", []) if isinstance(json_data, dict) else json_data
            if not isinstance(file_list, list):
                file_list = [file_list]
            return file_list
        else:
            print(f"❌ Erreur HTTP {response.status_code} lors de la récupération des fichiers.")
            print("Contenu de la réponse :", response.text)
            return []
    except requests.exceptions.Timeout:
        print("🚨 Timeout : Le délai d'attente pour la connexion a expiré.")
        return []
    except requests.exceptions.ConnectionError:
        print("🚨 Erreur de connexion : Impossible de se connecter à l'ESP32.")
        return []
    except requests.exceptions.RequestException as e:
        print(f"🚨 Erreur de requête : {e}")
        return []


def download_file(file_info):
    """Télécharge un fichier depuis l'ESP32 dans le dossier data/json_data_files/"""
    # Si file_info est un dictionnaire, extraire le nom du fichier.
    if isinstance(file_info, dict):
        file_name = file_info.get("file", "")
    else:
        file_name = file_info

    # Vérifier que file_name est bien une chaîne non vide
    if not isinstance(file_name, str) or not file_name.strip():
        print("❌ Nom de fichier invalide :", file_name)
        return

    # Définir le chemin local du fichier à télécharger
    local_path = os.path.join(LOCAL_SAVE_FOLDER, file_name)

    # Vérifier si le fichier existe déjà
    if os.path.exists(local_path):
        print(f"ℹ️ Le fichier {file_name} existe déjà dans {LOCAL_SAVE_FOLDER}. Téléchargement ignoré.")
        return

    file_url = f"{DOWNLOAD_URL}?file={file_name}"
    print(f"🔄 Téléchargement du fichier depuis : {file_url}")
    try:
        response = requests.get(file_url, timeout=10)
        print(f"Réponse du serveur pour le téléchargement ({file_name}) : {response.status_code}")
        if response.status_code == 200:
            with open(local_path, "wb") as file:
                file.write(response.content)
            print(f"✅ Téléchargé : {file_name} → {local_path}")
        else:
            print(f"❌ Impossible de télécharger {file_name}. Code HTTP : {response.status_code}")
            print("Contenu de la réponse :", response.text)
    except requests.exceptions.RequestException as e:
        print(f"🚨 Erreur lors du téléchargement de {file_name} : {e}")


def call_data_from_esp():
    print("🔄 Récupération de la liste des fichiers...")
    print("COUCOU____1")

    file_list = get_file_list()
    print("COUCOU___2")

    if not file_list:
        print("❌ Aucun fichier trouvé sur l'ESP32.")
        return
    print("COUCOU___3")

    print(f"📂 {len(file_list)} fichiers trouvés : {file_list}")
    print("COUCOU___4")
    # Téléchargement de chaque fichier vers data/json_data_files/
    for file_name in file_list:
        download_file(file_name)

    print("🎉 Tous les fichiers ont été récupérés avec succès dans :", LOCAL_SAVE_FOLDER)


if __name__ == "__main__":
    call_data_from_esp()
