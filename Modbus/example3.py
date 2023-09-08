from igus_modbus import Robot
from time import sleep


delta_robot = Robot("192.168.3.11")

delta_robot.enable()
delta_robot.reference()

delta_robot.controll_programs("start")
sleep(3)
delta_robot.controll_programs("stop")
# delta_robot.client.write_single_register(180,0xFFFF)
# delta_robot.client.write_single_register(187,0xFFFF)
# delta_robot.set_position_endeffector(0, 0, 150)
# delta_robot.move_endeffector()
# delta_robot.set_velocity(2000)
# delta_robot.move_circular(100, step=40)
