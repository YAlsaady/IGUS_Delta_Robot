from src.gripper import Gripper

if __name__ == "__main__":
    gripper = Gripper()
    while True:
        if gripper.is_connected:
            gripper.modbus()
