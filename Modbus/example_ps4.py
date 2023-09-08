from igus_modbus import Robot
from time import sleep
from pyPS4Controller.controller import Controller

delta_robot = Robot("192.168.3.11")

delta_robot.enable()
delta_robot.reference()

class MyController(Controller):
    def __init__(self, **kwargs):
        Controller.__init__(self, **kwargs)
    def on_L3_up(self,value):
        delta_robot.set_and_move(1,0,0, relative="base", velocity=500)
        return value
    def on_L3_down(self,value):
        delta_robot.set_and_move(-1,0,0, relative="base", velocity=500)
        return value
    def on_L3_right(self, value):
        delta_robot.set_and_move(0,1,0, relative="base", velocity=500)
        return value
    def on_L3_left(self,value):
        delta_robot.set_and_move(0,-1,0, relative="base", velocity=500)
        return value
controller = MyController(interface="/dev/input/js0", connecting_using_ds4drv=False)
controller.listen()
