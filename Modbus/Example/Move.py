from src.igus_modbus import Robot

def main():
    delta = Robot("192.168.3.11")
    wait = True

    if delta.is_connected:
        delta.enable()
        delta.reference()

        delta.set_velocity(500)
        delta.set_position_endeffector(-200, -200, 150)
        delta.move_endeffector(wait)

        delta.set_position_endeffector(200, -200, 150)
        delta.move_endeffector(wait)

        delta.set_position_endeffector(200, 200, 150)
        delta.move_endeffector(wait)

        delta.set_position_endeffector(-200, 200, 150)
        delta.move_endeffector(wait)
    else:
        print("No Connection")
