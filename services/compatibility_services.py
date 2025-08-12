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
            "amour infini",
            "superbe rencontre",
            "âme sœur",
            "coup de foudre",
            "pire ennemi",
            "amitié sincère",
            "lien éternel",
            "passion folle",
            "amour perdu",
            "très proche",
            "premier amour",
            "frère de cœur",
            "sœur de cœur",
            "grand soutien",
            "complice fidèle",
            "ex inoubliable",
            "rival juré",
            "allié précieux",
            "partenaire parfait",
            "ancien amour",
            "crush secret",
            "relation toxique",
            "béguin d'enfance",
            "trahison amère",
            "amour caché",
            "complice de vie",
            "meilleur ami",
            "meilleure amie",
            "ennemi juré",
            "idylle courte",
            "relation secrète",
            "rencontre magique",
            "coup de cœur",
            "grand amour",
            "ancienne flamme",
            "âme perdue",
            "passion éphémère",
            "énergie positive",
            "lien brisé",
            "harmonie parfaite",
            "guerre froide",
            "fidèle allié",
            "ex proche",
            "confident secret",
            "muse inspirante",
            "inspiration quotidienne",
            "ombre menaçante",
            "ennemi intime",
            "partenaire d'aventure",
            "âme jumelle",
            "guide précieux",
            "compagnon fidèle",
            "lien incassable",
            "rivalité amicale",
            "vieux complice",
            "amour interdit",
            "colère froide",
            "profonde rancune",
            "grand rival",
            "très inspirant",
            "présence rassurante",
            "animosité forte",
            "soutien constant",
            "partage unique",
            "regard complice",
            "sourire rassurant",
            "respect mutuel",
            "haine tenace",
            "défi permanent",
            "allié secret",
            "jalousie cachée",
            "amour fragile",
            "relation brisée",
            "passion brûlante",
            "espoir commun",
            "force tranquille",
            "souvenir doux",
            "méfiance réciproque",
            "bienveillance sincère",
            "hostilité ouverte",
            "lien sacré",
            "fidélité absolue",
            "clash régulier",
            "affection profonde",
            "tendresse infinie",
            "fascination mutuelle",
            "tension constante",
            "connivence totale",
            "admiration partagée",
            "blessure ancienne",
            "promesse tenue",
            "projet commun",
            "avenir incertain",
            "espoir brisé",
            "envie partagée",
            "futur ensemble",
            "lien unique",
            "rivalité féroce",
            "affection cachée"
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