import cv2, os
import numpy as np
from PIL import ImageFont, ImageDraw, Image

class ContentService:
    def __init__(self, title, description, background, main_content, second_content, file_name, sign_picture=None):
        self.title = title
        self.description = description
        self.background = background
        self.main_content = main_content
        self.second_content = second_content
        self.file_name = file_name
        self.sign_picture = sign_picture

    def generate_content(self):
        # Charger l'image de fond
        image = cv2.imread(self.background)
        if image is None:
            print("Erreur : image de fond non trouvée")
            return

        # Résolution TikTok
        resolution = (540, 960)
        image = cv2.resize(image, resolution)

        # Conversion OpenCV -> PIL
        image_pil = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(image_pil)

        # Chargement de la police
        font_path = "assets/fonts/TikTokSans-Bold.ttf"

        # TAILLES DES POLICES ADAPTÉES EN FONCTION DE LA SIGNATURE
        if self.sign_picture:
            font_main_size = 40
        else:
            font_main_size = 85  # Plus grand si pas de signature

        font_main = ImageFont.truetype(font_path, font_main_size)
        font_second = ImageFont.truetype(font_path, 27)

        max_width = resolution[0] - 100  # marge de 50px
        line_spacing_main = 20
        spacing_between_blocks = 40
        line_spacing_second = 20
        spacing_above_main = 60  # espace entre la signature et le bloc principal

        # Fonction pour découper un texte en lignes
        def wrap_text(text, font, max_width):
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

        # Fonction pour calculer la hauteur totale d’un bloc de texte
        def get_text_block_height(lines, font, spacing):
            return sum([(font.getbbox(line)[3] - font.getbbox(line)[1]) + spacing for line in lines]) - spacing

        lines_main = wrap_text(self.main_content, font_main, max_width)
        lines_second = wrap_text(self.second_content, font_second, max_width)

        height_main = get_text_block_height(lines_main, font_main, line_spacing_main)
        height_second = get_text_block_height(lines_second, font_second, line_spacing_second)
        total_text_height = height_main + spacing_between_blocks + height_second

        sign_img_height = 0
        sign_img_resized = None
        if self.sign_picture:
            try:
                sign_img = Image.open(self.sign_picture).convert("RGBA")
                sign_img_width = 200
                aspect_ratio = sign_img.height / sign_img.width
                sign_img_height = int(sign_img_width * aspect_ratio)
                resample_method = getattr(Image, 'Resampling', Image).LANCZOS
                sign_img_resized = sign_img.resize((sign_img_width, sign_img_height), resample=resample_method)
            except Exception as e:
                print("Erreur lors du chargement de la sign_picture :", e)
                self.sign_picture = None
                sign_img_height = 0

        # Calcul total hauteur (si pas de signature, la police plus grande gère la place)
        total_height = (sign_img_height if self.sign_picture else 0) + spacing_above_main + total_text_height
        start_y = (resolution[1] - total_height) // 2

        # Ajouter l’image de signature si elle existe
        if self.sign_picture and sign_img_resized:
            x_sign = (resolution[0] - sign_img_resized.width) // 2
            image_pil.paste(sign_img_resized, (x_sign, start_y), mask=sign_img_resized)
            start_y += sign_img_height + spacing_above_main
        elif not self.sign_picture:
            # si pas de signature, on peut ajuster start_y un peu pour mieux centrer le texte
            start_y = (resolution[1] - total_text_height) // 2

        # Fonction pour dessiner les lignes
        def draw_lines(lines, font, y_start, spacing):
            y = y_start
            for line in lines:
                bbox = font.getbbox(line)
                text_width = bbox[2] - bbox[0]
                x = (resolution[0] - text_width) // 2
                draw.text((x, y), line, font=font, fill=(255, 255, 255))
                y += (bbox[3] - bbox[1]) + spacing
            return y

        y_after_main = draw_lines(lines_main, font_main, start_y, line_spacing_main)
        y_second_start = y_after_main + spacing_between_blocks
        draw_lines(lines_second, font_second, y_second_start, line_spacing_second)

        # Créer dossier si inexistant
        output_dir = f"results/{self.file_name}"
        os.makedirs(output_dir, exist_ok=True)

        # Nom de fichier propre à partir du titre
        safe_title = "".join(c if c.isalnum() or c in "-_ " else "_" for c in self.title).strip().replace(" ", "_")
        output_path = os.path.join(output_dir, f"{safe_title}.png")

        # Sauvegarde
        image_pil.save(output_path)
        print(f"Image générée et enregistrée dans : {output_path}")