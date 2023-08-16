import uuid
from google.cloud import translate


def gen_uuid():
    return uuid.uuid4()


def translate_text(text):
    text = str(text)
    project_id="cheers-wisdom-translate"
    client = translate.TranslationServiceClient()
    location = "global"
    parent = f"projects/{project_id}/locations/{location}"
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",
            "source_language_code": "en-US",
            "target_language_code": "hi",
        }
    )
    return response.translations[0].translated_text
