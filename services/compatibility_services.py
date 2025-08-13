import random
from models.astrology_compatibility import AstrologyCompatibility

class CompatibilityService:
    def __init__(self):
        pass

    def generate_couple(self):
        signs = [
            "Bélier", "Taureau", "Gémeaux", "Cancer", "Lion",
            "Vierge", "Balance", "Scorpion", "Sagittaire", "Capricorne",
            "Verseau", "Poissons"
        ]
        
        sign1 = random.choice(signs)
        sign2 = random.choice(signs)
        
        return sign1, sign2

    def generate_compatibility(self):
        
        relations = [
            "Amour infini",
            "Superbe rencontre",
            "Âme sœur",
            "Coup de foudre",
            "Pire ennemi",
            "Amitié sincère",
            "Lien éternel",
            "Passion folle",
            "Amour perdu",
            "Très proche",
            "Premier amour",
            "Frère de cœur",
            "Sœur de cœur",
            "Grand soutien",
            "Complice fidèle",
            "Ex inoubliable",
            "Rival juré",
            "Allié précieux",
            "Partenaire parfait",
            "Ancien amour",
            "Crush secret",
            "Relation toxique",
            "Béguin d'enfance",
            "Trahison amère",
            "Amour caché",
            "Complice de vie",
            "Meilleur ami",
            "Meilleure amie",
            "Ennemi juré",
            "Idylle courte",
            "Relation secrète",
            "Rencontre magique",
            "Coup de cœur",
            "Grand amour",
            "Ancienne flamme",
            "Âme perdue",
            "Passion éphémère",
            "Énergie positive",
            "Lien brisé",
            "Harmonie parfaite",
            "Guerre froide",
            "Fidèle allié",
            "Ex proche",
            "Confident secret",
            "Muse inspirante",
            "Inspiration quotidienne",
            "Ombre menaçante",
            "Ennemi intime",
            "Partenaire d'aventure",
            "Âme jumelle",
            "Guide précieux",
            "Compagnon fidèle",
            "Lien incassable",
            "Rivalité amicale",
            "Vieux complice",
            "Amour interdit",
            "Colère froide",
            "Profonde rancune",
            "Grand rival",
            "Très inspirant",
            "Présence rassurante",
            "Animosité forte",
            "Soutien constant",
            "Partage unique",
            "Regard complice",
            "Sourire rassurant",
            "Respect mutuel",
            "Haine tenace",
            "Défi permanent",
            "Allié secret",
            "Jalousie cachée",
            "Amour fragile",
            "Relation brisée",
            "Passion brûlante",
            "Espoir commun",
            "Force tranquille",
            "Souvenir doux",
            "Méfiance réciproque",
            "Bienveillance sincère",
            "Hostilité ouverte",
            "Lien sacré",
            "Fidélité absolue",
            "Clash régulier",
            "Affection profonde",
            "Tendresse infinie",
            "Fascination mutuelle",
            "Tension constante",
            "Connivence totale",
            "Admiration partagée",
            "Blessure ancienne",
            "Promesse tenue",
            "Projet commun",
            "Avenir incertain",
            "Espoir brisé",
            "Envie partagée",
            "Futur ensemble",
            "Lien unique",
            "Rivalité féroce",
            "Affection cachée"
        ]

        return random.choice(relations)
    
    def generate_content(self):

        couples = []
        results = []

        for _ in range(20):

            sign1, sign2 = self.generate_couple()

            while (sign1, sign2) in couples or (sign2, sign1) in couples:
                sign1, sign2 = self.generate_couple()

            relation = self.generate_compatibility()
            compatibility = AstrologyCompatibility(sign1, sign2, relation)
            couples.append((sign1, sign2))
            results.append(compatibility)  
        
        return results