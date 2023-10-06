from time import sleep
import tkinter as tk
from tkinter import ttk
import os

from src.igus_modbus import Robot
from src.gripper import Gripper

PATH = os.path.dirname(os.path.abspath(__file__)) + "/"



class App(ttk.Frame):
    fontsize = 20
    def __init__(self, _):
        ttk.Frame.__init__(self)

        self.tk.call("source", PATH + "azure.tcl")
        self.tk.call("set_theme", "dark")
        self.dr = Robot("192.168.3.11")
        self.gripper = Gripper()
        # Make the app responsive
        for index in [0, 1, 2]:
            self.columnconfigure(index=index, weight=1)
            self.rowconfigure(index=index, weight=1)

        # Create control variables
        self.theme = ["dark", "light"]
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
        self.program_var = tk.IntVar()
        self.remove_var = tk.StringVar()
        self.update_delay = tk.IntVar(value=1000)
        self.step_var = tk.IntVar(value=10)
        self.about_msg = (
                "Delta Robot\nUser Interface to contol the Robot\nPart of Project Work\n\nCreated by:\n\tYaman Alsaady\nSupervised by:\n\tM. Eng. Jeffrey Wermann",
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
        self.load_widgets()

        self.move_widgets(self.tab_3, 0, 0)
        self.gripper_widgets(self.tab_3, 2, 0)
        self.teach_widgets()

        self.dr.set_velocity(2000)
        self.after(self.update_delay.get(), self.update)
        print(PATH)

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
        self.tab_3 = ttk.Frame(self)
        self.tabs.add(self.tab_3, text="Teach and Play")
        self.tab_4 = ttk.Frame(self)
        self.tabs.add(self.tab_4, text="More")

    def logo_widgets(self, img=PATH + "img/hsel_logo_dark.png"):
        self.logo = tk.PhotoImage(file=img)
        self.logo_label = ttk.Label(self, image=self.logo)
        self.logo_label.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.info_frame = ttk.LabelFrame(self, text="About", padding=(20, 10))
        self.info_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nwewns")

        self.about_label = ttk.Label(
            self.info_frame,
            # text="Hochschule Emden/Leer\nTechnikum\nDelta Robot",
            text=self.about_msg[0],
            font=("-size", self.fontsize),
        )
        self.about_label.grid(row=1, column=0, padx=5, pady=10, sticky="nsew")
        # self.about_label.grid(row=5, column=0, padx=5, pady=10)
        # self.reset = ttk.Button(
        #     self.info_frame, text="Reset", command=lambda: self.dr.reset()
        # )

    def setting_widgets(self):
        self.setting_frame = ttk.LabelFrame(self, text="Setting", padding=(20, 10))
        self.setting_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nwewns")

        self.enable = ttk.Checkbutton(
            self.setting_frame,
            text="Enable",
            style="Toggle.TButton",
            variable=self.enalbe_var,
            command=lambda: self.enable_robot(),
        )
        self.enable.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")

        self.reset = ttk.Button(
            self.setting_frame, text="Reset", command=lambda: self.dr.reset()
        )
        self.reset.grid(row=1, column=0, padx=5, pady=10, sticky="nsew")

        self.reference = ttk.Button(
            self.setting_frame,
            text="Reference",
            command=lambda: (
                self.reference_label.config(text="Reference: Robot is referencing"),
                self.dr.reference(True),
                sleep(0.1),
            ),
        )
        self.reference.grid(row=2, column=0, padx=5, pady=10, sticky="nsew")

        self.zero_torque = ttk.Checkbutton(
            self.setting_frame,
            text="Zero Torque",
            style="Toggle.TButton",
            variable=self.zero_torque_var,
            command=lambda: self.dr.set_zero_torque(self.zero_torque_var.get()),
        )
        self.zero_torque.grid(row=3, column=0, padx=5, pady=10, sticky="nsew")

        self.theme = ttk.Combobox(
            self.setting_frame, state="readonly", values=self.theme
        )
        self.theme.current(0)
        self.theme.grid(row=4, column=0, padx=5, pady=10, sticky="nsew")
        self.theme.bind("<<ComboboxSelected>>", self.update_theme)

        # self.update_label = ttk.Label(
        #     self.setting_frame, text="Update delay:", font=("-size", fontsize)
        # )
        # self.update_label.grid(row=5, column=0, padx=5, pady=10)
        #
        # self.update_box = ttk.Spinbox(
        #     self.setting_frame,
        #     from_=10,
        #     to=1000,
        #     increment=10,
        #     textvariable=self.update_delay,
        #     width=10,
        # )
        # self.update_box.grid(row=5, column=1, padx=5, pady=10, sticky="ew")

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

    def speed_widgets(self):
        self.separator = ttk.Separator(self.tab_1)
        self.separator.grid(row=2, column=0, padx=(10, 10), pady=10, sticky="nwew")
        self.speed_frame = ttk.LabelFrame(self.tab_1, text="Speed", padding=(20, 20))
        self.speed_frame.grid(row=3, column=0, padx=(20, 20), pady=10, sticky="nwew")

        self.global_speed_scale = ttk.Scale(
            self.speed_frame,
            from_=0,
            to=100,
            variable=self.global_speed_var,
            command=lambda _: (
                self.global_speed_var.set(self.global_speed_scale.get()),
                self.global_speed_label.config(text=int(self.global_speed_var.get())),
                self.dr.set_override_velocity(int(self.global_speed_var.get())),
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
            self.speed_frame, text="Global Speed", font=("-size", self.fontsize)
        )
        self.global_speed_title_label.grid(
            row=0, column=0, padx=(5, 10), pady=(20, 0), sticky="ew"
        )

        self.speed_scale = ttk.Scale(
            self.speed_frame,
            from_=0,
            to=100,
            variable=self.speed_var,
            command=lambda _: (
                self.dr.set_velocity(int(self.speed_scale.get() * 20)),
                self.speed_var.set(self.speed_scale.get()),
                self.speed_label.config(text=int(self.speed_var.get())),
            ),
        )
        self.speed_scale.grid(row=1, column=1, padx=(20, 20), pady=(20, 0), sticky="ew")

        self.speed_label = ttk.Label(
            self.speed_frame, text=int(self.speed_var.get()), font=("-size", self.fontsize)
        )
        self.speed_label.grid(row=1, column=2, padx=(20, 20), pady=(20, 0), sticky="ew")

        self.speed_title_label = ttk.Label(
            self.speed_frame, text="Speed", font=("-size", self.fontsize)
        )
        self.speed_title_label.grid(
            row=1, column=0, padx=(5, 10), pady=(20, 20), sticky="ew"
        )

    def gripper_widgets(self, tab_name, row, column):
        self.separator = ttk.Separator(tab_name)
        self.separator.grid(
            row=row - 1, column=0, padx=(10, 10), pady=10, sticky="nwew"
        )

        self.gripper_frame = ttk.LabelFrame(tab_name, text="Gripper", padding=(20, 20))
        self.gripper_frame.grid(
            row=row, column=column, padx=(20, 20), pady=10, sticky="nwew"
        )
        self.gripper_scale = ttk.Scale(
            self.gripper_frame,
            from_=0,
            to=100,
            variable=self.gripper_var,
            command=lambda _: (
                self.gripper_var.set(self.gripper_scale.get()),
                self.gripper_label.config(text=int(self.gripper_var.get())),
                self.gripper_mov(),
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
            variable=self.gripper_orient_var,
            command=lambda _: (
                self.gripper_orient_var.set(self.gripper_orient_scale.get()),
                self.gripper_orient_label.config(
                    text=int(self.gripper_orient_var.get())
                ),
                self.gripper_mov(),
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
            self.gripper_frame, text="Gripper Orientation", font=("-size", self.fontsize)
        )
        self.gripper_orient_title_label.grid(
            row=2, column=0, padx=(5, 10), pady=(20, 20), sticky="ew"
        )

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
            command=lambda: self.dr.set_and_move(
                -1 * self.step_var.get(), 0, 0, relative="base"
            ),
        )
        self.x_m.grid(row=0, column=0, padx=25, pady=10)

        self.x_p = ttk.Button(
            self.move_tab,
            text="X+",
            command=lambda: self.dr.set_and_move(
                self.step_var.get(), 0, 0, relative="base"
            ),
        )
        self.x_p.grid(row=0, column=2, padx=25, pady=5)

        self.x_label = ttk.Label(self.move_tab, text="X", font=("-size", self.fontsize))
        self.x_label.grid(row=0, column=1, padx=5, pady=10)

        self.y_m = ttk.Button(
            self.move_tab,
            text="Y-",
            command=lambda: self.dr.set_and_move(
                0, -1 * self.step_var.get(), 0, relative="base"
            ),
        )
        self.y_m.grid(row=1, column=0, padx=5, pady=10)

        self.y_p = ttk.Button(
            self.move_tab,
            text="Y+",
            command=lambda: self.dr.set_and_move(
                0, self.step_var.get(), 0, relative="base"
            ),
        )
        self.y_p.grid(row=1, column=2, padx=10, pady=5)

        self.y_label = ttk.Label(self.move_tab, text="Y", font=("-size", self.fontsize))
        self.y_label.grid(row=1, column=1, padx=5, pady=10)

        self.z_m = ttk.Button(
            self.move_tab,
            text="Z-",
            command=lambda: self.dr.set_and_move(
                0, 0, -1 * self.step_var.get(), relative="base"
            ),
        )
        self.z_m.grid(row=2, column=0, padx=5, pady=10)

        self.z_p = ttk.Button(
            self.move_tab,
            text="Z+",
            command=lambda: self.dr.set_and_move(
                0, 0, self.step_var.get(), relative="base"
            ),
        )
        self.z_p.grid(row=2, column=2, padx=10, pady=5)

        self.z_label = ttk.Label(self.move_tab, text="Z", font=("-size", self.fontsize))
        self.z_label.grid(row=2, column=1, padx=5, pady=10)

        self.step_label = ttk.Label(
            self.move_tab, text="Stops per Move:", font=("-size", self.fontsize)
        )
        self.step_label.grid(row=3, column=0, padx=5, pady=10)

        self.step = ttk.Spinbox(
            self.move_tab,
            from_=1,
            to=100,
            increment=1,
            textvariable=self.step_var,
            width=10,
        )
        self.step.grid(row=3, column=2, padx=5, pady=10, sticky="ew")

        # Tab #2
        self.axes_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.axes_tab, text="Joints")

        self.a1_m = ttk.Button(
            self.axes_tab,
            text="A1-",
            command=lambda: self.dr.set_and_move(
                -1 * self.step_var.get(), 0, 0, relative="base", movement="axes"
            ),
        )
        self.a1_m.grid(row=0, column=0, padx=25, pady=10)

        self.a1_p = ttk.Button(
            self.axes_tab,
            text="A1+",
            command=lambda: self.dr.set_and_move(
                self.step_var.get(), 0, 0, relative="base", movement="axes"
            ),
        )
        self.a1_p.grid(row=0, column=2, padx=25, pady=5)

        self.a1_label = ttk.Label(self.axes_tab, text="A1", font=("-size", self.fontsize))
        self.a1_label.grid(row=0, column=1, padx=5, pady=10)

        self.a2_m = ttk.Button(
            self.axes_tab,
            text="A2-",
            command=lambda: self.dr.set_and_move(
                0, -1 * self.step_var.get(), 0, relative="base", movement="axes"
            ),
        )
        self.a2_m.grid(row=1, column=0, padx=5, pady=10)

        self.a2_p = ttk.Button(
            self.axes_tab,
            text="A2+",
            command=lambda: self.dr.set_and_move(
                0, self.step_var.get(), 0, relative="base", movement="axes"
            ),
        )
        self.a2_p.grid(row=1, column=2, padx=10, pady=5)

        self.a2_label = ttk.Label(self.axes_tab, text="A2", font=("-size", self.fontsize))
        self.a2_label.grid(row=1, column=1, padx=5, pady=10)

        self.a3_m = ttk.Button(
            self.axes_tab,
            text="A3-",
            command=lambda: self.dr.set_and_move(
                0, 0, -1 * self.step_var.get(), relative="base", movement="axes"
            ),
        )
        self.a3_m.grid(row=2, column=0, padx=5, pady=10)

        self.a3_p = ttk.Button(
            self.axes_tab,
            text="A3+",
            command=lambda: self.dr.set_and_move(
                0, 0, self.step_var.get(), relative="base", movement="axes"
            ),
        )
        self.a3_p.grid(row=2, column=2, padx=10, pady=5)

        self.a3_label = ttk.Label(self.axes_tab, text="A3", font=("-size", self.fontsize))
        self.a3_label.grid(row=2, column=1, padx=5, pady=10)

        self.step_label = ttk.Label(
            self.axes_tab, text="Stops per Move:", font=("-size", self.fontsize)
        )
        self.step_label.grid(row=3, column=0, padx=5, pady=10)

        self.step = ttk.Spinbox(
            self.axes_tab,
            from_=1,
            to=100,
            increment=1,
            textvariable=self.step_var,
            width=10,
        )
        self.step.grid(row=3, column=2, padx=5, pady=10, sticky="ew")

    def error_widgets(self):
        self.separator = ttk.Separator(self.tab_1)
        self.separator.grid(row=2, column=1, padx=(10, 10), pady=10, sticky="nwew")
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
            command=lambda: self.dr.controll_programs("start"),
        )
        self.play.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")
        self.stop = ttk.Button(
            self.programs_frame,
            text="Stop",
            command=lambda: self.dr.controll_programs("stop"),
        )
        self.stop.grid(row=0, column=1, padx=5, pady=10, sticky="nsew")
        self.pause = ttk.Button(
            self.programs_frame,
            text="Pause",
            command=lambda: self.dr.controll_programs("pause"),
        )
        self.pause.grid(row=0, column=2, padx=5, pady=10, sticky="nsew")
        self.continue_p = ttk.Button(
            self.programs_frame,
            text="Continue",
            command=lambda: self.dr.controll_programs("continue"),
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

        # self.load_p = ttk.Spinbox(
        #     self.load_frame, from_=1, to=100, increment=1, textvariable=self.program_var
        # )
        # self.load_p.insert(0, "Program Number")
        # self.load_p.grid(row=1, column=0, padx=5, pady=10, sticky="ew")

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

    def teach_widgets(self):
        self.show_frame = ttk.LabelFrame(
            self.tab_3, text="Teach and Play", padding=(20, 10)
        )
        self.show_frame.grid(
            row=0, column=1, padx=(20, 10), pady=(20, 10), sticky="nwewns", rowspan=10
        )
        self.teach_label = ttk.Label(
            self.show_frame, text="Positions:", font=("-size", self.fontsize)
        )
        self.teach_label.grid(
            row=0, column=0, padx=5, pady=10, sticky="ew", columnspan=4
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

    def update(self):
        if self.dr.is_connected:
            try:
                cart_pos = self.dr.get_position_endeffector()
                axes_pos = self.dr.get_position_axes()
                self.x_label.config(text=cart_pos[0])
                self.y_label.config(text=cart_pos[1])
                self.z_label.config(text=cart_pos[2])
                self.a1_label.config(text=axes_pos[0])
                self.a2_label.config(text=axes_pos[1])
                self.a3_label.config(text=axes_pos[2])
                self.status_p.config(text="status: " + self.dr.get_program_runstate())
                self.loaded_p.config(
                    text="Loaded Program: " + self.dr.get_program_name()
                )
                self.robot_label.config(
                    text="Robot:\n" + self.split_list(self.dr.get_robot_errors())
                )
                self.kinematic_label.config(
                    text="Kinematic:\n" + self.dr.get_kinematics_error()
                )
                self.load_label.config(
                    text="Programs:\n"
                    + self.program_names(self.dr.get_list_of_porgrams())
                )
                self.enalbe_var.set(self.dr.is_enabled())

                if self.dr.is_connected:
                    self.connect_label.config(text="Connection: Robot is connected")
                else:
                    self.connect_label.config(text="Connection: Robot is not connected")

                if self.dr.is_referenced():
                    self.reference_label.config(text="Reference: Robot is referenced")
                else:
                    self.reference_label.config(
                        text="Reference: Robot is not referenced"
                    )
                self.zero_torque_var.set(self.dr.is_zero_torque())
            except:
                pass
        else:
            self.connect_label.config(text="Connection: Robot is not connected")
        self.prog_label.config(text=int(self.program_var.get()))
        self.teach_label.config(
            text="Positions:\t\t\t\t\n" + self.show_positions(self.pos_list)
        )
        self.after(self.update_delay.get(), self.update)

    def update_theme(self, _):
        theme = self.theme.get()
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

    def program_names(self, list):
        # self.dr.print_list_of_programs()
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
        if self.dr.is_connected and not self.dr.get_globale_signal(6):
            self.gripper.controll(
                int(self.gripper_scale.get()), int(self.gripper_orient_scale.get())
            ),

    def enable_robot(self):
        if self.enalbe_var.get():
            self.dr.enable()
        else:
            self.dr.reset()

    def load_pragram(self):
        try:
            list = self.dr.get_list_of_porgrams()
            num = int(self.program_var.get()) - 1
            self.dr.set_program_name(list[num])
        except:
            pass

    def add(self):
        list = []
        if self.dr.is_connected:
            list.append(self.dr.get_position_endeffector())
        else:
            list.append([0, 0, 0])
        list.append([self.gripper_var.get(), self.gripper_orient_var.get()])
        self.pos_list.append(list)

    def run_list(self):
        self.zero_torque_var.set(False)
        self.enalbe_var.set(True)
        self.dr.enable()
        if self.run_var.get():
            if self.dr.is_connected or True:
                k = 1
                for i in self.pos_list:
                    if i[0]:
                        self.dr.set_and_move(*i[0])
                        print(k, *i[0], *i[1])
                        k += 1
                    if self.gripper.is_connected:
                        if i[1]:
                            if (
                                i[1][0] != self.gripper.opening
                                or i[1][0] != self.gripper.orientation
                            ):
                                self.gripper.controll(*i[1])
                                sleep(0.5)
        self.run_var.set(False)

    def sort_list(self):
        sort = self.sort_var.get().split()
        list = []
        for i in sort:
            i = int(i)
            list.append(self.pos_list[i - 1])
        self.pos_list = list
        self.sort_var.set("")

    def clear_list(self):
        self.pos_list = []

    def remove_list_element(self):
        try:
            index = int(self.remove_var.get()) - 1
            self.pos_list.pop(index)
        except:
            pass

def main():
    root = tk.Tk()
    root.title("HS Emden/Leer: Delta Robot")
    # root.attributes("-fullscreen", True)
    root.attributes("-zoomed", True)
    # root.iconbitmap(PATH+"img/hsel_logo.ico")
    root.iconphoto(False, tk.PhotoImage(file=PATH + "img/hsel_icon.png"))
    app = App(root)
    app.pack(fill="both", expand=True)

    root.update()
    app.mainloop()
