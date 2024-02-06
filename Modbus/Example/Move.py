"""
Author: 
    Yaman Alsaady

Description:
    This example demonstrates how to move the Delta robot in a rectangular pattern. It begins by establishing a connection to the robot, and if successful, performs some basic movements.
"""
from src.igus_modbus import Robot

def main():
    """
    This function creates an instance of the Robot class, establishes a connection to the robot, and executes a predefined sequence of movements.
    """
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
