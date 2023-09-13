from igus_modbus import Robot
from time import sleep


delta_robot = Robot("192.168.3.11")

if delta_robot.is_connected:
    delta_robot.enable()
    delta_robot.reference()
    delta_robot.set_override_velocity(50)

    delta_robot.set_program_name("test_var.xml")
    delta_robot.controll_programs("start")
    delta_robot.set_program_replay_mode("repeat")
    print(delta_robot.get_program_runstate())
    print(delta_robot.get_number_of_current_program())

    delta_robot.set_position_variable(movement="cartesian",x=10,y=10,z=150)
    print(delta_robot.get_writable_position_variable(1))
    delta_robot.set_number_variables(1,100)
    delta_robot.set_number_variables(2,100)

    print(delta_robot.get_kinematics_error())
    print(delta_robot.get_robot_errors())
else:
    print("No Connection")
