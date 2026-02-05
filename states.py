from main import campsite_menu, character
from player import create_character
from combat import wolf_ambush

class State:
    def enter (self, game):
        pass

    def update (self, game):
        raise NotImplementedError

    def exit (self, game):
        pass

class Game:
    def __init__(self):
        self.character = None
        self.running = True

class GameStartState(State):
    def update(self, game):
        game.character = create_character()
        game.character.display()
        return WolfCombatState()

class WolfCombatState(State):
    def update(self, game):
        result = wolf_ambush(game.character)
        if result == "died":
            return GameEndingState()
        else:
            return CampsiteMenuState()

class GameEndingState(State):
    def update(self, game):

class CampsiteMenuState(State):
    def update(self, game):
        result = campsite_menu()
