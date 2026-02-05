from main import campsite_menu, character, boss_intro, glade_path, path_choice, forest_path
from player import create_character
from combat import bandit_leader_combat, boss_fight, wolf_ambush, pixie_encounter
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

class PixieEncounterState(State):
    def update(self,game):
        result = pixie_encounter(game.character)
        if result == "died":
            return GameEndingState()
        else:
            offer_save(game.character, "PATH_CHOICE")
            return PathChoiceState()

class PathChoiceState(State):
    def update(self, game):
        result = path_choice(game.character)
        if result == "glade":
            return GladePathState()
        else:
            return ForestPathState()

class GladePathState(State):
    def update(self, game):
        result = glade_path(game.character)
        if result == "died":
            return GameEndingState()
        else:
            offer_save(game.character, "BANDIT_COMBAT")
            return BanditCombatState()

class ForestPathState(State):
    def update(self, game):
        forest_path(game.character)
        offer_save(game.character, "BANDIT_COMBAT")
        return BanditCombatState()

class BanditCombatState(State):
    def update(self,game):
        result = bandit_leader_combat(game.character)
        if result == "died":
            return GameEndingState()
        else:
            return GameVictoryState()


class GameEndingState(State):
    def update(self, game):
