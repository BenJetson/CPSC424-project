from defaults import generate
from base import SettingType
from gui_parts import SettingWidget
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

# Create main window frame
root = tk.Tk()
root.title("Setting Lock Manager")
tabControl = ttk.Notebook(root)

# Generate the list of settings
mgr = generate()


def save() -> None:
    if messagebox.askyesno(
        title="Confirmation",
        message="Are you sure?\n\nExisting settings will be overwritten.",
    ):
        mgr.save_to_disk()
        messagebox.showinfo("Success", "Profile and locks saved to disk.")


def unlock_all() -> None:
    if messagebox.askyesno(
        title="Confirmation",
        message="Are you sure? \n\nThis will immediately unlock all settings!",
    ):
        mgr.unlock_all()
        messagebox.showinfo("Success", "Destroyed profile and locks.")


# Iterate over each group and create a tab for the group.
for group in mgr.groups:
    tab = ttk.Frame(master=tabControl)
    tabControl.add(tab, text=group.title)
    tabControl.pack(expand=1, fill="both")

    # Iterate over each setting in the group
    # Add a label and control for each
    for setting in group.items:
        SettingWidget(setting, tab)

# Create buttons in  the footer.
tk.Button(text="Save", command=save).pack(side=tk.RIGHT, padx=5, pady=5)
tk.Button(text="Cancel", command=root.destroy).pack(
    side=tk.RIGHT, padx=5, pady=5
)
tk.Button(text="Unlock All", command=unlock_all).pack(
    side=tk.RIGHT, padx=5, pady=5
)

# This shows the window and needs to be at the bottom iirc.
root.mainloop()
