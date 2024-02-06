"""
Description:
    Main script for continuous control of the gripper using Modbus.

    This script initializes a Gripper object and continuously calls its modbus() method as long as the gripper is connected.
    If the gripper gets disconnected, a new Gripper object is created to reestablish the connection.
"""
from src.gripper import Gripper

if __name__ == "__main__":
    gripper = Gripper()
    while True:
        if gripper.is_connected:
            gripper.modbus()
        else:
            gripper = Gripper()
