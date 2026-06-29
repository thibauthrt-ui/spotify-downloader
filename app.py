import streamlit as st
import subprocess
import os
import shutil

# Configuration de la page web
st.set_page_config(page_title="Spotify Downloader", page_icon="🎵", layout="centered")

st.title("Téléchargeur de Playlist Spotify 🎵")
st.write("Entrez le lien d'une playlist Spotify pour récupérer les fichiers MP3.")

# Zone de saisie du lien
url_playlist = st.text_input("Lien de la playlist Spotify :", placeholder="https://open.spotify.com/playlist/...")

# Dossier temporaire sur le serveur pour stocker les musiques
DOSSIER_TELECHARGEMENT = "musiques_temporaires"

if st.button("Préparer le téléchargement", type="primary"):
    if url_playlist:
        # Nettoyage d'un ancien téléchargement s'il existe
        if os.path.exists(DOSSIER_TELECHARGEMENT):
            shutil.rmtree(DOSSIER_TELECHARGEMENT)
        os.makedirs(DOSSIER_TELECHARGEMENT)
        
        st.info("Le serveur traite votre playlist... Cela peut prendre quelques minutes selon sa taille.")
        
        # Commande spotdl adaptée pour le serveur (sans dossier local Windows)
       # Commande simplifiée et optimisée pour Linux (Streamlit Cloud)
     # Commande simplifiée au maximum pour éviter les bugs d'accolades
        commande = [
            "spotdl",
            "download",
            url_playlist,
            "--generate-lrc"
        ]
        
        try:
            # Exécution de spotdl
            subprocess.run(commande, check=True)
            
            # Vérifier si des fichiers ont bien été téléchargés
            fichiers = os.listdir(DOSSIER_TELECHARGEMENT)
            if fichiers:
                st.success(f"Téléchargement réussi sur le serveur ! ({len(fichiers)} fichiers récupérés)")
                
                # Création d'une archive ZIP pour l'utilisateur
                nom_archive = "MaPlaylist_Spotify"
                shutil.make_archive(nom_archive, 'zip', DOSSIER_TELECHARGEMENT)
                fichier_zip = f"{nom_archive}.zip"
                
                # Lecture du fichier ZIP pour le proposer au téléchargement
                with open(fichier_zip, "rb") as f:
                    st.download_button(
                        label="📥 Télécharger ma playlist (.ZIP)",
                        data=f,
                        file_name="MaPlaylist_Spotify.zip",
                        mime="application/zip"
                    )
                
                # Nettoyage après création du ZIP
                shutil.rmtree(DOSSIER_TELECHARGEMENT)
                if os.path.exists(fichier_zip):
                    os.remove(fichier_zip)
            else:
                st.error("Le dossier est vide. Vérifiez que le lien de la playlist est public.")
                
        except subprocess.CalledProcessError as e:
            st.error("Une erreur est survenue lors de l'exécution de spotdl.")
            st.code(str(e))
    else:
        st.warning("Veuillez coller un lien de playlist valide.")
