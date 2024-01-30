from tkinter import *
from tkinter import ttk

root = Tk()

#create a button, passing two option
button = ttk.Button(root, text = "Hello World", command="Buttonpressed").grid()

root.mainloop()