import streamlit as st
import subprocess
import os
import shutil

st.set_page_config(page_title="Hébergeur Downloader", page_icon="🎵", layout="centered")
st.title("Téléchargeur de Musique en Ligne 🎵")
st.write("Collez un lien YouTube, YouTube Music ou Spotify (converti via YT).")

url_playlist = st.text_input("Lien de la musique ou playlist :", placeholder="https://...")
DOSSIER_TELECHARGEMENT = "musiques_temporaires"

if st.button("Préparer le téléchargement", type="primary"):
    if url_playlist:
        if os.path.exists(DOSSIER_TELECHARGEMENT):
            shutil.rmtree(DOSSIER_TELECHARGEMENT)
        os.makedirs(DOSSIER_TELECHARGEMENT)
        
        st.info("Traitement en cours... Veuillez patienter.")
        
        # Commande robuste utilisant yt-dlp directement pour extraire le MP3
        commande = [
            "yt-dlp",
            "-x",
            "--audio-format", "mp3",
            "--audio-quality", "0",
            "-o", f"{DOSSIER_TELECHARGEMENT}/%(title)s.%(ext)s",
            url_playlist
        ]
        
        try:
            subprocess.run(commande, check=True)
            fichiers = os.listdir(DOSSIER_TELECHARGEMENT)
            
            if fichiers:
                st.success(f"Récupération réussie ! ({len(fichiers)} fichier(s) prêt(s))")
                
                nom_archive = "MaPlaylist"
                shutil.make_archive(nom_archive, 'zip', DOSSIER_TELECHARGEMENT)
                fichier_zip = f"{nom_archive}.zip"
                
                with open(fichier_zip, "rb") as f:
                    st.download_button(
                        label="📥 Télécharger les fichiers (.ZIP)",
                        data=f,
                        file_name="Playlist.zip",
                        mime="application/zip"
                    )
                
                shutil.rmtree(DOSSIER_TELECHARGEMENT)
                if os.path.exists(fichier_zip):
                    os.remove(fichier_zip)
            else:
                st.error("Aucun fichier n'a pu être extrait.")
        except subprocess.CalledProcessError as e:
            st.error("Le serveur a rencontré une erreur de conversion.")
    else:
        st.warning("Veuillez entrer un lien valide.")
