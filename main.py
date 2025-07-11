from services.content_services import ContentService
from services.astrology_services import AstrologyServices
from models.astrology_day import AstrologyDay


signs: list[AstrologyDay] = AstrologyServices().load_content_by_sign()

for sign in signs:

    content_service = ContentService("test", "description_test", "assets/backgrounds/astrology1.jpg", sign.sign, sign.content, sign.picture)
    content_service.generate_content()