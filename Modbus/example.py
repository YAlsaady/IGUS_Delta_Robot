"""
Description:
    Main function to select and run different example modules.

    This script prompts the user to choose from three example modules: Move, Gripper, and Control_programs.
    After the user selects a module by entering a number, the corresponding main function of that module is executed.
    If the user enters an invalid number, a message indicating that the command is not recognized is printed.
"""
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
