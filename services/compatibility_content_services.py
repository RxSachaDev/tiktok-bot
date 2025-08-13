import cv2, os
from PIL import ImageFont, ImageDraw, Image

class CompatibilityContentServices:
    def __init__(self, sign1, sign2, relation, background):
        self.sign1 = sign1
        self.sign2 = sign2
        self.relation = relation
        self.background = background
        self.file_name = "compatibility_result"
        self.title = f"{sign1}_{sign2}"

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
        font_relation = ImageFont.truetype(font_path, 50)  # police réduite
        font_sign = ImageFont.truetype(font_path, 40)

        # Afficher la relation au centre (remontée de 200px)
        bbox_rel = font_relation.getbbox(self.relation)
        rel_width = bbox_rel[2] - bbox_rel[0]
        rel_height = bbox_rel[3] - bbox_rel[1]
        rel_x = (resolution[0] - rel_width) // 2
        rel_y = (resolution[1] - rel_height) // 2 - 200
        draw.text((rel_x, rel_y), self.relation, font=font_relation, fill=(255, 255, 255))

        # Position intermédiaire pour les signes (≈ 55% de la hauteur totale)
        sign_y_position = int(resolution[1] * 0.55)

        # Signe 1 à gauche
        bbox_s1 = font_sign.getbbox(self.sign1)
        s1_width = bbox_s1[2] - bbox_s1[0]
        draw.text((50, sign_y_position), self.sign1, font=font_sign, fill=(255, 255, 255))

        # Signe 2 à droite
        bbox_s2 = font_sign.getbbox(self.sign2)
        s2_width = bbox_s2[2] - bbox_s2[0]
        draw.text((resolution[0] - s2_width - 50, sign_y_position), self.sign2, font=font_sign, fill=(255, 255, 255))

        # Sauvegarde
        output_dir = f"results/{self.file_name}"
        os.makedirs(output_dir, exist_ok=True)
        safe_title = "".join(c if c.isalnum() or c in "-_ " else "_" for c in self.title).strip().replace(" ", "_")
        output_path = os.path.join(output_dir, f"{safe_title}.png")
        image_pil.save(output_path)
        print(f"Image générée et enregistrée dans : {output_path}")