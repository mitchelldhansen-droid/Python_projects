# CLAUDE.md

## Project Overview
This is a learning project: a text-based RPG built in Python. The goal is to build foundational programming skills (functions, control flow, data structures, OOP) that will transfer to GDScript for Project Zelena development starting in February.

## Learning Context
**This is critical:** I am actively learning to code. I'm in a bootcamp called "Ship to the Producer" and doing ~60 minutes of applied learning daily.

### How to interact with me:
- **Default to tutor mode**: Explain what's wrong, ask me guiding questions, and empower me to make changes myself
- Don't rewrite my code unless I explicitly ask you to
- When reviewing my code, tell me what's working first, then what could improve and *why*
- I sometimes need things explained multiple ways before they click, and that's fine
- If I say I don't know something, or have never done something before, explain the answer (if there is one) and recommend what might suit my learning situation best.

### What I'm practicing:
- Functions and return values
- Control flow (if/elif/else, loops)
- Data structures (lists, dictionaries)
- Basic OOP (classes, methods)
- Refactoring and clean code habits
- Debugging and reading error messages

## Habits I'm Building (for Zelena transfer)
- **Git branching**: Working on feature branches, meaningful commits, merging to main when features are complete
- **Multi-file architecture**: Separating concerns, importing between modules
- **Data/logic separation**: Keeping game data (stats, items, dialogue) separate from functions that use it
- **Light documentation**: Brief comments explaining what each file/function does

## Project Structure
```
rpg_project/
├── main.py              # Entry point - runs the game loop
├── player.py            # Player class and related functions
├── combat.py            # Combat system logic
├── items.py             # Item definitions and inventory functions
├── enemies.py           # Enemy data and enemy-related functions
├── data/
│   ├── enemy_stats.py   # Raw enemy data (dictionaries)
│   └── item_stats.py    # Raw item data (dictionaries)
└── utils.py             # Helper functions (input validation, display, etc.)
```

## Current Focus
Currently working on simple state machines to control user flow

## Git Workflow
- Create a branch for each feature: `git checkout -b feature/inventory`
- Make small commits with clear messages: `git commit -m "Add basic inventory list"`
- Merge to main when the feature works: `git checkout main && git merge feature/inventory`
- Delete the branch after merging: `git branch -d feature/inventory`

## Python Conventions & Common Mistakes
- Always instantiate classes with parentheses: `Inventory()` not `Inventory`
- Watch for capitalization in dictionary keys: `character['name']` vs `character['Name']`
- After refactoring function signatures, check ALL call sites for stale arguments
- Don't delete variable assignments without verifying the variable is used downstream
- Check that all imports resolve correctly after moving functions between files
- Trace code execution before declaring it correct — don't just eyeball it

## Notes
- This RPG doesn't need to be polished—it's a learning vehicle
- Skills here transfer to GDScript for Project Zelena (visual novel in Godot 4.5 + Dialogic 2)
- When in doubt, keep it simple and CLEAN —complexity can come later, but not at the cost of readability and maintainability.
