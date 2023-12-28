from Example import Move,Gripper,Control_programs

if __name__ == "__main__":
    print("Choice an Example to run:")
    print(" 1. Move\n 2. Gripper\n 3. Control_programs")
    print("Enter a number: ")
    choice = input()
    print(choice)
    match choice:
        case "1":
            Move.main()
        case "2":
            Gripper.main()
        case "3":
            Control_programs.main()
        case _:
            print("Command not recognized")
