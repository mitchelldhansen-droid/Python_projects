from data.spell_stats import CLASS_SPELLS


def display_spell_menu(character):
    spells = character.get_available_spells()
    spell_keys = list(spells.keys())  # ["fireball", "arcane_shield", etc.]

    print("=== SPELLS ===")
    for index, key in enumerate(spell_keys, start=1):
        spell = spells[key]  # get the spell dict
        name = spell["name"]
        cost = spell["slots_required"]

        # Now check if they can cast THIS spell
        if character.can_cast(key):
            print(f"{index}. {name} ({cost} slot)")
        else:
            print(f"{index}. {name} ({cost} slot) [Not enough slots!]")

    return spell_keys


def cast_spell(character, spell_key, target=None):
    spell = CLASS_SPELLS[character.player_class][spell_key]
    if not character.can_cast(spell_key):
        return {"success": False, "message": "Not enough spell slots!"}

    character.use_spell_slots(spell["slots_required"])
    effect = spell["effect"]
    power = spell["power"]

    if effect == "damage":
        if target is None:
            return {"success": False, "message": "No target for damage spell!"}
        target.take_damage(power)
        message = f"{character.name} casts {spell['name']} for {power} damage!"
    elif effect == "heal":
        character.heal(power)
        message = f"{character.name} casts {spell['name']} and heals for {power} HP!"
    elif effect == "buff_attack":
        character.active_buffs["attack_bonus"] = power
        message = (
            f"{character.name} casts {spell['name']}! Next attack +{power} damage."
        )

    elif effect == "shield":
        character.active_buffs["shield"] = power
        message = f"{character.name} casts {spell['name']}! Absorbs {power} damage."

    elif effect == "dodge_next":
        character.active_buffs["dodge"] = True
        message = f"{character.name} casts {spell['name']}! Will dodge next attack."
    else:
        message = f"{character.name} casts {spell['name']}!"
    return {"success": True, "message": message}
