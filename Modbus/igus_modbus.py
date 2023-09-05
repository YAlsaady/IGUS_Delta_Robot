"""
igus_modbus Module
==================

This module provides a Python interface for controlling a Delta Robot (from igus) using Modbus TCP communication.

Classes:
    - Robot: Represents the Robot and provides methods for controlling it.

Usage:
    To use this module, create an instance of the 'Robot' class with the IP address and the port of the Robot as a parameter.

"""

from pyModbusTCP.client import ModbusClient


class Robot:
    def __init__(self, address, port=502):
        """
        Initialize a Robot instance and establish the communication

        :param address: The IP address of the Robot.
        :type address: str
        :param port: The port for Modbus TCP communication (default is 502).
        :type port: int
        """
        self.address = address
        self.client = ModbusClient(host=address, port=port)

    def __del__(self):
        """
        Close current TCP connection.

        :return: None
        """
        self.client.close()

    def enable(self):
        """
        Enable the motors of the Robot.

        This method enables the motors of the robot by writing 1 the coil 53.

        :return: None
        """
        self.client.write_single_coil(53, True)

    def disable(self):
        """
        Disable the motors of the Robot.

        This method disables the motors of the robot by writing 0 to the coil 53.

        :return: None
        """
        self.client.write_single_coil(53, False)

    def reference(self):
        """
        Reference the Robot.

        This method references the robot by writing a rising edge to the coil 60.

        :return: None
        """
        self.client.write_single_coil(60, False)
        self.client.write_single_coil(60, True)
