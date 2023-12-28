"""
Gripper Module
==============

This module provides a Python interface for controlling a gripper device through serial communication.

Classes:
    - Gripper: Represents the gripper and provides methods for controlling its opening and orientation.

Usage:
    To use this module, create an instance of the 'Gripper' class with the appropriate serial port and settings.
"""

import serial
from src.igus_modbus import Robot


class Gripper:
    is_connected: bool = False
    orientation = 0
    opening = 0

    def __init__(
        self, port: str = "/dev/ttyUSB0", baudrate: int = 115200, timeout: int = 1
    ):
        """
        Initialize the Gripper instance.

        :param port: The serial port for communication (default is "/dev/ttyUSB0").
        :type port: str
        :param baudrate: The baud rate for serial communication (default is 9600).
        :type baudrate: int
        :param timeout: The timeout for serial communication (default is 1 second).
        :type timeout: int or float
        """
        try:
            self.ser = serial.Serial(port, baudrate, timeout=timeout)
            self.orientation = 90
            self.opening = 100
            self.is_connected = self.ser.is_open
            self.delta = Robot("192.168.3.11")
        except:
            pass

    def controll(self, opening: int, orientation: int = None) -> bool:
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

        self.opening = opening
        if orientation is not None:
            self.orientation = orientation
        pos = f"{self.opening} {self.orientation}\n"
        self.ser.write(pos.encode())
        # sleep(0.05)
        return True

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

        self.orientation = orientation
        pos = f"{self.opening} {self.orientation}\n"
        self.ser.write(pos.encode())
        return True

    def modbus(self, signal: int = 6, var1: int = 15, var2: int = 16):
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
        opening = self.delta.get_writable_number_variable(var1)
        orientation = self.delta.get_writable_number_variable(var2)
        return self.controll(opening, orientation)
