from defaults import generate
from base import SettingType
from gui_parts import SettingWidget
import tkinter as tk
from tkinter import ttk

# Create main window frame
root = tk.Tk()
root.title("Tab Widget")
tabControl = ttk.Notebook(root)

# Generate the list of settings
mgr = generate()

# Iterate over each group and create a tab for the group.
for group in mgr.groups:
    tab = ttk.Frame(master=tabControl)
    tabControl.add(tab, text=group.title)
    tabControl.pack(expand=1, fill="both")

    # Iterate over each setting in the group
    # Add a label and control for each
    for setting in group.items:
        SettingWidget(setting, tab)

# Button for applying settings
B = tk.Button(text="Apply", command=mgr.save_to_disk).pack(
    side=tk.RIGHT, padx=5, pady=5
)

# This shows the window and needs to be at the bottom iirc.
root.mainloop()
