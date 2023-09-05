from igus_modbus import Robot
import time

# Create a Delta Robot instance with the IP address '192.168.1.11'
delta_robot = Robot("192.168.3.11")
dt = 0.5

# Perform actions with the Delta Robot
delta_robot.reference()
delta_robot.enable()

delta_robot.set_velocity(2000)
delta_robot.set_position_endeffector(-200, -200, 150)
delta_robot.move_endeffector_absolute()
time.sleep(dt)

delta_robot.set_position_endeffector(200, -200, 150)
delta_robot.move_endeffector_absolute()
time.sleep(dt)

delta_robot.set_position_endeffector(200, 200, 150)
delta_robot.move_endeffector_absolute()
time.sleep(dt)

delta_robot.set_position_endeffector(-200, 200, 150)
delta_robot.move_endeffector_absolute()
time.sleep(dt)
