import openai
import genanki
import random
import os

# Put your API key here
openai.api_key = os.getenv("OPENAI_API_KEY")
model_id = "gpt-3.5-turbo"

# Change the quantity of phrases or words you want to generate
QUANT = 3


def chat_completion(message):
    completion = openai.ChatCompletion.create(
        model=model_id, messages=[{"role": "user", "content": message}]
    )
    content = completion.choices[0].message.content
    return content


def format_reply(content):
    reply = content.split("\n")
    for i, v in enumerate(reply):
        if "1)" in v:
            reply[i] = v.replace(f"{i+1}) ", "")
        else:
            reply[i] = v.replace(f"{i+1}. ", "")
        card = reply[i].split("|")
        reply[i] = card
    return reply


def create_note(model, card):
    note = genanki.Note(model=model, fields=card)
    return note


def gen_id():
    id = random.randrange(1 << 30, 1 << 31)
    return id


def create_model(id=gen_id()):
    model = genanki.Model(
        id,
        "Simple Model",
        fields=[
            {"name": "Question"},
            {"name": "Answer"},
        ],
        templates=[
            {
                "name": "Card 1",
                "qfmt": "{{Question}}",
                "afmt": '{{FrontSide}}<hr id="answer">{{Answer}}',
            },
        ],
    )
    return model


def main():
    # Modify the deck name
    deck_name = "Frases Cotidianas em Espanhol"
    # Customize flashcard content
    message = f"""Faça {QUANT} Flashcards com frases cotidianas em espanhol para
    português seguindo essa formatação: [concept] | [answer]."""

    content = chat_completion(message)
    reply = format_reply(content)
    model = create_model()
    deck = genanki.Deck(gen_id(), f"{QUANT} {deck_name}")
    for note in reply:
        note = create_note(model, note)
        deck.add_note(note)
    genanki.Package(deck).write_to_file("output.apkg")


main()
