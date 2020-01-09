#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  8 13:08:39 2020

Select a directory that contains .npy files, each of a separate scan. The program will then 
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


# Load data from .npy - select directory with .npy files in
def load_data(file) : 
    return np.load(Path(selected_dir/file))

# For outputting the output JSON file. 
def dump_json(dict, save_dir) : 
    name =  Path(save_dir/"output.json")
    with open(name, "w") as out : 
        json.dump(dict, out)

    
# Moves the displayed image on by + or - 1 to cycle through the files. 
def move(delta):
    global current, files, text, plot_widget, canvas
    
    
    
    # Checks if you're at the beginning or end of the images
    if not (0 <= current + delta < len(files)):
        tk.messagebox.showinfo('End', 'You have reached the end. ')
        return
    
    text.grid_forget()
    plot_widget.grid_forget()
    current += delta
    plt.close()
    plot_data = load_data(files[current])

    
    # Clears the previous plots - stops them from being plotted again
    ax.clear()
    ax.imshow(plot_data)

    
    canvas = FigureCanvasTkAgg(fig, master=root)
    plot_widget = canvas.get_tk_widget()
    plot_widget.grid(row=1, column=2)
    
    # Information for the user
    text = tk.Label(root, text="You said this was: {}".format(get_label(current)))
    text.grid(row=5, column=1)
  
    counter = tk.Label(root, text="You are on: [{}/{}] images".format(current+1, len(files)))
    counter.grid(row=6, column=1)



    
def label_positive(i, delta):
    global cwd, save_dir
    
    # Appends the new label to the existing output file
    with open("label_output.txt", 'a') as saving:
        saving.write(files[i] + "," + "1" + "\n")

    dict[files[i]] = 1 
    dump_json(dict, save_dir)

    move(delta)
    
# Label the files[i] file as a negative example and move on by delta (-1)
def label_negative(i, delta):
    global cwd, save_dir
    
    # Appends the new label to the existing output file
    with open("label_output.txt", 'a') as saving:
        saving.write(files[i] + "," + "0" + "\n")
        
    dict[files[i]] = 0
    dump_json(dict, save_dir)
    
    move(delta)

# Checks the JSON file to see if the image has been labelled and returns the result. 
def get_label(i) : 

    if files[i] in dict.keys(): 
        return labels[dict[files[i]]]
    else : 
        return "No label"


# Starts the program on the first image 
current = 0


# Set up tkinter and file locations
root = tk.Tk()
root.geometry('1200x540')
cwd = Path(os.getcwd())

selected_dir = Path(filedialog.askdirectory(parent=root, title = "Choose directory containing .npy files"))
files = os.listdir(selected_dir)

save_dir = Path(filedialog.askdirectory(parent = root, title = "Choose save directory for JSON/txt output"))

# Creates the save files. 
dict = {}
dump_json(dict, save_dir)
labels = {0: "No triangle", 1: "Triangle"}

 #The figure that is displayed on the tkinter window
fig = Figure(figsize=(8,6))
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
tk.Button(root,text="Move forward (right)", command=lambda: move(+1)).grid(row=2, column=1)
tk.Button(root, text="Move backward (left)", command=lambda: move(-1)).grid(row=2, column=0)


counter = tk.Label(root, text="You are on: [{}/{}] images".format(current+1, len(files)))
counter.grid(row=6, column=1)




frame = tk.Frame(root)
frame.grid(row=1, column=1)

root.bind('<Right>', lambda event: move(+1))
root.bind('<Left>', lambda event: move(-1))

root.bind('<t>', lambda event: label_positive(current, +1))
root.bind('<space>', lambda event: label_negative(current, +1))

move(0)
root.title("Tinder for Triangles")
root.mainloop()
