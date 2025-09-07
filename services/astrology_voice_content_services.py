import cv2
import numpy as np
import json
import os
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.video.io.ImageSequenceClip import ImageSequenceClip
from moviepy.editor import VideoFileClip, concatenate_videoclips
from PIL import ImageFont, ImageDraw, Image

class AstrologyVoiceContentServices:
    def __init__(self, background, sign):
        self.background = background
        self.sign = sign

    def wrap_text(self, text, font, max_width):
        words = text.split()
        lines = []
        current_line = ""
        for word in words:
            test_line = current_line + " " + word if current_line else word
            bbox = font.getbbox(test_line)
            if bbox[2] - bbox[0] > max_width:
                lines.append(current_line)
                current_line = word
            else:
                current_line = test_line
        if current_line:
            lines.append(current_line)
        return lines

    def generate_video(self, audio_dir="results/astrology_voice", output_dir="results/astrology_video"):
        # Préparer les chemins
        audio_path = os.path.join(audio_dir, f"{self.sign}.wav")
        timing_path = os.path.join(audio_dir, f"{self.sign}_timings.json")
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, f"{self.sign}.mp4")

        # Charger les timings
        with open(timing_path, "r", encoding="utf-8") as f:
            timings = json.load(f)

        # Charger l'audio
        audio_clip = AudioFileClip(audio_path)
        duration = audio_clip.duration

        # Charger et préparer l'image de fond
        bg_img = cv2.imread(self.background)
        if bg_img is None:
            raise ValueError(f"Impossible de charger l'image : {self.background}")
        bg_img = cv2.resize(bg_img, (540, 960))  # Résolution TikTok

        # Configuration du texte
        font_path = "assets/fonts/TikTokSans-Bold.ttf"
        font_size = 40
        font = ImageFont.truetype(font_path, font_size)
        max_width = 440  # 540 - 100 (marge de 50px de chaque côté)
        line_spacing = 20
        max_lines = 6
        fps = 25

        # Générer les frames
        frames = []
        current_text = ""
        timing_idx = 0

        for t in range(int(duration * fps)):
            time_ms = t * 1000 / fps
            
            # Mettre à jour le texte selon le timing
            while timing_idx < len(timings) and timings[timing_idx]["offset"] <= time_ms:
                current_text += timings[timing_idx]["text"] + " "
                timing_idx += 1
            
            # Convertir l'image OpenCV en image PIL
            frame_pil = Image.fromarray(cv2.cvtColor(bg_img.copy(), cv2.COLOR_BGR2RGB))
            draw = ImageDraw.Draw(frame_pil)
            
            # Découper le texte en lignes
            lines = self.wrap_text(current_text, font, max_width)
            
            # Garder seulement les 6 dernières lignes si dépassement
            if len(lines) > max_lines:
                lines = lines[-max_lines:]
            
            # Calculer la hauteur totale du bloc de texte
            total_height = sum([(font.getbbox(line)[3] - font.getbbox(line)[1]) + line_spacing for line in lines]) - line_spacing
            
            # Position Y de départ pour centrer le bloc de texte
            start_y = (960 - total_height) // 2
            
            # Dessiner chaque ligne
            y = start_y
            for line in lines:
                bbox = font.getbbox(line)
                text_width = bbox[2] - bbox[0]
                x = (540 - text_width) // 2
                
                # Dessiner le texte (sans fond semi-transparent)
                draw.text((x, y), line, font=font, fill=(255, 255, 255))
                y += bbox[3] - bbox[1] + line_spacing
            
            # Convertir l'image PIL en array numpy pour MoviePy
            frame_array = np.array(frame_pil)
            frames.append(frame_array)

        try:
            # Créer le clip vidéo
            video = ImageSequenceClip(frames, fps=fps)
            video.audio = audio_clip
            
            # Générer la vidéo finale
            video.write_videofile(
                output_path,
                fps=fps,
                codec='libx264',
                audio_codec='aac',
                temp_audiofile='temp-audio.m4a',
                remove_temp=True
            )
            print(f"Vidéo générée avec succès : {output_path}")
            
        except Exception as e:
            print(f"Erreur lors de la génération de la vidéo : {e}")
            
        finally:
            try:
                video.close()
                audio_clip.close()
            except:
                pass

    def merge_videos(self, input_dir="results/astrology_video", output_dir="results/astrology_video_result"):
        """Concatène les fichiers MP4 en deux vidéos : 6 premiers signes et 6 derniers"""
        try:
            # Créer les dossiers s'ils n'existent pas
            os.makedirs(input_dir, exist_ok=True)
            os.makedirs(output_dir, exist_ok=True)

            # Récupérer tous les fichiers MP4
            video_files = [f for f in os.listdir(input_dir) if f.endswith('.mp4')]
            if not video_files:
                print("Aucun fichier MP4 trouvé dans le dossier.")
                return

            # Trier les fichiers
            video_files.sort()
            
            # Séparer en deux groupes
            first_half = video_files[:6]
            second_half = video_files[6:]

            # Fonction helper pour créer une vidéo à partir d'une liste de fichiers
            def create_merged_video(files, output_name):
                clips = []
                output_file = os.path.join(output_dir, output_name)
                
                for file in files:
                    file_path = os.path.join(input_dir, file)
                    try:
                        clip = VideoFileClip(file_path)
                        clips.append(clip)
                        print(f"Ajout de {file}")
                    except Exception as e:
                        print(f"Erreur lors du chargement de {file}: {e}")

                if clips:
                    final_clip = concatenate_videoclips(clips, method="chain")
                    final_clip.write_videofile(
                        output_file,
                        fps=25,
                        codec='libx264',
                        audio_codec='aac'
                    )
                    # Nettoyer
                    for clip in clips:
                        clip.close()
                    final_clip.close()

            # Créer la première vidéo (6 premiers signes)
            if first_half:
                print("\nCréation de la première vidéo (6 premiers signes)...")
                create_merged_video(first_half, "final_astrology_part1.mp4")

            # Créer la deuxième vidéo (6 derniers signes)
            if second_half:
                print("\nCréation de la deuxième vidéo (6 derniers signes)...")
                create_merged_video(second_half, "final_astrology_part2.mp4")

            print("Fusion des vidéos terminée")
            
        except Exception as e:
            print(f"Erreur lors de la fusion des vidéos : {e}")