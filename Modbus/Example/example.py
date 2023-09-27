from src.igus_modbus import Robot
from src.gripper import Gripper
import time

# Create a Delta Robot instance with the IP address '192.168.1.11'
def main():
    delta_robot = Robot("192.168.3.11")
    while not delta_robot.is_connected:
        delta_robot = Robot("192.168.3.11")
        print(delta_robot.is_connected)
    gripper = Gripper()
    print("X")

# Perform actions with the Delta Robot
    delta_robot.enable()
    delta_robot.reference()

    delta_robot.set_velocity(500)
    gripper.controll(50, 90)

    delta_robot.set_position_endeffector(0, 0, 250)
    delta_robot.move_endeffector()
    time.sleep(2)
    print("X")
    gripper.open()

    delta_robot.set_position_endeffector(0, 0, -120)
    delta_robot.move_endeffector(relative = "base")
    time.sleep(2)
    gripper.close()
    time.sleep(2)

    delta_robot.set_position_endeffector(0, 0, 120)
    delta_robot.move_endeffector(relative = "base")
    delta_robot.set_position_endeffector(200, 200, 0)
    delta_robot.move_endeffector(relative = "base")
    delta_robot.set_position_endeffector(0, 0, -130)
    delta_robot.move_endeffector(relative = "base")
    time.sleep(2)
    gripper.rotate(180)
    time.sleep(2)
    gripper.open()
    time.sleep(2)

    gripper.rotate(90)
    delta_robot.set_position_endeffector(0, 0, 100)
    delta_robot.move_endeffector(relative = "base")
    delta_robot.set_position_endeffector(0, 0, 250)
    delta_robot.move_endeffector()
