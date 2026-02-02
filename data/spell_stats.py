CLASS_SPELLS = {
    "Warrior": {
        "battle_cry": {
            "name": "Battle Cry",
            "description": "+10 on your next attack",
            "effect": "buff_attack",
            "power": 10,
            "slots_required": 1,
        },
        "second_wind": {
            "name": "Second Wind",
            "description": "Heal 15 HP",
            "effect": "heal",
            "power": 15,
            "slots_required": 1,
        },
    },
    "Mage": {
        "fireball": {
            "name": "Fireball",
            "description": "Deal 25 damage",
            "effect": "damage",
            "power": 25,
            "slots_required": 1,
        },
        "arcane_shield": {
            "name": "Arcane Shield",
            "description": "Block 20 damage",
            "effect": "shield",
            "power": 20,
            "slots_required": 1,
        },
        "lightning_bolt": {
            "name": "Lightning Bolt",
            "description": "Deal 35 damage",
            "effect": "damage",
            "power": 35,
            "slots_required": 2,
        },
    },
    "Rogue": {
        "shadow_step": {
            "name": "Shadow Step",
            "description": "Dodge next attack",
            "effect": "dodge_next",
            "power": 1,
            "slots_required": 1,
        },
        "poison_blade": {
            "name": "Poison Blade",
            "description": "+8 to next attack",
            "effect": "buff_attack",
            "power": 8,
            "slots_required": 1,
        },
    },
    "Paladin": {
        "lay_on_hands": {
            "name": "Lay on Hands",
            "description": "Heal 30 HP",
            "effect": "heal",
            "power": 30,
            "slots_required": 2,
        },
        "smite": {
            "name": "Smite",
            "description": "+15 damage to next attack",
            "effect": "buff_attack",
            "power": 15,
            "slots_required": 1,
        },
    },
}
BASE_SPELL_SLOTS = {"Warrior": 2, "Rogue": 3, "Paladin": 4, "Mage": 5}
