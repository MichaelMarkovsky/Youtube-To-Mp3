#solves the issue of the UI being blurry
from ctypes import windll
windll.shcore.SetProcessDpiAwareness(1)

import tkinter as tk
import tkinter
from tkinter import ttk#sub module to use themed widgests
from tkinter.scrolledtext import ScrolledText


import sv_ttk

root = tkinter.Tk()#the window 
root.title("Youtube Converter")
#Don't allow the screen to be resized
root.resizable(0,0)
root.iconbitmap("Icon.ico")#replace the defult icon with a Transparent Icon

frame = ttk.Frame(root)#sets up a frame that can be used to organize and layout other GUI elements within the main application window + makes this application responsive
frame.pack()#enables the privious line(makes it responsive)


table_list_links = set()



def clear_table():
    table.delete(*table.get_children())

def Clear_table_list():
    clear_table()
    table_list_links.clear()


def Insert_link():
    #delete all the rows of the table inorder to bypass a bug
    clear_table()

    links = text_widget.get("1.0", tk.END)

    # Remove empty items from the list
    no_empty_links = [item for item in links.splitlines() if item != ""]

    filtered_links = set(no_empty_links)
    
    table_list_links.update(filtered_links)


    #insert the list of links to the table
    for link in table_list_links:
        table.insert('',tk.END,values=("","",link))




widgets_frame = ttk.LabelFrame(frame,text="Interface")
widgets_frame.grid(row=0, column=0,padx=20,pady=10)



text_widget = ScrolledText(widgets_frame, wrap="none", width=30, height=4, font=('Arial', 9))
text_widget.grid(row=1,column=0,padx=5,pady=5, sticky="ew")


insert_button = ttk.Button(widgets_frame, text="Insert",command=Insert_link)
insert_button.grid(row=2,column=0,padx=5,pady=5, sticky="nsew")

clear_button = ttk.Button(widgets_frame, text="Clear Table",command=Clear_table_list)
clear_button.grid(row=3,column=0,padx=5,pady=5, sticky="nsew")


separator = ttk.Separator(widgets_frame)
separator.grid(row =4,column=0,padx=(20,10),pady=10,sticky="ew")

download_button = ttk.Button(widgets_frame, text="Download!", style="Accent.TButton")
download_button.grid(row=5,column=0,padx=5,pady=7)



Tableframe = ttk.Frame(frame)
Tableframe.grid(row=0, column=1,padx=0,pady=10)

tablescroll = ttk.Scrollbar(Tableframe)
tablescroll.pack(side="right",fill="y")

cols = ("Name","Status","Link")
table = ttk.Treeview(Tableframe,show="headings",yscrollcommand=tablescroll.set,columns=cols , height=10)
table.column("Name",width=200)
table.column("Status",width=100)
table.column("Link",width=400)

# define headings
table.heading('Name', text='Name')
table.heading('Status', text='Status')
table.heading('Link', text='Link')
table.pack()



sv_ttk.use_dark_theme()
root.mainloop()#the loop of the application