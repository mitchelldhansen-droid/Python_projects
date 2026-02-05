import json

from save_game import load_game
from states import STATE_MAP, Game, GameStartState


def game_start():
    print("Welcome to the game!")
    print("What would you like to do?")
    print("1. Start a new game")
    print("2. Load a saved game")
    choice = input("Enter your choice: ")
    if choice == "1":
        return None, "GAME_START"
    elif choice == "2":
        try:
            character, current_state = load_game()
            return character, current_state
        except FileNotFoundError:
            print("No save file found! Starting a new game...")
            current_state = "GAME_START"
            character = None
            return character, current_state
        except json.JSONDecodeError:
            print("Save file corrupted! Starting a new game...")
            return None, "GAME_START"
    else:
        print("Invalid choice. Please try again.")
        return game_start()


# ----------------------------------------------------------------------------------


if __name__ == "__main__":
    game = Game()
    character, state_string = game_start()

    if character:  # Loaded a save
        game.character = character
        current_state = STATE_MAP[state_string]()
    else:  # New game
        current_state = GameStartState()

    while current_state:
        current_state.enter(game)
        next_state = current_state.update(game)
        current_state.exit(game)
        current_state = next_state


# Commenting Save file out so it doesn't resave every time its run
# with open("save.json", "w") as file:
#     json.dump(character, file)

# print("Character saved!")
