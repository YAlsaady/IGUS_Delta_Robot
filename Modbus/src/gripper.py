"""
Gripper Module
==============

Author: 
    Yaman Alsaady

Description:
    This module provides a Python interface for controlling a gripper device through serial communication.

Classes:
    - Gripper: Represents the gripper and provides methods for controlling its opening and orientation.

Usage:
    To use this module, create an instance of the 'Gripper' class with the appropriate serial port and settings.
"""

import serial
from src.igus_modbus import Robot
from time import time


class Gripper:
    is_connected: bool = False
    orientation = 0
    opening = 0
    last_control_time = 0

    def __init__(
        self,
        port: str = "/dev/ttyUSB0",
        baudrate: int = 115200,
        timeout: int = 1,
        movement_time: float = 1,
    ):
        """
        Initialize the Gripper instance.

        :param port: The serial port for communication (default is "/dev/ttyUSB0").
        :type port: str
        :param baudrate: The baud rate for serial communication (default is 115200).
        :type baudrate: int
        :param timeout: The timeout for serial communication (default is 1 second).
        :type timeout: int
        :param movement_time: The maximum movement time in seconds (default is 1 second).
        :type movement_time: float
        """
        try:
            self.ser = serial.Serial(port, baudrate, timeout=timeout)
            self.orientation = 90
            self.opening = 100
            self.open_min = 90
            self.open_max = 180
            self.orient_min = 30
            self.orient_max = 150
            self.table_hight = 0
            self.is_connected = self.ser.is_open
            self.delta = Robot("192.168.3.11")
            if self.delta.is_connected:
                self.delta.set_globale_signal(7, False)
            self.movement_time = movement_time
            self.table_movement_time = 0
            self.last_control_time = time()
        except:
            pass

    def controll(
        self, opening: int, orientation: int = None, table_hight: int = 0
    ) -> bool:
        """
        Control the gripper's opening and orientation.

        This method allows you to control the gripper's opening (0 to 100 percent) and, optionally, its orientation in degrees.

        :param opening: The desired gripper opening in percent (0 to 100).
        :type opening: int
        :param orientation: The desired gripper orientation in degrees (optional).
        :type orientation: int or None
        :return: True if the operation was successful, False otherwise.
        :rtype: bool
        """
        if not self.is_connected:
            return
        if not (0 <= opening <= 100):
            return False  # Opening value out of range
        if orientation is not None and not (0 <= orientation <= 180):
            return False  # Orientation value out of range

        if (
            self.opening == opening
            and self.orientation == orientation
            and self.table_hight == table_hight
        ):
            return True

        if orientation is None:
            orientation = self.orientation

        if (self.opening == opening) ^ (self.orientation == orientation):
            self.last_control_time = time()
        else:
            self.last_control_time = time() + self.movement_time

        self.opening = opening
        self.orientation = orientation
        table_hight = int(table_hight)
        self.table_hight = table_hight
        opening = int((opening * (self.open_max - self.open_min) / 100) + self.open_min)
        orientation = 180 - int(
            (orientation * (self.orient_max - self.orient_min) / 180) + self.orient_min
        )
        if table_hight == 2:
            table_hight = -1
        pos = f"{opening} {orientation} {table_hight}\n"
        print(pos)
        self.ser.write(pos.encode())
        return True

    def is_moving(self) -> bool:
        """
        Check if the gripper is still moving after the last control operation.

        This method calculates the time since the last control operation and compares it with the maximum movement time.
        If the time since the last control operation is less than the maximum movement time, it returns True,
        indicating that the gripper is still moving. Otherwise, it returns False.

        Additionally, if the delta robot is connected, it sets a global signal to indicate the gripper's movement state.

        :return: True if the gripper is still moving, False otherwise.
        :rtype: bool
        """
        time_since_last_control = time() - self.last_control_time
        state = time_since_last_control < self.movement_time
        if self.delta.is_connected:
            self.delta.set_globale_signal(7, state)
        return state

    def is_table_moving(self) -> bool:
        if self.table_movement_time > time():
            return True
        if self.table_hight:
            print(self.table_movement_time)
            print(time())
            self.controll(self.opening, self.orientation, 0)
            self.delta.set_number_variables(13, 0)
            self.delta.set_number_variables(14, 0)
        return False

    def open(self) -> bool:
        """
        Open the gripper fully.

        This method sets the gripper opening to 0 percent.

        :return: True if the operation was successful, False otherwise.
        :rtype: bool
        """
        if not self.is_connected:
            return
        return self.controll(0)

    def close(self) -> bool:
        """
        Close the gripper fully.

        This method sets the gripper opening to 100 percent.

        :return: True if the operation was successful, False otherwise.
        :rtype: bool
        """
        if not self.is_connected:
            return
        return self.controll(100)

    def rotate(self, orientation: int) -> bool:
        """
        Rotate the gripper to a specific orientation.

        This method sets the gripper orientation to the specified degree value.

        :param orientation: The desired gripper orientation in degrees.
        :type orientation: int
        :return: True if the operation was successful, False otherwise.
        :rtype: bool
        """
        if not self.is_connected:
            return
        if not (0 <= orientation <= 180):
            return False  # Orientation value out of range

        self.controll(self.opening, self.orientation)
        return True

    def modbus(
        self,
        signal: int = 6,
        table_hight: int = 13,
        table_movement_time: int = 14,
        opening: int = 15,
        orientation: int = 16,
    ):
        """
        Control the gripper using Modbus signals and variables.

        :param signal: The Modbus signal number to enable/disable gripper control.
                       Default is 6.
        :type signal: int
        :param var1: The Modbus variable number for reading the gripper opening.
                     Default is 15.
        :type var1: int
        :param var2: The Modbus variable number for reading the gripper orientation.
                     Default is 16.
        :type var2: int
        :return: True if the gripper control was successful, False otherwise.
        :rtype: bool
        """
        if not self.is_connected:
            return False
        if not self.delta.is_connected:
            self.delta = Robot("192.168.3.11")
        if not self.delta.is_connected:
            return False
        if not self.delta.get_globale_signal(signal):
            return False

        opening = self.delta.get_writable_number_variable(opening)
        orientation = self.delta.get_writable_number_variable(orientation)
        table_hight = int(self.delta.get_writable_number_variable(table_hight))
        if self.delta.get_writable_number_variable(table_movement_time):
            self.table_movement_time = self.delta.get_writable_number_variable(
                table_movement_time
            ) / 1000
            self.table_movement_time = self.table_movement_time+time()
        return self.controll(opening, orientation, table_hight)
