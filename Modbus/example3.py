from igus_modbus import Robot
import time


delta_robot = Robot("192.168.3.11")

delta_robot.enable()
delta_robot.reference()

delta_robot.set_and_move(0, 0, 150, velocity=500)
