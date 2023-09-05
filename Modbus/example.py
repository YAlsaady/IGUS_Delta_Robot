from igus_modbus import Robot

# Create a Delta Robot instance with the IP address '192.168.1.11'
delta_robot = Robot('192.168.3.11')

# Perform actions with the Delta Robot
delta_robot.enable()
delta_robot.reference()
delta_robot.set_position_endeffector(0, 0, 250)
delta_robot.set_velocity(120)
delta_robot.move_endeffector_absolute()
