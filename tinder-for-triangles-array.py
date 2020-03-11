#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  8 13:08:39 2020

Select a .npy file that contains an array of nps each of a separate scan. The program will then 
display them on the screen and allow you to mark each as either not being a triangle or as 
containing triangles. This information is then saved to a text file (which contains all decisions 
you make, including ones you later correct) and an updated JSON file (which only contains the
latest, correct labels). The JSON output is in the form {"file-name.npy: label}, where the 
label is either 0 (no triangle) or 1 (triangle). 


@author: joseph
"""

# Imports
import numpy as np
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import os
from pathlib import Path
import tkinter.messagebox
import json 
from tkinter import filedialog
import matplotlib.pyplot as plt
from tkinter import simpledialog
import pylint

# Load data from .npy - select directory with .npy file in 
def load_data(file) : 
    return np.load(file)

# For outputting the output JSON file. 
def dump_json(dict, save_dir) : 
    name =  Path(save_dir/"output.json")
    with open(name, "w") as out : 
        json.dump(dict, out)

def load_json(filename) : 
    with open(filename, 'r') as f : 
        dict = json.load(f)
        return dict

    
# Moves the displayed image on by + or - 1 to cycle through the files. 
def move(delta):
    global current, files, text, plot_widget, canvas
    
    
    
    # Checks if you're at the beginning or end of the images
    if not (0 <= current + delta < len(file)):
        tk.messagebox.showinfo('End', 'You have reached the end. ')
        return
    
    text.grid_forget()
    plot_widget.grid_forget()
    current += delta
    plt.close()
    plot_data = file[current]

    
    # Clears the previous plots - stops them from being plotted again
    ax.clear()
    ax.imshow(plot_data)

    
    canvas = FigureCanvasTkAgg(fig, master=root)
    plot_widget = canvas.get_tk_widget()
    plot_widget.grid(row=1, column=4)
    
    # Information for the user
    text = tk.Label(root, text="You said this was: {}".format(get_label(current)))
    text.grid(row=5, column=1)
  
    counter = tk.Label(root, text="You are on: [{}/{}] images".format(current+1, len(file)))
    counter.grid(row=6, column=1)



    
def label(i, delta, label):
    global cwd, save_dir
    
    # Appends the new label to the existing output file
    with open(Path(save_dir/"label_output.txt"), 'a') as saving:
        saving.write(str(i) + "," + "{}".format(label) + "\n")

    dict[i] = label
    dump_json(dict, save_dir)

    move(delta)
    

# Checks the JSON file to see if the image has been labelled and returns the result. 
def get_label(i) : 
    if i in dict.keys(): 
        return labels[dict[i]]
    else : 
        return "No label"

def save(dict) :

    chosen_name = simpledialog.askstring(title = "Save name", prompt = "Please choose a save file name: ") 

    chosen_name += ".json"
    name =  Path(save_dir/chosen_name)
    with open(name, "w") as out : 
        json.dump(dict, out)


def load() : 
    ask = simpledialog.askstring(title = "Is there a load file?", prompt = "yes/[no]")

    if ask == "yes" :
        new_dict = Path(filedialog.askopenfilename(parent = root, title = "Choose json save file", initialdir = os.path.expanduser('~/Downloads')))
        string_dict = load_json(new_dict)
        for key in string_dict.keys() : 
            string_dict[int(key)] = string_dict.pop(key)
        return string_dict

    else : 
        return {}


    


# Starts the program on the first image 



# Set up tkinter and file locations
root = tk.Tk()
cwd = Path(os.getcwd())


select_file = Path(filedialog.askopenfilename(parent = root, title = "Choose .npy file containing data", initialdir = os.path.expanduser('~/Downloads')))

save_dir = Path(filedialog.askdirectory(parent = root, title = "Choose save directory for JSON/txt output", initialdir = os.path.expanduser('~/Desktop')))
root.geometry('1200x940')

# Creates the save files. 

dict = load()

current = len(dict)

dump_json(dict, save_dir)
labels = {0: "No triangle", 1: "Triangle", 2: "Maybe triangle"}

# array : .npy file with array of arrays containing the data
file = load_data(select_file)


#The figure that is displayed on the tkinter window
fig = Figure(figsize=(8,6))
ax = fig.add_subplot(111)
ax.imshow(file[current])

# The tkinter window
canvas = FigureCanvasTkAgg(fig, master=root)
plot_widget = canvas.get_tk_widget()
text = tk.Label(root, text="You said this was: {}".format(get_label(current)))
text.grid(row=5, column=1)

plot_widget.grid(row=1, column=2)
tk.Button(root, text = "No triangle (space)", command = lambda: label(current, +1, 0)).grid(row=1, column=0)
tk.Button(root, text = "Bias triangle (t)", command = lambda: label(current, +1, 1)).grid(row=1, column = 1)
tk.Button(root, text = "Maybe baby (/)", command = lambda: label(current, +1, 2)).grid(row=1, column = 2)

tk.Button(root,text="Move forward (right)", command=lambda: move(+1)).grid(row=2, column=1)
tk.Button(root, text="Move backward (left)", command=lambda: move(-1)).grid(row=2, column=0)

tk.Button(root, text = "Save (Ctrl-s)", command = lambda: save(dict)).grid(row = 2, column = 3)
#tk.Button(root, text = "Load", command = lambda: load()).grid(row = 2, column = 5)


counter = tk.Label(root, text="You are on: [{}/{}] images".format(current+1, len(file)))
counter.grid(row=6, column=1)

frame = tk.Frame(root)
frame.grid(row=1, column=1)

root.bind('<Right>', lambda event: move(+1))
root.bind('<Left>', lambda event: move(-1))

root.bind('<t>', lambda event: label(current, +1, 1))
root.bind('<space>', lambda event: label(current, +1, 0))
root.bind('<slash>', lambda event: label(current, +1, 2))

root.bind('<Control-s>', lambda event: save(dict))

move(0)
root.title("Tinder for Triangles")
root.mainloop()
