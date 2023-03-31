import genanki


def create_model(id):
    """Cria e retorna o modelo da nota."""

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


def create_note(model, card):
    """Cria e retorna a nota."""

    note = genanki.Note(model=model, fields=card)
    return note


def create_deck(id, name, size):
    """Cria e retorna o deck."""

    deck_name = f"{size} {name}"
    deck = genanki.Deck(id, deck_name)
    return deck


def create_file(deck):
    return genanki.Package(deck).write_to_file("output.apkg")
