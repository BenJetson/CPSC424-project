import tkinter as tk                    
from tkinter import ttk
  
  
root = tk.Tk()
root.title("Tab Widget")
tabControl = ttk.Notebook(root, width=600, height=300)
  
security_tab = ttk.Frame(master=tabControl)
misc_tab = ttk.Frame(master=tabControl)

vals = ('5','10','15','20','25','30')
  
tabControl.add(security_tab, text ='Security')
tabControl.add(misc_tab, text ='Miscellanious')
tabControl.pack(expand = 1, fill ="both")

#Stuff for the security tab. Labels, plus a text entry.
label1 = tk.Label(master=security_tab, text="Screen Timeout").grid(row=0, column=0)
entry1 = tk.Entry(master=security_tab).grid(row=0, column=1)

# Stuff to create a combobox/dropdown selector
label4 = tk.Label(master=security_tab, text="Screen Timeout").grid(row=1, column=0)
n = tk.StringVar(value="5")
combobox = ttk.Combobox(master=security_tab, values=vals, textvariable=n).grid(row=1, column=1, pady=15)

# Create a radio button
label5 = tk.Label(master=security_tab, text="Screen Timeout").grid(row=2, column=0)
radiobutton_t = tk.Radiobutton(master=security_tab, text="True", value="true").grid(row=2, column=1)
radiobutton_f = tk.Radiobutton(master=security_tab, text="False", value="false").grid(row=2, column=2)

# Misc tab stuff
label2 = tk.Label(master=misc_tab, text="This is the second tab")
label2.pack()
  


B = tk.Button(text="Apply")
B.pack(side=tk.RIGHT)
  
root.mainloop() 