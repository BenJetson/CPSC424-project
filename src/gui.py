#!/usr/bin/python3

#
# CPSC 424-001 SP21
# Term Project
#
# Ben Godfrey (bfgodfr)
# and
# Avery Holder (holder9)
#
# gui.py - the main driver for our program; renders the GUI.
#

import tkinter as tk
from os import geteuid
from tkinter import messagebox, ttk

from base import SettingType, is_debug_mode
from defaults import generate
from gui_parts import SettingGroupHeader, SettingRow, SettingRowHeader

# Create main window frame
root = tk.Tk()
root.title("Setting Lock Manager")

# Check for root access before starting program.
# Can be overridden using DEBUG environment variable.
if geteuid() != 0 and not is_debug_mode():
    messagebox.showerror(
        "Insufficient Privileges",
        "This program must be run as root. Try using sudo.",
    )
    exit(1)


# Create the tab interface manager.
tabControl = ttk.Notebook(root)

# Generate the list of settings
mgr = generate()

# Load the existing values from disk.
mgr.load_from_disk()


def save() -> None:
    if messagebox.askyesno(
        title="Confirmation",
        message="Are you sure?\n\nExisting settings will be overwritten.",
    ):
        mgr.save_to_disk()
        messagebox.showinfo(
            "Success",
            "Profile and locks saved to disk. Reboot or logout to see changes.",
        )


def unlock_all() -> None:
    if messagebox.askyesno(
        title="Confirmation",
        message="Are you sure?\n\nThis will immediately unlock all settings!",
    ):
        mgr.unlock_all()
        messagebox.showinfo(
            "Success",
            "Destroyed profile and locks. Reboot or logout to see changes.",
        )


# Iterate over each group and create a tab for the group.
for group in mgr.groups:
    tab = ttk.Frame(master=tabControl)
    tabControl.add(tab, text=group.title)
    tabControl.pack(expand=1, fill="both")

    group_header_frame = ttk.Frame(master=tab)
    SettingGroupHeader(group, group_header_frame)

    settings_frame = ttk.Frame(master=tab)

    # Add a header row.
    SettingRowHeader(settings_frame)

    # Iterate over each setting in the group
    # Add a label and control for each
    for index, setting in enumerate(group.items):
        SettingRow(setting, settings_frame, index + 2)

# Create buttons in  the footer.
tk.Button(text="Save", command=save).pack(side=tk.RIGHT, padx=5, pady=5)
tk.Button(text="Cancel", command=root.destroy).pack(
    side=tk.RIGHT, padx=5, pady=5
)
tk.Button(text="Unlock All", command=unlock_all).pack(
    side=tk.RIGHT, padx=5, pady=5
)

# Force the window to center on the display.
root.eval("tk::PlaceWindow . center")

# This shows the window and needs to be at the bottom iirc.
root.mainloop()
