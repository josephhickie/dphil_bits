#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  8 13:08:39 2020

@author: joseph
"""

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


# Load data from .npy 
def load_data(file) : 
    return np.load(Path(selected_dir/file))


def dump_json(dict) : 
    with open("output.json", "w") as out : 
        json.dump(dict, out)
    
    
# Moves the displayed image on by + or - 1 to cycle through the files. 
def move(delta):
    global current, files, text, plot_widget
    
    
    
    # Checks if you're at the beginning or end of the images
    if not (0 <= current + delta < len(files)):
        tk.messagebox.showinfo('End', 'You have reached the end. ')
        return
    
    text.grid_forget()
    plot_widget.grid_forget()
    current += delta
    plt.close()
    ax.imshow(load_data(files[current]))
    
    canvas = FigureCanvasTkAgg(fig, master=root)
    plot_widget = canvas.get_tk_widget()
    plot_widget.grid(row=1, column=2)
    
    text = tk.Label(root, text="You said this was: {}".format(get_label(current)))
    text.grid(row=5, column=1)
    
def label_positive(i, delta):
    
    # Appends the new label to the existing output file
    with open("label_output.txt", 'a') as saving:
        saving.write(files[i] + "," + "1" + "\n")

    dict[files[i]] = 1 
    dump_json(dict)

    move(delta)
    
# Label the files[i] file as a negative example and move on by delta (-1)
def label_negative(i, delta):
    
    # Appends the new label to the existing output file
    with open("label_output.txt", 'a') as saving:
        saving.write(files[i] + "," + "0" + "\n")
        
    dict[files[i]] = 0
    dump_json(dict)
    
    move(delta)

# Checks the JSON file to see if the image has been labelled and returns the result. 
def get_label(i) : 
    if files[i] in dict.keys(): 
        return labels[dict[files[i]]]
    else : 
        return "No label"
    
    
# Starts the program on the first image 
current = 0


# Creates the save files. 
dict = {}
dump_json(dict)
labels = {0: "No triangle", 1: "Triangle"}

# Set up tkinter and file locations
root = tk.Tk()
root.geometry('960x540')
cwd = Path(os.getcwd())


selected_dir = Path(filedialog.askdirectory(parent=root))
files = os.listdir(selected_dir)

 #The figure that is displayed on the tkinter window
fig = Figure(figsize=(8, 6))
ax = fig.add_subplot(111)
ax.imshow(load_data(files[current]))

# The tkinter window
canvas = FigureCanvasTkAgg(fig, master=root)
plot_widget = canvas.get_tk_widget()
text = tk.Label(root, text="You said this was: {}".format(get_label(current)))
text.grid(row=5, column=1)

plot_widget.grid(row=1, column=2)
tk.Button(root, text = "No triangle (space)", command = lambda: label_negative(current, +1)).grid(row=1, column=0)
tk.Button(root, text = "Bias triangle (t)", command = lambda: label_positive(current, +1)).grid(row=1, column = 1)
tk.Button(root,text="Forward (right)", command=lambda: move(+1)).grid(row=2, column=1)
tk.Button(root, text="Back (left)", command=lambda: move(-1)).grid(row=2, column=0)





frame = tk.Frame(root)
frame.grid(row=1, column=1)

root.bind('<Right>', lambda event: move(+1))
root.bind('<Left>', lambda event: move(-1))

root.bind('<t>', lambda event: label_positive(current, +1))
root.bind('<space>', lambda event: label_negative(current, +1))

move(0)
root.title("Tinder for triangles")
root.mainloop()
