#
# CPSC 424-001 SP21
# Term Project
#
# Ben Godfrey (bfgodfr)
# and
# Avery Holder (holder9)
#
# gui_parts.py - custom GUI widgets for our program.
#

from typing import Union
import tkinter as tk
from tkinter import ttk

from base import Setting, SettingType


class SettingRowHeader:
    def __init__(self, frame: ttk.Frame):
        ttk.Label(master=frame, text="Setting", width=30, anchor="w").grid(
            row=0, column=0, padx=5, pady=5
        )
        ttk.Label(master=frame, text="Locked?", anchor="w").grid(
            row=0, column=1, padx=5, pady=5
        )
        ttk.Label(master=frame, text="Value", width=20, anchor="w").grid(
            row=0, column=2, padx=5, pady=5
        )

        ttk.Separator(master=frame, orient=tk.HORIZONTAL).grid(
            row=1, column=0, columnspan=3, sticky="ew", pady=5,
        )

        frame.pack()


class SettingRow:
    frame: ttk.Frame
    row_no: int

    setting: Setting

    widget_ckbx: ttk.Checkbutton
    ckbx_intvar: tk.IntVar

    widget_entry: Union[ttk.Entry, ttk.Combobox]
    entry_stringvar: tk.StringVar

    def __init__(self, setting: Setting, frame: ttk.Frame, row_no: int) -> None:
        # Pass necessary arguments to parent initializer.
        # super().__init__(master=master, **kwargs)

        # Save a reference to the given Setting object.
        self.setting = setting
        self.frame = frame
        self.row_no = row_no

        # Construct widgets.
        self.build_label()
        self.build_ckbx()
        self.build_entry()

        # Pack widgets.
        self.frame.pack()

    def build_label(self) -> None:
        ttk.Label(
            master=self.frame, text=self.setting.name, width=30, anchor="w"
        ).grid(row=self.row_no, column=0, padx=5, pady=5)

    def build_ckbx(self) -> None:
        self.ckbx_intvar = tk.IntVar()
        self.widget_ckbx = tk.Checkbutton(
            master=self.frame,
            variable=self.ckbx_intvar,
            command=self.handle_ckbx_change,
        )
        self.widget_ckbx.grid(row=self.row_no, column=1, padx=5)

    def build_entry(self) -> None:
        # Set the input method based on setting type.
        if (
            self.setting.get_kind() is SettingType.CHOICE
            or self.setting.get_kind() is SettingType.BOOLEAN
        ):
            choices = (
                self.setting.value_list
                if self.setting.value_list is not None
                else [True, False]
            )
            self.widget_entry = ttk.Combobox(
                master=self.frame,
                values=choices,  # list of legal values.
                width=20,
                state="disabled",
            )
            self.widget_entry.bind(
                "<<ComboboxSelected>>", self.handle_combobox_change
            )
        else:
            self.entry_stringvar = tk.StringVar()
            self.widget_entry = tk.Entry(
                master=self.frame,
                width=20,
                textvariable=self.entry_stringvar,
                validate="all",
                validatecommand=self.frame.register(self.handle_entry_change),
                state="disabled",
            )

        self.widget_entry.grid(row=self.row_no, column=2, padx=5)

    def enable_entry(self) -> None:
        if isinstance(self.widget_entry, ttk.Combobox):
            self.widget_entry.configure(state="readonly")
            self.widget_entry.current(0)
            self.handle_combobox_change()
        else:
            self.widget_entry.configure(state="normal")
            self.entry_stringvar.set("")
            self.handle_entry_change()

    def disable_entry(self) -> None:
        self.widget_entry.configure(state="disabled")

        if isinstance(self.widget_entry, ttk.Combobox):
            self.widget_entry.set("")
        else:
            self.entry_stringvar.set("")

        self.setting.unset()

    def handle_ckbx_change(self, _: ttk.Checkbutton = None) -> None:
        is_checked = self.ckbx_intvar.get() == 1

        if is_checked:
            self.enable_entry()
        else:
            self.disable_entry()

    def handle_combobox_change(self, _: ttk.Combobox = None) -> None:
        value = self.widget_entry.get()  # always a string.

        # print(f"combobox change! got {value}")  # FIXME
        self.set_from_string(value)

    def handle_entry_change(self, _: ttk.Entry = None) -> bool:
        value = self.entry_stringvar.get()  # always a string.

        # print(f"entry change! got {value}")  # FIXME
        self.set_from_string(value)

        return True  # must return True for this to be called on each input.

    def set_from_string(self, value: str) -> None:
        if len(value) == 0:
            self.setting.unset()
            return

        if self.setting.get_kind() == SettingType.NUMBER:
            value = int(value)
        if self.setting.get_kind() == SettingType.BOOLEAN:
            value = True if value == "True" else False

        self.setting.set_value(value)
