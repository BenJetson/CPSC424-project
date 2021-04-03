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


class SettingWidget(ttk.Frame):
    setting: Setting

    widget_ckbx: ttk.Checkbutton

    widget_entry: Union[ttk.Entry, ttk.Combobox]
    entry_stringvar: tk.StringVar

    def __init__(
        self,
        setting: Setting,
        master: ttk.Frame,  # unlike ttk.Frame, this is required here.
        **kwargs,
    ) -> None:
        # Pass necessary arguments to parent initializer.
        super().__init__(master=master, **kwargs)

        # Save a reference to the given Setting object.
        self.setting = setting

        # Construct widgets.
        self.build_label()
        self.build_ckbx()
        self.build_entry()

        # Pack widgets.
        self.pack()

    def build_label(self) -> None:
        tk.Label(
            master=self, text=self.setting.name, width=30, anchor="w"
        ).grid(row=0, column=0, padx=5, pady=5)

    def build_ckbx(self) -> None:
        pass

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
                master=self,
                values=choices,  # list of legal values.
                width=20,
                state="readonly",
            )
            self.widget_entry.bind(
                "<<ComboboxSelected>>", self.handle_combobox_change
            )
            self.widget_entry.current(0)
        else:
            self.entry_stringvar = tk.StringVar()
            self.widget_entry = tk.Entry(
                master=self,
                width=20,
                textvariable=self.entry_stringvar,
                validate="all",
                validatecommand=self.register(self.handle_entry_change),
            )

        self.widget_entry.grid(row=0, column=1, padx=5)

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
