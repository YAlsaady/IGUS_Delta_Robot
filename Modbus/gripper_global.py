from src.gripper import Gripper

if __name__ == "__main__":
    while True:
        gripper = Gripper()
        if gripper.is_connected:
            gripper.modbus()
