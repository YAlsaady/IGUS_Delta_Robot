from time import sleep
from gripper import Gripper
from igus_modbus import Robot


delta = Robot("192.168.3.11")
gripper = Gripper()
while True:
    if delta.get_globale_signal(6):
        open = delta.get_readable_number_variable(15)
        orient = delta.get_readable_number_variable(16)
        sleep(.3)
        gripper.controll(open, orient)
