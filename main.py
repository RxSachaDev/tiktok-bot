from services.content_services import ContentService
from services.astrology_services import AstrologyServices
from models.astrology_day import AstrologyDay
from services.email_sender_services import EmailSenderServices

import json

with open('config.json', 'r') as f:
    config = json.load(f)

signs: list[AstrologyDay] = AstrologyServices().load_content_by_sign()

for sign in signs:

    content_service = ContentService(sign.sign, "description_test", "assets/backgrounds/astrology1.jpg", sign.sign, sign.content, sign.picture)
    content_service.generate_content()

email_sender = EmailSenderServices(
    sender_email=config['EMAIL'],
    sender_password=config["PASSWORD"]  # Utilise un mot de passe d’application si tu es sur Gmail
)

email_sender.send_folder_contents(
    folder_path="results/astrology_day",
    subject="Astrology du jour",
    body="Voici les contenus astrologiques du jour.",
    recipient_emails=[config['EMAIL']]
)