from src.igus_modbus import Robot
import time

# Create a Delta Robot instance with the IP address '192.168.1.11'
def main():
    delta_robot = Robot("192.168.3.11")
    wait = True

# Perform actions with the Delta Robot
    delta_robot.enable()
    delta_robot.reference()

    delta_robot.set_velocity(500)
    delta_robot.set_position_endeffector(-200, -200, 150)
    delta_robot.move_endeffector(wait)

    delta_robot.set_position_endeffector(200, -200, 150)
    delta_robot.move_endeffector(wait)

    delta_robot.set_position_endeffector(200, 200, 150)
    delta_robot.move_endeffector(wait)

    delta_robot.set_position_endeffector(-200, 200, 150)
    delta_robot.move_endeffector(wait)
