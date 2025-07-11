

import smtplib
import os
from email.message import EmailMessage
import mimetypes

class EmailSenderServices:
    def __init__(self, sender_email, sender_password, smtp_server='smtp.gmail.com', smtp_port=587):
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port

    def send_folder_contents(self, folder_path, subject, body, recipient_emails):
        if not os.path.isdir(folder_path):
            print(f"Erreur : le dossier {folder_path} n'existe pas.")
            return

        # Créer l'e-mail
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = self.sender_email
        msg['To'] = ', '.join(recipient_emails)
        msg.set_content(body)

        # Parcourir les fichiers du dossier
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)

            if os.path.isfile(file_path):
                with open(file_path, 'rb') as f:
                    file_data = f.read()
                    mime_type, _ = mimetypes.guess_type(file_path)
                    maintype, subtype = mime_type.split('/') if mime_type else ('application', 'octet-stream')
                    msg.add_attachment(file_data, maintype=maintype, subtype=subtype, filename=filename)

        # Envoyer via SMTP
        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as smtp:
                smtp.starttls()
                smtp.login(self.sender_email, self.sender_password)
                smtp.send_message(msg)
                print(f"✅ Email envoyé avec succès à {recipient_emails}")
        except Exception as e:
            print(f"❌ Erreur lors de l'envoi de l'e-mail : {e}")