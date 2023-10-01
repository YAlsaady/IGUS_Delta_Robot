import GUI.gui as gui
from Example import example3 as example
from src.igus_modbus import Robot

if __name__ == "__main__":
    # method_list = [method for method in dir(Robot) if method.startswith('__') is False]
    # for i in method_list:
    #     print(i,"()")
    # example.main()
    gui.main()
