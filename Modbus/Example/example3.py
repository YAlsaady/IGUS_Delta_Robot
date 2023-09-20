from igus_modbus import Robot
from time import sleep


delta = Robot("192.168.3.11")

if delta.is_connected:
    delta.enable()
    delta.reference()
    delta.set_override_velocity(50)

    # delta.print_list_of_programs()
    list = delta.get_list_of_porgrams()
    delta.set_program_name(list[2])

    delta.controll_programs("stop")
    delta.set_position_variable(number=1,movement="cartesian",x=200,y=100,z=150)
    # delta_robot.set_position_variable(number=1,movement="axes",a1=30,a2=30,a3=30,conversion=1)
    delta.set_globale_signal(1,False)
    delta.set_digital_output(2,True)
    # for i in range(64):
    print(delta.get_kinematics_error())
    print(delta.get_robot_errors())
    for i in range(16):
        print(i,delta.get_readable_number_variable(i+1))
else:
    print("No Connection")
