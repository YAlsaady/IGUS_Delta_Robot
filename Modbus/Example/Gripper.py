from src.igus_modbus import Robot

def main():
    delta = Robot("192.168.3.11")

    if delta.is_connected:
        delta.enable()
        delta.reference()

        delta.set_override_velocity(50)

        # set_and_move(
        #     val_1,
        #     val_2,
        #     val_3,
        #     movement = "cartesian",
        #     relative = None,
        #     wait = True,
        #     velocity = None
        # ) -> None

        # def control_gripper(opening, orientation, signal = 6)

        delta.set_and_move(0 , 0, 150)
        delta.control_gripper(100,90)
        delta.set_and_move(0 , 0, 250)
        delta.control_gripper(0,90)
        delta.set_and_move(0 , 0, 150)
        delta.control_gripper(0,180)
        delta.set_and_move(0 , 0, 250)
        delta.control_gripper(100,180)
        delta.set_and_move(0 , 0, 150)
    else:
        print("No Connection")
