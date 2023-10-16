from igus_modbus import Robot
from time import sleep


# def main():

while True:
    delta = Robot("192.168.3.11")
    # print(delta.get_kinematics_error())
    print(delta.client.read_coils(20,12))
    # print(delta.client.read_input_registers(400,32))
    # (delta.get_info_message())
    sleep(.1)
