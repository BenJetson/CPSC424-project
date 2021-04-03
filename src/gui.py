from defaults import generate
from base import SettingType
import tkinter as tk                    
from tkinter import ttk

# Define function for apply button
def get_vals():
    print("Setting values:")
    for setting_obj in settings_list:
        print("    " + setting_obj[0] + ": " + setting_obj[1].get())

# Create main window frame
root = tk.Tk()
root.title("Tab Widget")
tabControl = ttk.Notebook(root)

security_tab = ttk.Frame(master=tabControl)
misc_tab = ttk.Frame(master=tabControl)

# List of settings and values. This will be a list of lists.
settings_list = []

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
        if setting.get_kind() is SettingType.CHOICE:
            entry = ttk.Combobox(master=setting_frame, values=setting.value_list, width=20)
            entry.grid(row=0, column=1, padx=5)
        else:
            entry = tk.Entry(master=setting_frame, width=20)
            entry.grid(row=0, column=1, padx=5)

        #add entry to settings_list
        temp_list = [setting.name, entry]
        settings_list.append(temp_list)
        setting_frame.pack()


B = tk.Button(text="Apply", command=get_vals).pack(side=tk.RIGHT, padx=5, pady=5)
  
root.mainloop() 