import tkinter as tk
from tkinter import ttk
from igus_modbus import Robot
from gripper import Gripper
import datetime


class App(ttk.Frame):
    # {{{ Init
    def __init__(self, parent):
        ttk.Frame.__init__(self)

        self.dr = Robot("192.168.3.11")
        self.gripper = Gripper()
        # Make the app responsive
        for index in [0, 1, 2]:
            self.columnconfigure(index=index, weight=1)
            self.rowconfigure(index=index, weight=1)

        # Create control variables
        self.enalbe_var = tk.BooleanVar(value=True)
        self.reset_var = tk.BooleanVar(value=False)
        self.speed_var = tk.DoubleVar(value=100)
        self.global_speed_var = tk.DoubleVar(value=50)
        self.gripper_var = tk.DoubleVar(value=0)
        self.gripper_orient_var = tk.DoubleVar(value=90)
        self.time_var = None

        # Create widgets :)
        self.setup_widgets()

    # }}}

    def enable_robot(self):
        if self.enalbe_var.get():
            self.dr.enable()
        else:
            self.dr.reset()

    def setup_widgets(self):
        # {{{Control
        self.control_frame = ttk.LabelFrame(self, text="Control", padding=(20, 10))
        self.control_frame.grid(
            row=0, column=0, padx=(20, 10), pady=(20, 10), sticky="nsew"
        )

        self.enable = ttk.Checkbutton(
            self.control_frame,
            text="Enable",
            style="Toggle.TButton",
            variable=self.enalbe_var,
            # command=lambda: (print(self.enalbe_var.get()), print("x"))
            command=lambda: self.enable_robot(),
        )
        self.enable.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")

        self.reset = ttk.Button(
            self.control_frame, text="Reset", command=lambda: (self.dr.reset(), self.enalbe_var.set(False))
        )
        self.reset.grid(row=0, column=1, padx=5, pady=10, sticky="nsew")

        self.reference = ttk.Button(
            self.control_frame,
            text="Reference",
            command=lambda: self.dr.reference(True),
        )
        self.reference.grid(row=0, column=2, padx=5, pady=10, sticky="nsew")
        # }}}

        self.separator = ttk.Separator(self)
        self.separator.grid(row=2, column=0, padx=(10, 10), pady=10, sticky="ew")

        # {{{ Speed
        self.speed_frame = ttk.LabelFrame(self, text="Speed", padding=(10, 10))
        self.speed_frame.grid(row=3, column=0, padx=(20, 20), pady=10, sticky="nsew")

        self.global_speed_scale = ttk.Scale(
            self.speed_frame,
            from_=0,
            to=100,
            variable=self.global_speed_var,
            command=lambda event: (
                self.global_speed_var.set(self.global_speed_scale.get()),
                self.global_speed_label.config(text=int(self.global_speed_var.get())),
                self.dr.set_override_velocity(int(self.global_speed_var.get()))
            ),
        )
        self.global_speed_scale.grid(row=0, column=1, padx=(20, 10), pady=(20, 0), sticky="ew")

        self.global_speed_label = ttk.Label(
            self.speed_frame, text=int(self.global_speed_var.get()), font=("-size", 12)
        )
        self.global_speed_label.grid(row=0, column=2, padx=(20, 10), pady=(20, 0), sticky="ew")

        self.global_speed_title_label = ttk.Label(
            self.speed_frame, text="Global Speed", font=("-size", 12)
        )
        self.global_speed_title_label.grid(
            row=0, column=0, padx=(20, 70), pady=(20, 0), sticky="ew"
        )

        self.speed_scale = ttk.Scale(
            self.speed_frame,
            from_=0,
            to=100,
            variable=self.speed_var,
            command=lambda event: (
                self.dr.set_velocity(int(self.speed_scale.get())),
                self.speed_var.set(self.speed_scale.get()),
                self.speed_label.config(text=int(self.speed_var.get())),
            ),
        )
        self.speed_scale.grid(row=1, column=1, padx=(20, 20), pady=(20, 0), sticky="ew")

        self.speed_label = ttk.Label(
            self.speed_frame, text=int(self.speed_var.get()), font=("-size", 12)
        )
        self.speed_label.grid(row=1, column=2, padx=(20, 20), pady=(20, 0), sticky="ew")

        self.speed_title_label = ttk.Label(
            self.speed_frame, text="Speed", font=("-size", 12)
        )
        self.speed_title_label.grid(
            row=1, column=0, padx=(20, 10), pady=(20, 20), sticky="ew"
        )
        # }}}

        self.separator = ttk.Separator(self)
        self.separator.grid(row=4, column=0, padx=(20, 20), pady=20, sticky="ew")

        # {{{Gripper
        self.gripper_frame = ttk.LabelFrame(self, text="Gripper", padding=(20, 10))
        self.gripper_frame.grid(row=5, column=0, padx=(20, 20), pady=10, sticky="nsew")
        self.gripper_scale = ttk.Scale(
            self.gripper_frame,
            from_=0,
            to=100,
            variable=self.gripper_var,
            command=lambda event: (
                self.gripper.controll(int(self.gripper_scale.get())),
                self.gripper_var.set(self.gripper_scale.get()),
                self.gripper_label.config(text=int(self.gripper_var.get())),
            ),
        )
        self.gripper_scale.grid(
            row=1, column=1, padx=(20, 10), pady=(20, 0), sticky="ew"
        )

        self.gripper_label = ttk.Label(
            self.gripper_frame, text=int(self.gripper_var.get()), font=("-size", 12)
        )
        self.gripper_label.grid(
            row=1, column=2, padx=(20, 10), pady=(20, 0), sticky="ew"
        )

        self.gripper_title_label = ttk.Label(
            self.gripper_frame, text="Gripper Opening", font=("-size", 12)
        )
        self.gripper_title_label.grid(
            row=1, column=0, padx=(20, 10), pady=(20, 0), sticky="ew"
        )

        self.gripper_orient_scale = ttk.Scale(
            self.gripper_frame,
            from_=0,
            to=180,
            variable=self.gripper_orient_var,
            command=lambda event: (
                print(int(self.gripper_orient_scale.get())),
                self.gripper.rotate(int(self.gripper_orient_scale.get())),
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
            font=("-size", 12),
        )
        self.gripper_orient_label.grid(
            row=2, column=2, padx=(20, 10), pady=(20, 20), sticky="ew"
        )

        self.gripper_orient_title_label = ttk.Label(
            self.gripper_frame, text="Gripper Orientation", font=("-size", 12)
        )
        self.gripper_orient_title_label.grid(
            row=2, column=0, padx=(20, 30), pady=(20, 20), sticky="ew"
        )
        # }}}

        #{{{Move
        self.move_frame = ttk.LabelFrame(self, text="Move", padding=(20, 10))
        self.move_frame.grid(
            row=0, column=1, padx=(20, 10), pady=(20, 10), sticky="nsewne"
        )

        self.x_m = ttk.Button(
            self.move_frame,
            text="X-",
            command=lambda: self.dr.set_and_move(-1 * step, 0, 0, relative="base"),
        )
        self.x_m.grid(row=0, column=0, padx=5, pady=10)

        self.x_p = ttk.Button(
            self.move_frame,
            text="X+",
            command=lambda: self.dr.set_and_move(step, 0, 0, relative="base"),
        )
        self.x_p.grid(row=0, column=2, padx=10, pady=5)

        self.x_label = ttk.Label(
            self.move_frame,
            text="X",
            font=("-size", 12)
        )
        self.x_label.grid(row=0, column=1, padx=5, pady=10)

        self.y_m = ttk.Button(
            self.move_frame,
            text="Y-",
            command=lambda: self.dr.set_and_move(0, -1 * step, 0, relative="base"),
        )
        self.y_m.grid(row=1, column=0, padx=5, pady=10)

        self.y_p = ttk.Button(
            self.move_frame,
            text="Y+",
            command=lambda: self.dr.set_and_move(0, step, 0, relative="base"),
        )
        self.y_p.grid(row=1, column=2, padx=10, pady=5)

        self.y_label = ttk.Label(
            self.move_frame,
            text="Y",
            font=("-size", 12)
        )
        self.y_label.grid(row=1, column=1, padx=5, pady=10)

        self.z_m = ttk.Button(
            self.move_frame,
            text="Z-",
            command=lambda: self.dr.set_and_move(0, 0, -1 * step, relative="base"),
        )
        self.z_m.grid(row=2, column=0, padx=5, pady=10)

        self.z_p = ttk.Button(
            self.move_frame,
            text="Z+",
            command=lambda: self.dr.set_and_move(0, 0, step, relative="base"),
        )
        self.z_p.grid(row=2, column=2, padx=10, pady=5)

        self.z_label = ttk.Label(
            self.move_frame,
            text="Z",
            font=("-size", 12)
        )
        self.z_label.grid(row=2, column=1, padx=5, pady=10)
    #}}}


def update():
    x_val, y_val,z_val =app.dr.get_position_endeffector()
    app.x_label.config(text=x_val)
    app.y_label.config(text=y_val)
    app.z_label.config(text=z_val)
    app.enalbe_var.set(app.dr.is_enabled())
    print(app.gripper.is_connected)
    app.after(dt, update)


# {{{Main
if __name__ == "__main__":
    root = tk.Tk()
    root.title("HS Emden/Leer: Delta Robot")
    dt = 1000
    step = 10

    # Simply set the theme
    root.tk.call("source", "azure.tcl")
    root.tk.call("set_theme", "dark")

    app = App(root)
    app.pack(fill="both", expand=True)
    app.after(dt, update)

    # Set a minsize for the window, and place it in the middle
    root.update()
    root.minsize(root.winfo_width(), root.winfo_height())
    x_cordinate = int((root.winfo_screenwidth() / 2) - (root.winfo_width() / 2))
    y_cordinate = int((root.winfo_screenheight() / 2) - (root.winfo_height() / 2))
    root.geometry("+{}+{}".format(x_cordinate, y_cordinate))

    root.mainloop()
# }}}
# vim:foldmethod=marker
