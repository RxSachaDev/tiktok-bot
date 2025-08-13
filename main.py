from services.content_services import ContentService
from services.astrology_services import AstrologyServices
from models.astrology_day import AstrologyDay
from services.email_sender_services import EmailSenderServices
from services.compatibility_services import CompatibilityService
from services.compatibility_content_services import CompatibilityContentServices

from services.letter_services import LetterServices
from models.one_letter_one_sentence import OneLetterOneSentence

import json, os, shutil

with open("counter.txt", "r") as f:
    count = int(f.read())


# # Astrology day
with open('config.json', 'r') as f:
    config = json.load(f)

signs: list[AstrologyDay] = AstrologyServices().load_content_by_sign()

for sign in signs:
    content_service = ContentService(sign.sign, "description_test", f"assets/backgrounds/astrology{count}.jpg", sign.sign, sign.content, "astrology_day", sign.picture)
    content_service.generate_content()

email_sender = EmailSenderServices(
    sender_email=config["EMAIL"],
    sender_password=config["PASSWORD"]  # Utilise un mot de passe d’application si tu es sur Gmail
)

email_sender.send_folder_contents(
    folder_path="results/astrology_day",
    subject="Astrology du jour",
    body="Voici les contenus astrologiques du jour.",
    recipient_emails=[config["EMAIL"]]
)

# Astrology compatibility

folder = "./results/compatibility_result"
for filename in os.listdir(folder):
    file_path = os.path.join(folder, filename)
    if os.path.isfile(file_path) or os.path.islink(file_path):
        os.unlink(file_path)
    elif os.path.isdir(file_path):
        shutil.rmtree(file_path)

compatibility_service = CompatibilityService().generate_content()
for compatibility in compatibility_service:
    content_service = CompatibilityContentServices(
        compatibility.sign1,
        compatibility.sign2,
        compatibility.relation,
        f"assets/backgrounds/couple{count}.jpg"
    )
    content_service.generate_content()

email_sender.send_folder_contents(
    folder_path="results/compatibility_result",
    subject="Compatibilité astrologique",
    body="Voici les contenus de compatibilité astrologique.",
    recipient_emails=[config["EMAIL"]]
)

if count == 5:
    count = 1
else:
    count += 1
    
with open("counter.txt", "w") as f:
    f.write(str(count))


# One letter one sentence

# letters: list[OneLetterOneSentence] = LetterServices().load_content_by_letter()

# for letter in letters:

#     content_service = ContentService(letter.letter, "description_test", "assets/backgrounds/one_letter_one_sentence.jpg", letter.letter, letter.message, "one_letter_one_sentence")
#     content_service.generate_content()

# email_sender = EmailSenderServices(
#     sender_email=config['EMAIL'],
#     sender_password=config["PASSWORD"]  # Utilise un mot de passe d’application si tu es sur Gmail
# )

# email_sender.send_folder_contents(
#     folder_path="results/one_letter_one_sentence",
#     subject="Une lettre une phrase",
#     body="Voici les contenus par lettre du jour.",
#     recipient_emails=[config['EMAIL']]
# )