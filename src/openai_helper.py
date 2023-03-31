import openai
import os

# Put your API key here
API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = API_KEY
model_id = "gpt-3.5-turbo"


def get_chat_response(message):
    completion = openai.ChatCompletion.create(
        model=model_id, messages=[{"role": "user", "content": message}]
    )
    content = completion.choices[0].message.content
    return content
