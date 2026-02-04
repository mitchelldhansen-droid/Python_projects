import json

from player import Character


def save_game(character, current_state, filename="savegame.json"):
    # Bundle everything into one dictionary
    data = {"character": character.to_dict(), "current_state": current_state}

    # Open file for writing ("w" mode), write JSON
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)  # indent=2 makes it human-readable

    print("Game saved!")


def load_game(filename="savegame.json"):
    with open(filename, "r") as f:
        data = json.load(f)

    character = Character.from_dict(data["character"])
    current_state = data["current_state"]

    print("Game Loaded!")
    return character, current_state
