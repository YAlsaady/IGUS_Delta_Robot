from igus_modbus import Robot
import time
from math import sin, cos, radians
from numpy import arange


# delta_robot = Robot("192.168.3.11")
#
# delta_robot.enable()
# delta_robot.reference()
#
# print(hex(delta_robot.read_loaded_programmes(32)))
def move_circular(radius, step=1, start_angle=0, stop_angle=360):
    x_val = 0
    y_val = 0
    for angle in arange(start_angle, stop_angle+step, step):
        x = radius * cos(radians(angle)) + x_val
        y = radius * sin(radians(angle)) + y_val
        print(round(x,2), round(y,2))


if __name__ == "__main__":
    move_circular(200,0.5)
# delta_robot.set_position_endeffector(0, 0, 250)
# delta_robot.set_velocity(1500)
# delta_robot.controll_programs("start")
# time.sleep(5)
# delta_robot.controll_programs("stop")
