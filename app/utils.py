import uuid
from google.cloud import translate
import openai

from config import settings

openai.api_key = settings.openai_api_key


def gen_uuid():
    return uuid.uuid4()


def translate_text(text, type):
    text = str(text)
    # if type == "q":
    #     paraphrased_text = openai.ChatCompletion.create(
    #         model="gpt-3.5-turbo",
    #         messages=[
    #             {"role": "system", "content": f"Paraphrase the following text to make it sound like you are asking a question: {text}"}]
    #     )
    # elif type == "a":
    #     paraphrased_text = openai.ChatCompletion.create(
    #         model="gpt-3.5-turbo",
    #         messages=[
    #             {"role": "system", "content": f"Paraphrase the following text to make it sound like you are giving an answer to an asked question:: {text}"}]
    #     )
    # elif type == "s":
    #     paraphrased_text = openai.ChatCompletion.create(
    #         model="gpt-3.5-turbo",
    #         messages=[
    #             {"role": "system", "content": f"Paraphrase the following text to make it sound like you are suggesting an action: {text}"}]
    #     )
    # else:
    #     paraphrased_text = text
    project_id="cheers-wisdom-translate"
    client=translate.TranslationServiceClient()
    location="global"
    parent=f"projects/{project_id}/locations/{location}"
    response=client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",
            "source_language_code": "en-US",
            "target_language_code": "hi",
        }
    )
    return response.translations[0].translated_text
