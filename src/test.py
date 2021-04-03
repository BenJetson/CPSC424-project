from defaults import generate
import tkinter as tk                    
from tkinter import ttk

# Create main window frame
root = tk.Tk()
root.title("Tab Widget")
tabControl = ttk.Notebook(root)

security_tab = ttk.Frame(master=tabControl)
misc_tab = ttk.Frame(master=tabControl)



mgr = generate()

for group in mgr.groups:
    print(f"Group: {group.title}")
    tab = ttk.Frame(master=tabControl)
    tabControl.add(tab, text=group.title)
    tabControl.pack(expand=1, fill="both")

    for setting in group.items:
        print(f"    Setting: {setting.name} has value {setting.get_value()} and is type {setting.get_kind()}")
        if setting.value_list is not None:
            for value in setting.value_list:
                print(f"        Value: {value}")
        setting_frame = ttk.Frame(master=tab)
        label = tk.Label(master=setting_frame, text=setting.name, width=30, anchor="w").grid(row=0, column=0, padx=5, pady=5)
        entry = tk.Entry(master=setting_frame, width=20).grid(row=0, column=1, padx=5)
        setting_frame.pack()

    print("")


B = tk.Button(text="Apply")
B.pack(side=tk.RIGHT)
  
root.mainloop() 