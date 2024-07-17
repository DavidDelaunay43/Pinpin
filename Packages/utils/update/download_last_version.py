import requests
import shutil
import os

def download_github_repo(repo_url, save_path):
    # Construire l'URL pour télécharger le dépôt en tant qu'archive zip
    if repo_url.endswith('/'):
        repo_url = repo_url[:-1]
    download_url = repo_url + '/archive/refs/heads/main.zip'

    # Envoyer une requête GET à l'URL de téléchargement
    response = requests.get(download_url, stream=True)

    # Vérifier si la requête a réussi
    if response.status_code == 200:
        # Ouvrir un fichier en mode écriture binaire pour enregistrer le contenu téléchargé
        with open(save_path, 'wb') as file:
            # Utiliser shutil pour copier le contenu de la réponse dans le fichier
            shutil.copyfileobj(response.raw, file)
        print(f"Téléchargement réussi : {save_path}")
    else:
        print(f"Erreur lors du téléchargement : {response.status_code}")

# Exemple d'utilisation
repo_url: str = 'https://github.com/DavidDelaunay43/Pinpin/tree/install'
save_path: str = os.path.join(os.path.expanduser("~"), 'Downloads','Pinpin-install.zip')
download_github_repo(repo_url, save_path)
