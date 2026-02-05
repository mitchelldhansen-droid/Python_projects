from combat import bandit_leader_combat, boss_fight, pixie_encounter, wolf_ambush
from player import create_character
from save_game import offer_save
from transitions import (
    boss_intro,
    campsite_menu,
    forest_path,
    glade_path,
    path_choice,
)
from utils import game_over


class State:
    def enter(self, game):
        pass

    def update(self, game):
        raise NotImplementedError

    def exit(self, game):
        pass


class Game:
    def __init__(self):
        self.character: object = None
        self.running: bool = True


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
            offer_save(game.character, "CAMPSITE_MENU")
            return BossIntroState()


class BossIntroState(State):
    def update(self, game):
        boss_intro()
        return BossFightState()


class BossFightState(State):
    def update(self, game):
        result = boss_fight(game.character)
        if result == "died":
            return GameEndingState()
        else:
            offer_save(game.character, "PIXIE_ENCOUNTER")
            return PixieEncounterState()


class PixieEncounterState(State):
    def update(self, game):
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
    def update(self, game):
        result = bandit_leader_combat(game.character)
        if result == "died":
            return GameEndingState()
        else:
            return GameVictoryState()


class GameVictoryState(State):
    def update(self, game):
        print("\n" + "=" * 50)
        print("Congratulations! You've completed the adventure!")
        if game.character.path_taken == "glade":
            print("\nBattered but powerful, you emerge from the wilderness alone.")
            print("The trials have made you stronger than you ever imagined.")
        elif game.character.path_taken == "forest" and game.character.has_companion:
            print("\nYou and your ally share a moment of triumph.")
            print("'Until next time, friend,' they say, clasping your hand.")
        elif game.character.path_taken == "forest":
            print("\nYou made it through, though you walk alone.")
        print(f"\nThanks for playing, {game.character.name}!")
        print("=" * 50)
        return None


class GameEndingState(State):
    def update(self, game):
        result = game_over(game.character)
        if result == "restart":
            return GameStartState()
        else:
            return None


# Map save file state strings to state classes
STATE_MAP = {
    "GAME_START": GameStartState,
    "CAMPSITE_MENU": CampsiteMenuState,
    "PIXIE_ENCOUNTER": PixieEncounterState,
    "PATH_CHOICE": PathChoiceState,
    "BANDIT_COMBAT": BanditCombatState,
}
