import tkinter as tk 
from tkinter import simpledialog
import pyperclip 

# Set up Tkinter
root = tk.Tk()
items = simpledialog.askstring("Title","Enter a string of items from latex:")

# Split up the list and alphabitise
items = items.split("\\")
items.sort()

# Put them back together as string so they can be copied to the clipboard
string = '\\'.join(items)

# Add to clipboard
pyperclip.copy(string)

# Success - not very UNIXy 
print("Sorted list copied to clipboard.")
