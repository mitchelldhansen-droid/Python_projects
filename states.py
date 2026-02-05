from main import campsite_menu, character, boss_intro
from player import create_character
from combat import boss_fight, wolf_ambush, pixie_encounter
from save_game import offer_save

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

class CampsiteMenuState(State):
    def update(self, game):
        result = campsite_menu(game.character)
        if result == "died":
            return GameEndingState()
        else:
            offer_save(game.character,"CAMPSITE_MENU")
            return BossIntroState()

class BossIntroState(State):
    def update(self,game):
        boss_intro()
        return BossFightState()

class BossFightState(State):
    def update(self,game):
        result = boss_fight(game.character)
        if result == "died":
            return GameEndingState()
        else:
            offer_save(game.character, "PIXIE_ENCOUNTER")
            return PixieEncounterState()

class GameEndingState(State):
    def update(self, game):
