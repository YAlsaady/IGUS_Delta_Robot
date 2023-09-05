"""
igus_modbus Module
==================

This module provides a Python interface for controlling a Delta Robot (from igus) using Modbus TCP communication.

Classes:
    - Robot: Represents the Robot and provides methods for controlling it.

Usage:
    To use this module, create an instance of the 'Robot' class with the IP address and the port of the Robot as a parameter.

Example:
    from igus_modbus import Robot
    
    # Create a Delta Robot instance with the IP address '192.168.1.11'
    delta_robot = Robot('192.168.3.11')
    
    # Perform actions with the Delta Robot
    delta_robot.enable()
    delta_robot.reference()
    delta_robot.set_position_endeffector(0, 0, 250)
    delta_robot.set_velocity(120)
    delta_robot.move_endeffector_absolute()

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
        if not self.is_enabled():
            self.client.write_single_coil(53, False)
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
        if not self.is_referenced():
            self.client.write_single_coil(60, False)
            self.client.write_single_coil(60, True)

    def is_enabled(self):
        """
        Check if the Robot is enabled.

        This method checks the state of the Robot's motors by reading coil 53.

        :return: True if the motors are enabled, False otherwise.
        :rtype: bool
        """
        return self.client.read_coils((53))

    def is_referenced(self):
        """
        Check if the Robot is referenced.

        This method checks if the Robot has been referenced by reading coil 60.

        :return: True if the Robot is referenced, False otherwise.
        :rtype: bool
        """
        return self.client.read_coils((60))

    def move_endeffector_absolute(self):
        """
        Move the endeffector to the target position.

        This method moves the endeffector to the specified Cartesian position by writing a rising edge to the coil 100.
        It checks if the robot is enabled and referenced before moving.
        To specify the position, use the method set_position_endeffector(x, y, z).

        :return: True if successful, False if out of range is set.
        :rtype: bool
        """
        print(self.client.read_coils(53))
        print(self.client.read_coils(60))
        self.client.write_single_coil(100, False)
        self.client.write_single_coil(100, True)
        if self.client.read_coils(41):
            return False
        return True

    def set_position_endeffector(self, x_val, y_val, z_val):
        """
        Set the target position of the endeffector

        This method sets the target position of the endeffector in millimeters.
        It converts the input values to the appropriate format and writes them to registers 130-135.

        The position can be absolute or relative to the the base or to itself.
        To make the robot move, use the one of the folling methods
        * move_endeffector_absolute()
        * move_endeffector_relative_tool()
        * move_endeffector_relative_base()

        :param x_val: The target X position in millimeters.
        :type x_val: float
        :param y_val: The target Y position in millimeters.
        :type y_val: float
        :param z_val: The target Z position in millimeters.
        :type z_val: float
        :return: None
        """
        x_val *= 100
        y_val *= 100
        z_val *= 100
        self.client.write_single_register(130, (x_val & 0x0000FFFF))
        self.client.write_single_register(131, (x_val >> 16) & 0x0000FFFF)
        self.client.write_single_register(132, (y_val & 0x0000FFFF))
        self.client.write_single_register(133, (y_val >> 16) & 0x0000FFFF)
        self.client.write_single_register(134, (z_val & 0x0000FFFF))
        self.client.write_single_register(135, (z_val >> 16) & 0x0000FFFF)

    def set_velocity(self, velocity):
        """
        Set the velocity of the Robot.

        This method sets the velocity of the robot in millimeters per second.
        For cartesian motions the value is set as a multiple of 1mm/s,
        for joint motions it is a multiple of 1% (relative to the maximum velocity)
        The actual motion speed also depends on the global override value (holding register 187).

        :param velocity: The desired velocity in millimeters per second (or in percent).
        :type velocity: float
        :return: None
        """
        self.client.write_single_register(180, velocity * 10)
