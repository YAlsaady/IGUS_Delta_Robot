from gripper import Gripper
from igus_modbus import Robot

# gripper = Gripper()
delta = Robot("192.168.3.11")

while True:
    open = delta.client.read_input_registers(54)[0]
    orient = delta.client.read_input_registers(55)[0]
    print(open, orient)
