import random
from genanki_helper import create_deck, create_model, create_note, create_file
from openai_helper import get_chat_response


START_RANGE = 1 << 30
STOP_RANGE = 1 << 31
DEFAULT_DECK_NAME = "Frases Cotidianas em Espanhol"
DEFAULT_DECK_SIZE = 3


def format_reply(content):
    """Retorna a mensagem da IA formatada

    Args:
        content (str): Mensagem da IA sem formatação.

    Returns:
        str: Mensagem da IA formatada.
    """
    try:
        reply = content.split("\n")
        reply = [
            v.replace(f"{i+1}) ", "").replace(f"{i+1}. ", "").split("|")
            for i, v in enumerate(reply)
        ]
        return reply
    except ValueError as e:
        print(e)


def generate_deck_id():
    """Gera um ID para o Deck"""
    deck_id = random.randrange(START_RANGE, STOP_RANGE)  # nosec
    return deck_id


def get_deck_size():
    """Get from user the deck size, if empty, use default value"""

    while True:
        try:
            deck_size = input(f"Quantidade de Notas (Padrão: {DEFAULT_DECK_SIZE}): ")
            if deck_size == "":
                return DEFAULT_DECK_SIZE
            return int(deck_size)
        except ValueError:
            print("Digite um número válido!")


def get_deck_name():
    """Get from user which name he wants to give to the deck."""

    while True:
        try:
            deck_name = input(f"Deck Name (Default: '{DEFAULT_DECK_NAME}'): ")
            if deck_name == "":
                return DEFAULT_DECK_NAME
            return deck_name
        except ValueError:
            print("Digite um nome válido!")


def main():
    deck_name = get_deck_name()
    deck_size = get_deck_size()

    # Change this if you want to customize flashcard content
    chat_message = (
        f"Crie {deck_size} Flashcards com sentenças em espanhol seguindo essa "
        "formatação: [concept] | [answer]."
    )

    content = get_chat_response(chat_message)
    notes = format_reply(content)
    deck_id = generate_deck_id()
    model = create_model(deck_id)
    deck = create_deck(deck_id, deck_name, deck_size)
    for note in notes:
        note = create_note(model, note)
        deck.add_note(note)
    create_file(deck)


main()
