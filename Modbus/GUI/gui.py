"""
Delta Robot Control Application
===============================

Author: 
    Yaman Alsaady

Description:
    - This application provides a graphical user interface (GUI) to control a Delta robot and its gripper.
    - The GUI allows the user to control the robot's movements, adjust speed settings, operate the gripper, and manage robot programs.

Classes:
    - App: Represents the main application window and contains methods for initializing the GUI and running the application.

"""
from time import localtime, strftime
import tkinter as tk
from tkinter import ttk
import os
import webbrowser
import json

from src.igus_modbus import Robot

PATH = os.path.dirname(os.path.abspath(__file__)) + "/"


class App(ttk.Frame):
    fontsize = 20

    # {{{ init
    def __init__(self, _):
        ttk.Frame.__init__(self)

        self.tk.call("source", PATH + "azure.tcl")
        self.tk.call("set_theme", "dark")
        self.delta = Robot("192.168.3.11")
        # Make the app responsive
        for index in [0, 1, 2]:
            self.columnconfigure(index=index, weight=1)
            self.rowconfigure(index=index, weight=1)

        # Create control variables

        self.theme = ["dark", "light"]
        self.steps = [0.5, 1, 2, 4, 6, 8, 10]
        self.steps.reverse()
        self.theme_var = tk.StringVar()
        self.enalbe_var = tk.BooleanVar(value=True)
        self.run_var = tk.BooleanVar(value=False)
        self.sort_var = tk.StringVar()
        self.pos_list = []
        self.zero_torque_var = tk.BooleanVar(value=False)
        self.reset_var = tk.BooleanVar(value=False)
        self.speed_var = tk.IntVar(value=100)
        self.global_speed_var = tk.IntVar(value=100)
        self.gripper_var = tk.IntVar(value=100)
        self.gripper_orient_var = tk.IntVar(value=90)
        self.gripper_enable_var = tk.BooleanVar(value=False)
        self.program_var = tk.IntVar()
        self.locale_program_var = tk.IntVar()
        self.remove_var = tk.StringVar()
        self.update_delay = tk.IntVar(value=1)
        self.step_var = tk.DoubleVar(value=10)
        self.reference_var = tk.BooleanVar(value=False)
        self.gripper_opening = 0
        self.gripper_orientation = 0
        self.last_error = ""
        self.count_error = 0
        self.last_kin_error = ""
        self.count_kin_error = 0
        self.robot_error = "Robot:\n"
        self.kinematic_error = "Kinematic:\n"
        self.about_msg = (
            "User Interface to control the Robot\nPart of Project Work\n\nCreated by:\n\tYaman Alsaady\nSupervised by:\n\tM. Eng. Jeffrey Wermann",
        )
        self.logo_widgets()
        self.setting_widgets()
        self.tabs()

        self.control_widgets()
        self.speed_widgets()
        self.gripper_widgets(self.tab_1, 5, 0)
        self.move_widgets(self.tab_1, 1, 1)
        self.error_widgets()

        self.programs_widgets()
        self.locale_programs_widgets()
        self.load_widgets()

        self.move_widgets(self.tab_3, 0, 0)
        self.gripper_widgets(self.tab_3, 2, 0)
        self.teach_widgets()

        self.delta.set_velocity(2000)
        self.after(self.update_delay.get(), self.update)
        self.update_list()
        self.locale_update_list()

    # }}}

    # {{{ Tabs
    def tabs(self):
        self.tabs = ttk.Notebook(self)
        self.tabs.grid(
            row=0, column=1, padx=(10, 10), pady=(10, 10), sticky="nwewns", rowspan=3
        )
        self.tabs.bind("<<NotebookTabChanged>>", self.update_tabs)

        self.tab_1 = ttk.Frame(self)
        self.tabs.add(self.tab_1, text="Control")
        self.tab_2 = ttk.Frame(self)
        self.tabs.add(self.tab_2, text="Program")
        self.tab_6 = ttk.Frame(self)
        self.tabs.add(self.tab_6, text="Locale Program")
        self.tab_3 = ttk.Frame(self)
        self.tabs.add(self.tab_3, text="Teach and Play")
        self.tab_4 = ttk.Frame(self)
        self.tabs.add(self.tab_4, text="More")

    #  }}}

    # {{{ LOGO
    def logo_widgets(self, img=PATH + "img/hsel_logo_dark.png"):
        self.logo_frame = tk.Frame(self)
        self.logo_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.logo = tk.PhotoImage(file=img)
        self.logo_label = ttk.Label(self.logo_frame, image=self.logo)
        self.logo_label.grid(row=0, column=0, padx=10, pady=10, sticky="ew", rowspan=3)

        self.info_frame = ttk.LabelFrame(self, text="About", padding=(20, 10))
        self.info_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nwewns")

        self.delta_label = ttk.Label(
            self.info_frame,
            text="Delta Robot",
            font=("-size", self.fontsize),
        )
        self.delta_label.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")
        self.about_label = ttk.Label(
            self.info_frame,
            text=self.about_msg[0],
            font=("-size", self.fontsize),
        )
        self.about_label.grid(
            row=1, column=0, padx=5, pady=10, sticky="nsew", columnspan=2
        )
        self.doc_button = ttk.Button(
            self.info_frame,
            text="Documentation",
            command=lambda: webbrowser.open(
                PATH.replace("GUI/", "docs/_build/html/index.html")
            ),
        )
        self.doc_button.grid(row=2, column=0, padx=5, pady=10, sticky="nw")

    # }}}

    # {{{ Setting
    def setting_widgets(self):
        self.setting_frame = ttk.LabelFrame(self, text="Setting", padding=(20, 10))
        self.setting_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nwewns")

        self.connect_button = ttk.Button(
            self.setting_frame, text="Connect", command=lambda: self.connect()
        )
        self.connect_button.grid(row=0, column=0, padx=5, pady=10, sticky="ew")

        self.enable = ttk.Checkbutton(
            self.setting_frame,
            text="Enable",
            style="Toggle.TButton",
            variable=self.enalbe_var,
            command=lambda: self.enable_robot(),
        )
        self.enable.grid(row=0, column=1, padx=5, pady=10, sticky="nsew")

        self.reset = ttk.Button(
            self.setting_frame, text="Reset", command=lambda: self.delta.reset()
        )
        self.reset.grid(row=1, column=1, padx=5, pady=10, sticky="nsew")

        self.reference = ttk.Button(
            self.setting_frame,
            text="Reference",
            command=lambda: (
                self.reference_label.config(text="Reference: Robot is referencing ..."),
                self.reference_var.set(True),
                self.delta.reference(True),
            ),
        )
        self.reference.grid(row=1, column=0, padx=5, pady=10, sticky="nsew")

        self.zero_torque = ttk.Checkbutton(
            self.setting_frame,
            text="Zero Torque",
            style="Toggle.TButton",
            variable=self.zero_torque_var,
            command=lambda: self.delta.set_zero_torque(self.zero_torque_var.get()),
        )
        self.zero_torque.grid(
            row=2, column=0, padx=5, pady=10, sticky="nsew", columnspan=2
        )

        self.theme = ttk.OptionMenu(
            self.setting_frame,
            self.theme_var,
            self.theme[0],
            *self.theme,
            command=lambda _: self.update_theme(),
            direction="above",
        )
        self.theme.grid(row=3, column=0, padx=5, pady=10, sticky="nsew", columnspan=2)

    #  }}}

    # {{{ Control
    def control_widgets(self):
        self.control_frame = ttk.LabelFrame(
            self.tab_1, text="Control", padding=(20, 10)
        )
        self.control_frame.grid(
            row=1, column=0, padx=(20, 10), pady=(20, 10), sticky="nwewns"
        )

        self.connect_label = ttk.Label(
            self.control_frame, text="Connection:", font=("-size", self.fontsize)
        )
        self.connect_label.grid(
            row=1, column=0, padx=5, pady=10, sticky="ew", columnspan=4
        )
        self.reference_label = ttk.Label(
            self.control_frame, text="Reference:", font=("-size", self.fontsize)
        )
        self.reference_label.grid(
            row=2, column=0, padx=5, pady=10, sticky="ew", columnspan=4
        )

    #  }}}

    # {{{ Speed
    def speed_widgets(self):
        self.speed_frame = ttk.LabelFrame(self.tab_1, text="Speed", padding=(20, 20))
        self.speed_frame.grid(row=3, column=0, padx=(20, 20), pady=10, sticky="nwew")

        self.global_speed_scale = ttk.Scale(
            self.speed_frame,
            from_=0,
            to=100,
            length=200,
            variable=self.global_speed_var,
            command=lambda _: (
                self.global_speed_var.set(self.global_speed_scale.get()),
                self.global_speed_label.config(text=int(self.global_speed_var.get())),
                self.delta.set_override_velocity(int(self.global_speed_var.get())),
            ),
        )
        self.global_speed_scale.grid(
            row=0, column=1, padx=(20, 10), pady=(20, 0), sticky="ew"
        )

        self.global_speed_label = ttk.Label(
            self.speed_frame,
            text=int(self.global_speed_var.get()),
            font=("-size", self.fontsize),
        )
        self.global_speed_label.grid(
            row=0, column=2, padx=(20, 10), pady=(20, 0), sticky="ew"
        )

        self.global_speed_title_label = ttk.Label(
            self.speed_frame, text="Globale Speed", font=("-size", self.fontsize)
        )
        self.global_speed_title_label.grid(
            row=0, column=0, padx=(5, 10), pady=(20, 0), sticky="ew"
        )

        self.speed_scale = ttk.Scale(
            self.speed_frame,
            from_=0,
            to=100,
            length=200,
            variable=self.speed_var,
            command=lambda _: (
                self.delta.set_velocity(int(self.speed_scale.get() * 20)),
                self.speed_var.set(self.speed_scale.get()),
                self.speed_label.config(text=int(self.speed_var.get())),
            ),
        )
        self.speed_scale.grid(row=1, column=1, padx=(20, 20), pady=(20, 0), sticky="ew")

        self.speed_label = ttk.Label(
            self.speed_frame,
            text=int(self.speed_var.get()),
            font=("-size", self.fontsize),
        )
        self.speed_label.grid(row=1, column=2, padx=(20, 10), pady=(20, 0), sticky="ew")

        self.speed_title_label = ttk.Label(
            self.speed_frame, text="Speed        ", font=("-size", self.fontsize)
        )
        self.speed_title_label.grid(
            row=1, column=0, padx=(5, 10), pady=(20, 0), sticky="ew"
        )
        self.table_up = ttk.Button(
            self.speed_frame,
            text="Up",
            command=lambda: (
                self.delta.change_table_hight(1,100),
            ),
        )
        self.table_up.grid(row=2, column=0, padx=5, pady=10, sticky="nsew")
        self.table_down = ttk.Button(
            self.speed_frame,
            text="Down",
            command=lambda: (
                self.delta.change_table_hight(2,100),
            ),
        )
        self.table_down.grid(row=2, column=2, padx=5, pady=10, sticky="nsew")
        self.table_title_label = ttk.Label(
            self.speed_frame, text="       Table", font=("-size", self.fontsize)
        )
        self.table_title_label.grid(
            row=2, column=1, padx=(5, 10), pady=(20, 0), sticky="ew"
        )

    #  }}}
    def tabel_widgets(self):
        self.table_frame = ttk.LabelFrame(self.tab_1, text="Table", padding=(20, 20))
        self.table_frame.grid(row=4, column=0, padx=(20, 20), pady=10, sticky="nwew")
        self.table_up = ttk.Button(
            self.table_frame,
            text="Up",
            command=lambda: (
                print("Up")
            ),
        )
        self.table_up.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")
        self.table_down = ttk.Button(
            self.table_frame,
            text="Down",
            command=lambda: (
                print("Down")
            ),
        )
        self.table_down.grid(row=0, column=1, padx=5, pady=10, sticky="nsew")

    # {{{ Gripper
    def gripper_widgets(self, tab_name, row, column):
        self.gripper_frame = ttk.LabelFrame(tab_name, text="Gripper", padding=(20, 20))
        self.gripper_frame.grid(
            row=row, column=column, padx=(20, 20), pady=10, sticky="nwew"
        )

        self.switch = ttk.Checkbutton(
            self.gripper_frame,
            text="Enable Gripper",
            style="Toggle.TButton",
            variable=self.gripper_enable_var,
        )
        self.switch.grid(row=0, column=0, padx=0, pady=0, sticky="nsew", columnspan=3)

        self.gripper_scale = ttk.Scale(
            self.gripper_frame,
            from_=0,
            to=100,
            length=200,
            variable=self.gripper_var,
            command=lambda _: (
                self.gripper_var.set(self.gripper_scale.get()),
                self.gripper_label.config(text=int(self.gripper_var.get())),
            ),
        )
        self.gripper_scale.grid(
            row=1, column=1, padx=(20, 10), pady=(20, 0), sticky="ew"
        )

        self.gripper_label = ttk.Label(
            self.gripper_frame,
            text=int(self.gripper_var.get()),
            font=("-size", self.fontsize),
        )
        self.gripper_label.grid(
            row=1, column=2, padx=(20, 10), pady=(20, 0), sticky="ew"
        )

        self.gripper_title_label = ttk.Label(
            self.gripper_frame, text="Gripper Opening", font=("-size", self.fontsize)
        )
        self.gripper_title_label.grid(
            row=1, column=0, padx=(5, 10), pady=(20, 0), sticky="ew"
        )

        self.gripper_orient_scale = ttk.Scale(
            self.gripper_frame,
            from_=0,
            to=180,
            length=200,
            variable=self.gripper_orient_var,
            command=lambda _: (
                self.gripper_orient_var.set(self.gripper_orient_scale.get()),
                self.gripper_orient_label.config(
                    text=int(self.gripper_orient_var.get())
                ),
            ),
        )
        self.gripper_orient_scale.grid(
            row=2, column=1, padx=(20, 10), pady=(20, 20), sticky="ew"
        )

        self.gripper_orient_label = ttk.Label(
            self.gripper_frame,
            text=int(self.gripper_orient_var.get()),
            font=("-size", self.fontsize),
        )
        self.gripper_orient_label.grid(
            row=2, column=2, padx=(20, 10), pady=(20, 20), sticky="ew"
        )

        self.gripper_orient_title_label = ttk.Label(
            self.gripper_frame,
            text="Gripper Orientation",
            font=("-size", self.fontsize),
        )
        self.gripper_orient_title_label.grid(
            row=2, column=0, padx=(5, 10), pady=(20, 20), sticky="ew"
        )

    # }}}

    # {{{ Move
    def move_widgets(self, tab_name, row, column):
        self.move_paned = ttk.PanedWindow(tab_name)
        self.move_paned.grid(
            row=row,
            column=column,
            padx=(20, 10),
            pady=(20, 10),
            sticky="nwewns",  # , rowspan=3
        )
        self.pane_2 = ttk.Frame(self.move_paned)
        self.move_paned.add(self.pane_2)

        self.notebook = ttk.Notebook(self.pane_2)
        self.notebook.pack(fill="both", expand=True)

        # Tab #1
        self.move_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.move_tab, text="Cartesian")

        self.x_m = ttk.Button(
            self.move_tab,
            text="X-",
            command=lambda: self.delta.set_and_move(
                -1 * self.step_var.get(), 0, 0, relative="base", wait=False
            ),
        )
        self.x_m.grid(row=0, column=0, padx=25, pady=10)

        self.x_p = ttk.Button(
            self.move_tab,
            text="X+",
            command=lambda: self.delta.set_and_move(
                self.step_var.get(), 0, 0, relative="base", wait=False
            ),
        )
        self.x_p.grid(row=0, column=2, padx=25, pady=5)

        self.x_label = ttk.Label(self.move_tab, text="X", font=("-size", self.fontsize))
        self.x_label.grid(row=0, column=1, padx=5, pady=10)

        self.y_m = ttk.Button(
            self.move_tab,
            text="Y-",
            command=lambda: self.delta.set_and_move(
                0, -1 * self.step_var.get(), 0, relative="base", wait=False
            ),
        )
        self.y_m.grid(row=1, column=0, padx=5, pady=10)

        self.y_p = ttk.Button(
            self.move_tab,
            text="Y+",
            command=lambda: self.delta.set_and_move(
                0, self.step_var.get(), 0, relative="base", wait=False
            ),
        )
        self.y_p.grid(row=1, column=2, padx=10, pady=5)

        self.y_label = ttk.Label(self.move_tab, text="Y", font=("-size", self.fontsize))
        self.y_label.grid(row=1, column=1, padx=5, pady=10)

        self.z_m = ttk.Button(
            self.move_tab,
            text="Z-",
            command=lambda: self.delta.set_and_move(
                0, 0, -1 * self.step_var.get(), relative="base", wait=False
            ),
        )
        self.z_m.grid(row=2, column=0, padx=5, pady=10)

        self.z_p = ttk.Button(
            self.move_tab,
            text="Z+",
            command=lambda: self.delta.set_and_move(
                0, 0, self.step_var.get(), relative="base", wait=False
            ),
        )
        self.z_p.grid(row=2, column=2, padx=10, pady=5)

        self.z_label = ttk.Label(self.move_tab, text="Z", font=("-size", self.fontsize))
        self.z_label.grid(row=2, column=1, padx=5, pady=10)

        self.step_label = ttk.Label(
            self.move_tab, text="Stops:", font=("-size", self.fontsize)
        )
        self.step_label.grid(row=3, column=0, padx=5, pady=10)

        self.step = ttk.OptionMenu(
            self.move_tab,
            self.step_var,
            self.steps[0],
            *self.steps,
            direction="below",
        )
        self.step.grid(row=3, column=1, padx=5, pady=10, sticky="ew", columnspan=2)
        self.axes_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.axes_tab, text="Joints")

        self.a1_m = ttk.Button(
            self.axes_tab,
            text="A1-",
            command=lambda: self.delta.set_and_move(
                -1 * self.step_var.get(), 0, 0, relative="base", movement="axes"
            ),
        )
        self.a1_m.grid(row=0, column=0, padx=25, pady=10)

        self.a1_p = ttk.Button(
            self.axes_tab,
            text="A1+",
            command=lambda: self.delta.set_and_move(
                self.step_var.get(), 0, 0, relative="base", movement="axes"
            ),
        )
        self.a1_p.grid(row=0, column=2, padx=25, pady=5)

        self.a1_label = ttk.Label(
            self.axes_tab, text="A1", font=("-size", self.fontsize)
        )
        self.a1_label.grid(row=0, column=1, padx=5, pady=10)

        self.a2_m = ttk.Button(
            self.axes_tab,
            text="A2-",
            command=lambda: self.delta.set_and_move(
                0, -1 * self.step_var.get(), 0, relative="base", movement="axes"
            ),
        )
        self.a2_m.grid(row=1, column=0, padx=5, pady=10)

        self.a2_p = ttk.Button(
            self.axes_tab,
            text="A2+",
            command=lambda: self.delta.set_and_move(
                0, self.step_var.get(), 0, relative="base", movement="axes"
            ),
        )
        self.a2_p.grid(row=1, column=2, padx=10, pady=5)

        self.a2_label = ttk.Label(
            self.axes_tab, text="A2", font=("-size", self.fontsize)
        )
        self.a2_label.grid(row=1, column=1, padx=5, pady=10)

        self.a3_m = ttk.Button(
            self.axes_tab,
            text="A3-",
            command=lambda: self.delta.set_and_move(
                0, 0, -1 * self.step_var.get(), relative="base", movement="axes"
            ),
        )
        self.a3_m.grid(row=2, column=0, padx=5, pady=10)

        self.a3_p = ttk.Button(
            self.axes_tab,
            text="A3+",
            command=lambda: self.delta.set_and_move(
                0, 0, self.step_var.get(), relative="base", movement="axes"
            ),
        )
        self.a3_p.grid(row=2, column=2, padx=10, pady=5)

        self.a3_label = ttk.Label(
            self.axes_tab, text="A3", font=("-size", self.fontsize)
        )
        self.a3_label.grid(row=2, column=1, padx=5, pady=10)

        self.step_label = ttk.Label(
            self.axes_tab, text="Stops:", font=("-size", self.fontsize)
        )
        self.step_label.grid(row=3, column=0, padx=5, pady=10)

        self.step = ttk.OptionMenu(
            self.axes_tab,
            self.step_var,
            self.steps[0],
            *self.steps,
            direction="below",
        )
        self.step.grid(row=3, column=1, padx=5, pady=10, sticky="ew", columnspan=2)

    # }}}

    # {{{ Errors
    def error_widgets(self):
        self.error_frame = ttk.LabelFrame(self.tab_1, text="Error", padding=(20, 10))
        self.error_frame.grid(
            row=3, column=1, padx=(20, 10), pady=(20, 10), sticky="nwewns", rowspan=3
        )
        self.robot_label = ttk.Label(
            self.error_frame, text="Robot:\n\n", font=("-size", self.fontsize)
        )
        self.robot_label.grid(row=0, column=0, padx=5, pady=10, sticky="ew")
        self.kinematic_label = ttk.Label(
            self.error_frame, text="Kinematic:", font=("-size", self.fontsize)
        )
        self.kinematic_label.grid(row=1, column=0, padx=5, pady=10, sticky="ew")

    #  }}}

    # {{{ Programs
    def programs_widgets(self):
        self.programs_frame = ttk.LabelFrame(
            self.tab_2, text="Program execution", padding=(20, 20)
        )
        self.programs_frame.grid(
            row=1, column=0, padx=(20, 10), pady=(20, 10), sticky="nwewns"
        )

        self.play = ttk.Button(
            self.programs_frame,
            text="Start",
            command=lambda: self.delta.controll_programs("start"),
        )
        self.play.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")
        self.stop = ttk.Button(
            self.programs_frame,
            text="Stop",
            command=lambda: self.delta.controll_programs("stop"),
        )
        self.stop.grid(row=0, column=1, padx=5, pady=10, sticky="nsew")
        self.pause = ttk.Button(
            self.programs_frame,
            text="Pause",
            command=lambda: self.delta.controll_programs("pause"),
        )
        self.pause.grid(row=0, column=2, padx=5, pady=10, sticky="nsew")
        self.continue_p = ttk.Button(
            self.programs_frame,
            text="Continue",
            command=lambda: self.delta.controll_programs("continue"),
        )
        self.continue_p.grid(row=0, column=3, padx=5, pady=10, sticky="nsew")

        self.status_p = ttk.Label(
            self.programs_frame, text="Status", font=("-size", self.fontsize)
        )
        self.status_p.grid(row=1, column=0, padx=5, pady=10, columnspan=4, sticky="ew")

        self.loaded_p = ttk.Label(
            self.programs_frame, text="Loaded Program:", font=("-size", self.fontsize)
        )
        self.loaded_p.grid(row=2, column=0, padx=5, pady=10, columnspan=4, sticky="ew")

    # }}}

    # {{{ Locale Programs
    def locale_programs_widgets(self):
        self.locale_load_frame = ttk.LabelFrame(
            self.tab_6, text="Load Programs", padding=(20, 10)
        )
        self.locale_load_frame.grid(
            row=3, column=0, padx=(20, 10), pady=(20, 10), sticky="nwewns", rowspan=3
        )
        self.locale_load_label = ttk.Label(
            self.locale_load_frame,
            text="Available Programs:",
            font=("-size", self.fontsize),
        )
        self.locale_load_label.grid(
            row=0, column=0, padx=5, pady=10, sticky="ew", columnspan=4
        )

        self.locale_next_prog = ttk.Button(
            self.locale_load_frame,
            text="Next",
            command=lambda: (
                self.locale_program_var.set(self.locale_program_var.get() + 1),
                self.locale_prog_label.config(text=int(self.locale_program_var.get())),
            ),
        )
        self.locale_next_prog.grid(row=1, column=3, padx=5, pady=10, sticky="ew")

        self.locale_previous_prog = ttk.Button(
            self.locale_load_frame,
            text="Previous",
            command=lambda: (
                self.locale_program_var.set(self.locale_program_var.get() - 1),
                self.locale_prog_label.config(text=int(self.locale_program_var.get())),
            ),
        )
        self.locale_previous_prog.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        self.locale_prog_label = ttk.Label(
            self.locale_load_frame, text="Program", font=("-size", self.fontsize)
        )
        self.locale_prog_label.grid(row=1, column=2, padx=5, pady=10, sticky="ew")

        self.locale_load_button = ttk.Button(
            self.locale_load_frame,
            text="Load",
            command=lambda: self.locale_load_pragram(),
        )
        self.locale_load_button.grid(row=1, column=0, padx=5, pady=10, sticky="nw")

        self.locale_update_button = ttk.Button(
            self.locale_load_frame,
            text="Update List",
            command=lambda: self.locale_update_list(),
        )
        self.locale_update_button.grid(row=1, column=4, padx=5, pady=10, sticky="nw")

    # }}}

    # {{{ Load Programs
    def load_widgets(self):
        self.separator = ttk.Separator(self.tab_2)
        self.separator.grid(row=2, column=0, padx=(10, 10), pady=10, sticky="nwewns")
        self.load_frame = ttk.LabelFrame(
            self.tab_2, text="Load Programs", padding=(20, 10)
        )
        self.load_frame.grid(
            row=3, column=0, padx=(20, 10), pady=(20, 10), sticky="nwewns", rowspan=3
        )
        self.load_label = ttk.Label(
            self.load_frame, text="Available Programs:", font=("-size", self.fontsize)
        )
        self.load_label.grid(
            row=0, column=0, padx=5, pady=10, sticky="ew", columnspan=4
        )

        self.next_prog = ttk.Button(
            self.load_frame,
            text="Next",
            command=lambda: (
                self.program_var.set(self.program_var.get() + 1),
                self.prog_label.config(text=int(self.program_var.get())),
            ),
        )
        self.next_prog.grid(row=1, column=3, padx=5, pady=10, sticky="ew")

        self.previous_prog = ttk.Button(
            self.load_frame,
            text="Previous",
            command=lambda: (
                self.program_var.set(self.program_var.get() - 1),
                self.prog_label.config(text=int(self.program_var.get())),
            ),
        )
        self.previous_prog.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        self.prog_label = ttk.Label(
            self.load_frame, text="Program", font=("-size", self.fontsize)
        )
        self.prog_label.grid(row=1, column=2, padx=5, pady=10, sticky="ew")

        self.load_button = ttk.Button(
            self.load_frame,
            text="Load",
            command=lambda: self.load_pragram(),
        )
        self.load_button.grid(row=1, column=0, padx=5, pady=10, sticky="nw")

        self.update_button = ttk.Button(
            self.load_frame,
            text="Update List",
            command=lambda: self.update_list(),
        )
        self.update_button.grid(row=1, column=4, padx=5, pady=10, sticky="nw")

    # }}}

    # {{{ Teach
    def teach_widgets(self):
        self.show_frame = ttk.LabelFrame(
            self.tab_3, text="Teach and Play", padding=(20, 10)
        )
        self.show_frame.grid(
            row=0, column=1, padx=(20, 10), pady=(20, 10), sticky="nwewns", rowspan=10
        )
        self.save_button = ttk.Button(
            self.show_frame, text="Save", command=lambda: self.save_list()
        )
        self.save_button.grid(
            row=0, column=0, padx=5, pady=10, sticky="ew", columnspan=4
        )
        self.teach_label = ttk.Label(
            self.show_frame, text="Positions:\t\t\t\t\n", font=("-size", self.fontsize)
        )
        self.teach_label.grid(
            row=1, column=0, padx=5, pady=10, sticky="ew", columnspan=4
        )

        self.teach_frame = ttk.LabelFrame(
            self.tab_3, text="Teach and Play", padding=(20, 10)
        )
        self.teach_frame.grid(
            row=3, column=0, padx=(20, 10), pady=(20, 10), sticky="nwewns"
        )

        self.add_button = ttk.Button(
            self.teach_frame, text="Add", command=lambda: self.add()
        )
        self.add_button.grid(row=1, column=0, padx=5, pady=10, sticky="nw")

        self.run_button = ttk.Checkbutton(
            self.teach_frame,
            text="Run",
            style="Toggle.TButton",
            variable=self.run_var,
            command=lambda: (self.run_list()),
        )
        self.run_button.grid(row=1, column=1, padx=5, pady=10, sticky="nw")

        self.clear_button = ttk.Button(
            self.teach_frame, text="Clear", command=lambda: self.pos_list.clear()
        )
        self.clear_button.grid(row=1, column=2, padx=5, pady=10, sticky="nw")

        self.remove_entry = ttk.Entry(self.teach_frame, textvariable=self.remove_var)
        self.remove_entry.grid(
            row=2, column=0, padx=5, pady=10, sticky="nw", columnspan=2
        )
        self.remove_button = ttk.Button(
            self.teach_frame,
            text="Remove",
            command=lambda: self.remove_list_element(),
        )
        self.remove_button.grid(row=2, column=2, padx=5, pady=10, sticky="nw")

        self.sort_entry = ttk.Entry(self.teach_frame, textvariable=self.sort_var)
        self.sort_entry.grid(
            row=3, column=0, padx=5, pady=10, sticky="nw", columnspan=2
        )
        self.sort_button = ttk.Button(
            self.teach_frame, text="Sort", command=lambda: self.sort_list()
        )
        self.sort_button.grid(row=3, column=2, padx=5, pady=10, sticky="nw")

    #  }}}

    # {{{ Update
    def update_theme(self):
        theme = self.theme_var.get()
        self.tk.call("set_theme", theme)
        if theme == "dark":
            self.logo_widgets(PATH + "img/hsel_logo_dark.png")
        else:
            self.logo_widgets(PATH + "img/hsel_logo_light.png")

    def update_tabs(self, _):
        current = self.tabs.index("current")
        if current == 0:
            self.gripper_widgets(self.tab_1, 5, 0)
            self.move_widgets(self.tab_1, 1, 1)
        elif current == 2:
            self.move_widgets(self.tab_3, 0, 0)
            self.gripper_widgets(self.tab_3, 2, 0)

    def update_error(self):
        new_error = self.delta.get_robot_errors()[0]
        new_kin_error = self.delta.get_kinematics_error()
        #
        # Kinematic Errors
        if self.count_kin_error == 5:
            self.kinematic_error = "Kinematic:\n"
            self.last_kin_error = ""
            self.count_kin_error = 0
        if self.last_kin_error is not new_kin_error:
            self.kinematic_error = (
                self.kinematic_error
                + strftime("%H:%M:%S", localtime())
                + ": "
                + self.delta.get_kinematics_error()
                + "\n"
            )
            self.count_kin_error += 1
        self.kinematic_label.config(text=self.kinematic_error)
        self.last_kin_error = self.delta.get_kinematics_error()
        #
        # Robot Errors
        if self.count_error == 5:
            self.robot_error = "Robot:\n"
            self.last_error = ""
            self.count_error = 0
        if self.last_error is not new_error:
            self.robot_error = (
                self.robot_error
                + strftime("%H:%M:%S", localtime())
                + ": "
                + self.split_list(self.delta.get_robot_errors())
            )
            self.count_error += 1
        self.robot_label.config(text=self.robot_error)
        self.last_error = self.delta.get_robot_errors()[0]

    def update(self):
        if self.delta.is_connected:
            try:
                cart_pos = self.delta.get_position_endeffector()
                axes_pos = self.delta.get_position_axes()
                self.x_label.config(text=cart_pos[0])
                self.y_label.config(text=cart_pos[1])
                self.z_label.config(text=cart_pos[2])
                self.a1_label.config(text=axes_pos[0])
                self.a2_label.config(text=axes_pos[1])
                self.a3_label.config(text=axes_pos[2])
                self.status_p.config(
                    text="status: " + self.delta.get_program_runstate()
                )
                self.loaded_p.config(
                    text="Loaded Program: " + self.delta.get_program_name()
                )
                self.enalbe_var.set(self.delta.is_enabled())

                self.connect_label.config(text="Connection: Robot is connected")

                if self.delta.is_referenced():
                    self.reference_label.config(text="Reference: Robot is referenced")
                else:
                    self.reference_label.config(
                        text="Reference: Robot is not referenced"
                    )
                self.zero_torque_var.set(self.delta.is_zero_torque())
                self.update_error()
                self.prog_label.config(text=int(self.program_var.get()))
                self.prog_label.config(text=int(self.locale_program_var.get()))
            except:
                pass
        else:
            self.connect_label.config(text="Connection: Robot is not connected")
        self.gripper_mov()
        self.teach_label.config(
            text="Positions:\t\t\t\t\n" + self.show_positions(self.pos_list)
        )
        self.after(self.update_delay.get(), self.update)

    # }}}

    # {{{ Position List
    def locale_load_pragram(self):
        file = os.listdir(PATH + "programs")[self.locale_program_var.get() - 1]
        with open(PATH + "programs/" + file, "r") as read_file:
            self.pos_list = []
            try:
                data = json.load(read_file)
                for position in data["position"]:
                    self.pos_list.append([position[0], position[1]])
            except:
                pass

    def add(self):
        list = []
        if self.delta.is_connected:
            list.append(self.delta.get_position_endeffector())
        else:
            list.append([10, 10, 200])
        list.append([self.gripper_var.get(), self.gripper_orient_var.get()])
        self.pos_list.append(list)

    def run_list(self):
        self.zero_torque_var.set(False)
        self.delta.set_zero_torque(False)
        self.enalbe_var.set(True)
        self.delta.enable()
        self.gripper_enable_var.set(True)
        if not self.delta.is_connected:
            self.run_var.set(False)
            self.gripper_enable_var.set(True)
            return
        for i in self.pos_list:
            self.delta.set_and_move(*i[0])
            while self.delta.is_moving():
                pass
            self.gripper_scale.set(i[1][0])
            self.gripper_var.set(i[1][0])
            self.gripper_orient_scale.set(i[1][1])
            self.gripper_orient_var.set(i[1][1])
            self.gripper_mov()
            while self.delta.is_gripper_moving():
                pass
        self.run_var.set(False)

    def sort_list(self):
        sort = self.sort_var.get().split()
        list = []
        for i in sort:
            i = int(i)
            list.append(self.pos_list[i - 1])
        self.pos_list = list
        self.sort_var.set("")

    def save_list(self):
        file = strftime("%Y%m%d-%H%M%S") + ".json"
        list = ""
        with open(PATH + "programs/" + file, "w") as write_file:
            list += '{\n\t"position":[\n'
            for i in self.pos_list:
                list += "\t\t" + str(i) + ",\n"
            list = list[:-2]
            list += "\n\t]\n}"
            write_file.write(list)

    def clear_list(self):
        self.pos_list = []

    def remove_list_element(self):
        try:
            index = int(self.remove_var.get()) - 1
            self.pos_list.pop(index)
        except:
            pass

    # }}}

    # {{{ Misc
    def program_names(self, list):
        if list:
            string = ""
            for count, i in enumerate(list):
                string += str(count + 1) + "\t" + i + "\n"
            return string
        else:
            return "No Information available"

    def show_positions(self, list):
        if list:
            string = "Num:\tPos:\tGrip:\n"
            for count, i in enumerate(list):
                string += str(count + 1) + " " + str(i[0]) + " " + str(i[1]) + "\n"
            return string
        else:
            return "Num:\tPos:\tGrip:\n"

    def split_list(self, list):
        if list:
            string = ""
            for i in list:
                string += i + "\n"
            return string
        else:
            return "No Information available"

    def gripper_mov(self):
        if not self.gripper_enable_var.get():
            return
        self.gripper_opening = self.gripper_var.get()
        self.gripper_orientation = self.gripper_orient_var.get()
        self.delta.control_gripper(self.gripper_opening, self.gripper_orientation)

    def enable_robot(self):
        if self.enalbe_var.get():
            self.delta.enable()
        else:
            self.delta.reset()

    def load_pragram(self):
        try:
            list = self.delta.get_list_of_porgrams()
            num = int(self.program_var.get()) - 1
            self.delta.set_program_name(list[num])
        except:
            pass

    def update_list(self):
        self.load_label.config(
            text="Programs:\n" + self.program_names(self.delta.get_list_of_porgrams())
        )

    def locale_update_list(self):
        dir_list = os.listdir(PATH + "programs")
        self.locale_load_label.config(text="Programs:\n" + self.program_names(dir_list))

    def connect(self):
        self.delta = Robot("192.168.3.11")

    # }}}


def main():
    root = tk.Tk()
    root.title("HS Emden/Leer: Delta Robot")
    root.attributes("-zoomed", True)
    root.iconphoto(False, tk.PhotoImage(file=PATH + "img/hsel_icon.png"))
    app = App(root)
    app.pack(fill="both", expand=True)

    root.update()
    app.mainloop()


# vim:foldmethod=marker
