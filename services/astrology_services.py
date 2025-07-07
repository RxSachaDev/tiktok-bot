import requests
import json
from models.astrology_day import AstrologyDay

class AstrologyServices:
    def __init__(self) -> None:
        pass

    def load_content_by_sign(self):
        signs = []

        url = "https://kayoo123.github.io/astroo-api/jour.json"

        try:
            response = requests.get(url)
            response.raise_for_status()  # Lève une erreur HTTP si besoin
            data = response.json()

            for signe, message in data.items():
                if signe.lower() != "date":
                    signs.append(AstrologyDay(signe, message, ""))

            print(signs)
            return signs

        except Exception as e:
            print(f"Erreur lors de la récupération des prédictions : {e}")
            return []