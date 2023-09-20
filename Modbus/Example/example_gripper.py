from gripper import Gripper
import time

dt = 2

gripper = Gripper()

gripper.close()
time.sleep(dt)
gripper.open()
time.sleep(dt)
gripper.rotate(180)
time.sleep(dt)
gripper.rotate(90)
time.sleep(dt)
gripper.rotate(0)
time.sleep(dt)
