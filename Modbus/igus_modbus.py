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
from ctypes import c_int32
from math import sin, cos, radians
from numpy import arange


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

    def shutdown(self):
        """
        Reset the Delta Robot.

        This method shut the robot down by writing a rising edge to the coil.

        :return: None
        """
        self.client.write_single_coil(51, False)
        self.client.write_single_coil(51, True)

    def reset(self):
        """
        Reset the Delta Robot.

        This method resets the robot by writing a rising edge to the coil.

        :return: None
        """
        self.client.write_single_coil(52, False)
        self.client.write_single_coil(52, True)

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

    def reference(self, only_once=True):
        """
        Reference the Robot.

        This method references the robot by writing a rising edge to the coil 60.
        If 'only_once' is set to True (default), it will only reference the robot if it's not already referenced.

        :param only_once: If True, the robot will only be referenced if not already referenced,
                         otherwise, it will be referenced each time this method is called (default is True).
        :type only_once: bool
        :return: None
        """
        if not only_once:
            self.client.write_single_coil(60, False)
            self.client.write_single_coil(60, True)
            return
        else:
            if not self.is_referenced():
                self.client.write_single_coil(60, False)
                self.client.write_single_coil(60, True)
            else:
                return

    def is_enabled(self):
        """
        Check if the Robot is enabled.

        This method checks the state of the Robot's motors by reading coil 53.

        :return: True if the motors are enabled, False otherwise.
        :rtype: bool
        """
        return self.client.read_coils(53)[0]

    def is_referenced(self):
        """
        Check if the Robot is referenced.

        This method checks if the Robot has been referenced by reading coil 60.

        :return: True if the Robot is referenced, False otherwise.
        :rtype: bool
        """
        return self.client.read_coils(60)[0]

    def is_moving(self):
        """
        Check if the Robot is moving.

        This method checks the state of the Robot's motion by reading coil 112.

        :return: True if the Robot is currently moving, False otherwise.
        :rtype: bool
        """
        return self.client.read_coils(112)[0]

    def set_zero_torque(self, enable = True):
        self.client.write_single_coil(111, enable)

    def move_endeffector(self, wait=True, relative=None):
        """
        Move the end effector to the target position.

        This method moves the end effector to the specified Cartesian position by controlling the appropriate coil.
        The movement can be relative to different reference frames (base, tool) based on the 'relative' parameter.
        To specify the position, use the method set_position_endeffector(x, y, z).

        :param wait: If True (default), wait until the movement is complete before returning.
        :type wait: bool
        :param relative: Specifies the reference frame for the movement (None for absolute, 'base', or 'tool').
        :type relative: str or None
        :return: True if the movement was successful, False if out of range is set.
        :rtype: bool
        """
        if wait:
            while self.is_moving():
                pass
        if relative == None:
            self.client.write_single_coil(100, False)
            self.client.write_single_coil(100, True)
        if relative == "base":
            self.client.write_single_coil(101, False)
            self.client.write_single_coil(101, True)
        if relative == "tool":
            self.client.write_single_coil(102, False)
            self.client.write_single_coil(102, True)
        return True

    def move_axes(self, wait=True, relative=False):
        """
        Move the end effector to the target position.

        This method moves the end effector to the specified axes position by controlling the appropriate coil.
        The movement can be relative or absolute 'relative' parameter.
        To specify the position, use the method set_position_endeffector(x, y, z).

        :param wait: If True (default), wait until the movement is complete before returning.
        :type wait: bool
        :param relative: If False (default), the movement will be absolute, otherwise will be relative to the current position
        :type relative: bool
        :return: True if the movement was successful, False if out of range is set.
        :rtype: bool
        """
        if wait:
            while self.is_moving():
                pass
        if relative:
            self.client.write_single_coil(104, False)
            self.client.write_single_coil(104, True)
        else:
            self.client.write_single_coil(103, False)
            self.client.write_single_coil(103, True)
        return True

    def set_position_endeffector(self, x_val, y_val, z_val):
        """
        Set the target position of the endeffector

        This method sets the target position of the endeffector in millimeters.
        It converts the input values to the appropriate format and writes them to registers 130-135.

        The position can be absolute or relative to the the base or to itself.
        To make the robot move, use the one of the folling method move_endeffector()

        :param x_val: The target X position in millimeters.
        :type x_val: float
        :param y_val: The target Y position in millimeters.
        :type y_val: float
        :param z_val: The target Z position in millimeters.
        :type z_val: float
        :return: None
        """
        x_val = int(x_val * 100)
        y_val = int(y_val * 100)
        z_val = int(z_val * 100)
        self.client.write_single_register(130, (x_val & 0x0000FFFF))
        self.client.write_single_register(131, (x_val >> 16) & 0x0000FFFF)
        self.client.write_single_register(132, (y_val & 0x0000FFFF))
        self.client.write_single_register(133, (y_val >> 16) & 0x0000FFFF)
        self.client.write_single_register(134, (z_val & 0x0000FFFF))
        self.client.write_single_register(135, (z_val >> 16) & 0x0000FFFF)

    def set_orientation_endeffector(self, a_val, b_val, c_val):
        self.client.write_single_register(130, a_val)
        self.client.write_single_register(132, b_val)
        self.client.write_single_register(134, c_val)

    def set_position_axes(self, a_val, b_val, c_val):
        """
        Set the target position of the endeffector

        This method sets the target position of the axes
        It converts the input values to the appropriate format and writes them to registers 142-154

        The position can be absolute or relative.
        To make the robot move, use the one of the method move_endeffector()

        :param a_val: The target A position in millimeters.
        :type x_val: float
        :param b_val: The target B position in millimeters.
        :type y_val: float
        :param c_val: The target C position in millimeters.
        :type z_val: float
        :return: None
        """
        x_val *= 100
        y_val *= 100
        z_val *= 100
        self.client.write_single_register(142, (a_val & 0x000000000000FFFF))
        self.client.write_single_register(143, (a_val >> 16) & 0x000000000000FFFF)
        self.client.write_single_register(144, (a_val >> 24) & 0x000000000000FFFF)
        self.client.write_single_register(145, (a_val >> 32) & 0x000000000000FFFF)
        self.client.write_single_register(146, (b_val & 0x000000000000FFFF))
        self.client.write_single_register(147, (b_val >> 16) & 0x000000000000FFFF)
        self.client.write_single_register(148, (b_val >> 24) & 0x000000000000FFFF)
        self.client.write_single_register(149, (b_val >> 32) & 0x000000000000FFFF)
        self.client.write_single_register(150, (c_val & 0x000000000000FFFF))
        self.client.write_single_register(151, (c_val >> 16) & 0x000000000000FFFF)
        self.client.write_single_register(152, (c_val >> 16) & 0x000000000000FFFF)
        self.client.write_single_register(153, (c_val >> 24) & 0x000000000000FFFF)
        self.client.write_single_register(154, (c_val >> 32) & 0x000000000000FFFF)

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

    def set_and_move(
        self, x_val, y_val, z_val, relative=None, wait=True, velocity=None
    ):
        self.set_position_endeffector(x_val, y_val, z_val)
        if velocity:
            self.set_velocity(velocity)
        self.move_endeffector(wait=wait, relative=relative)

    def get_cartesian_position(self):
        """
        Get the Cartesian position of the Delta Robot.

        This method reads the X, Y, and Z positions from input registers and returns them in millimeters.

        :return: A tuple (x_pos, y_pos, z_pos) representing the Cartesian position in millimeters.
        :rtype: tuple
        """
        x_pos = self.client.read_input_registers(130)[0]
        x_pos2 = self.client.read_input_registers(131)[0]
        y_pos = self.client.read_input_registers(132)[0]
        y_pos2 = self.client.read_input_registers(133)[0]
        z_pos = self.client.read_input_registers(134)[0]
        z_pos2 = self.client.read_input_registers(135)[0]
        x_pos = c_int32(x_pos | (x_pos2 << 16)).value / 100
        y_pos = c_int32(y_pos | (y_pos2 << 16)).value / 100
        z_pos = c_int32(z_pos | (z_pos2 << 16)).value / 100
        return x_pos, y_pos, z_pos

    def controll_programs(self, action):
        if action == "start":
            self.client.write_single_coil(124, False)
            self.client.write_single_coil(124, True)
            self.client.write_single_coil(122, False)
            self.client.write_single_coil(122, True)
        elif action == "continue":
            self.client.write_single_coil(122, False)
            self.client.write_single_coil(122, True)
        elif action == "pause":
            self.client.write_single_coil(123, False)
            self.client.write_single_coil(123, True)
        elif action == "stop":
            self.client.write_single_coil(124, False)
            self.client.write_single_coil(124, True)

    def read_loaded_program(self):
        read = self.client.read_holding_registers(267, 32)
        return self.read_string(read)

    def move_circular(self, radius, step=0.5, start_angle=0, stop_angle=360):
        while self.is_moving():
            pass
        x_val, y_val, z_val = self.get_cartesian_position()
        for angle in arange(start_angle, stop_angle, step):
            x = radius * cos(radians(angle)) + x_val
            y = radius * sin(radians(angle)) + y_val
            print(round(x,2))
            print(round(y,2))
            self.set_and_move(round(x, 2), round(y, 2), z_val)

    def read_string(self, read):
        string = ""
        for i in read:
            if i:
                string += chr(i & 0x00FF)
                string += chr(i >> 8)
        return string

