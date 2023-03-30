import openai
import genanki
import random
import os

START_RANGE = 1 << 30
STOP_RANGE = 1 << 31

# Put your API key here
openai.api_key = os.getenv("OPENAI_API_KEY")
model_id = "gpt-3.5-turbo"

# Change the quantity of phrases or words you want to generate


def chat_completion(message):
    completion = openai.ChatCompletion.create(
        model=model_id, messages=[{"role": "user", "content": message}]
    )
    content = completion.choices[0].message.content
    return content


def format_reply(content):
    # [ ] todo: trocar o for loop por list comprehension
    try:
        reply = content.split("\n")
        # reply = [v.replace(f"{i+1}) ", "") for i, v in enumerate(reply) if "1)" in v]
        # reply = [v.replace(f"{i+1}. ", "") for i, v in enumerate(reply) if "1." in v]
        # print(reply)
        for i, v in enumerate(reply):
            if "1)" in v:
                reply[i] = v.replace(f"{i+1}) ", "")
            else:
                reply[i] = v.replace(f"{i+1}. ", "")
        card = reply[i].split("|")
        reply[i] = card
        return reply
    except Exception as e:
        print(e)


def create_note(model, card):
    note = genanki.Note(model=model, fields=card)
    return note


def generate_deck_id():
    id = random.randrange(START_RANGE, STOP_RANGE)
    return id


def create_model(deck_id):
    model = genanki.Model(
        deck_id,
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


def create_deck(deck_id, deck_name="Frases Cotidianas em Espanhol", deck_quantity=50):
    deck = genanki.Deck(deck_id, f"{deck_quantity} {deck_name}")
    return deck


def main():
    # Modify the deck name
    # [ ] todo: Mudar o deck_name padrão que create_deck() recebe
    deck_name = input("Nome do Deck: ")
    deck_quantity = int(
        input("Digite a quantidade de Notas que gostaria de gerar (Padrão: 50): ")
    )
    # Customize flashcard content
    message = f"""Faça {deck_quantity} Flashcards com frases cotidianas em espanhol para
    português seguindo essa formatação: [concept] | [answer]."""

    content = chat_completion(message)
    reply = format_reply(content)
    deck_id = generate_deck_id()
    model = create_model(deck_id)
    deck = create_deck(deck_id, deck_name, deck_quantity)
    for note in reply:
        note = create_note(model, note)
        deck.add_note(note)
    genanki.Package(deck).write_to_file("output.apkg")


main()
