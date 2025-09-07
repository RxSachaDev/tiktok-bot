from models.astrology_day import AstrologyDay
import os, json, requests
import azure.cognitiveservices.speech as speechsdk

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
                    signs.append(AstrologyDay(signe.upper(), message, f"assets/signs/{signe}.png"))

            return signs

        except Exception as e:
            print(f"Erreur lors de la récupération des prédictions : {e}")
            return []
        
    def load_content_by_sign_voice(self):
        with open('config.json', 'r') as f:
            config = json.load(f)

        signs: list[AstrologyDay] = self.load_content_by_sign()

        speech_key = config["AZURE_SPEECH_KEY"]
        service_region = "francecentral"
        output_dir = "results/astrology_voice"
        os.makedirs(output_dir, exist_ok=True)

        speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
        speech_config.speech_synthesis_voice_name = "fr-FR-DeniseNeural"

        for sign in signs:
            texte = f"Pour l'horoscope du signe {sign.sign}. {sign.content}"
            audio_path = os.path.join(output_dir, f"{sign.sign}.wav")
            timing_path = os.path.join(output_dir, f"{sign.sign}_timings.json")
            try:
                audio_config = speechsdk.audio.AudioOutputConfig(filename=audio_path)
                synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

                word_timings = []

                def on_word_boundary(evt):
                    word_timings.append({
                        "text": evt.text,
                        "offset": evt.audio_offset / 10000  # ms
                    })

                synthesizer.synthesis_word_boundary.connect(on_word_boundary)
                result = synthesizer.speak_text_async(texte).get()
                if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
                    print(f"Audio généré pour {sign.sign}: {audio_path}")
                    with open(timing_path, "w", encoding="utf-8") as f:
                        json.dump(word_timings, f, ensure_ascii=False, indent=2)
                else:
                    cancellation_details = result.cancellation_details
                    print(f"Erreur synthèse pour {sign.sign}: {result.reason}")
                    print(f"Détails annulation: {cancellation_details.reason}")
                    if cancellation_details.error_details:
                        print(f"Erreur Azure: {cancellation_details.error_details}")
            except Exception as e:
                print(f"Erreur pour le signe {sign.sign}: {e}")
                print(f"Texte envoyé: {texte}")


