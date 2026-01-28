def game_over(character):
    print("GAME OVER" + " " + character.name + "!")
    print("1. Restart")
    print("2. Quit")
    choice = input("Enter your choice: ")
    if choice == "1":
        return "restart"
    elif choice == "2":
        return "quit"
    else:
        print("Invalid choice")
        return game_over(character)
