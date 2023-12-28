from src.igus_modbus import Robot

def main():
    delta = Robot("192.168.3.11")

    if delta.is_connected:
        delta.enable()
        delta.reference()
        delta.set_override_velocity(50)

        delta.print_list_of_programs()
        print("select a program\n")

        num = input()
        name = delta.get_list_of_porgrams(num)
        delta.set_program_name(name)
        
        print("select an action:\n 1. start\n 2. stop\n 3. pause\n 4. continue\n")
        action = input()


        delta.controll_programs(action)
    else:
        print("No Connection")
