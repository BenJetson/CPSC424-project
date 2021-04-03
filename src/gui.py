from defaults import generate
import tkinter as tk                    
from tkinter import ttk

# Create main window frame
root = tk.Tk()
root.title("Tab Widget")
tabControl = ttk.Notebook(root)

security_tab = ttk.Frame(master=tabControl)
misc_tab = ttk.Frame(master=tabControl)

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
        setting_frame = ttk.Frame(master=tab)
        label = tk.Label(master=setting_frame, text=setting.name, width=30, anchor="w").grid(row=0, column=0, padx=5, pady=5)
        entry = tk.Entry(master=setting_frame, width=20).grid(row=0, column=1, padx=5)
        setting_frame.pack()


B = tk.Button(text="Apply").pack(side=tk.RIGHT, padx=5, pady=5)
  
root.mainloop() 