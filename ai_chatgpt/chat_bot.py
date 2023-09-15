import openai

from utils.settings import APIKEY_AI

openai.api_key = APIKEY_AI


def discord_chat_gpt(user_input):
    messages = [{"role": "user", "content": user_input}]
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
    chat_reply = response["choices"][0]["message"]["content"]

    return chat_reply
