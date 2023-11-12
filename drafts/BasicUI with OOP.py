#solves the issue of the UI being blurry
from ctypes import windll
windll.shcore.SetProcessDpiAwareness(1)

import tkinter as tk
import tkinter
from tkinter import ttk#sub module to use themed widgests
from tkinter.scrolledtext import ScrolledText


import sv_ttk

#tkinter.Tk()#the window
class App(tkinter.Tk):
    def __init__(self):
        super().__init__()
        #setup
        self.table_list_links = set()  
        sv_ttk.use_dark_theme()
        self.title("Youtube Converter")
        self.resizable(0,0)#Don't allow the screen to be resized
        self.iconbitmap("Icon.ico")#replace the defult icon with a Transparent Icon

        #widgets
        self.widgets = Widgets(self,self.table_list_links)

        #run
        self.mainloop()#the loop of the application


class Widgets (ttk.Frame):
    def __init__(self,parent,table_list_links):#inherants the window
        super().__init__(parent)
        self.pack()

        self.table_list_links = table_list_links

        self.interface()
        self.table()


    def interface(self):
        interface_frame = ttk.LabelFrame(self,text="Interface")
        interface_frame.grid(row=0, column=0,padx=20,pady=10)

        self.text_widget = ScrolledText(interface_frame, wrap="none", width=30, height=4, font=('Arial', 9))
        self.text_widget.grid(row=1,column=0,padx=5,pady=5, sticky="ew")


        insert_button = ttk.Button(interface_frame, text="Insert",command=self.Insert_link)
        insert_button.grid(row=2,column=0,padx=5,pady=5, sticky="nsew")

        clear_button = ttk.Button(interface_frame, text="Clear Table",command=self.Clear_table_list)
        clear_button.grid(row=3,column=0,padx=5,pady=5, sticky="nsew")


        separator = ttk.Separator(interface_frame)
        separator.grid(row =4,column=0,padx=(20,10),pady=10,sticky="ew")

        download_button = ttk.Button(interface_frame, text="Download!", style="Accent.TButton")
        download_button.grid(row=5,column=0,padx=5,pady=7)


    def table(self):
        Tableframe = ttk.Frame(self)
        Tableframe.grid(row=0, column=1,padx=0,pady=10)

        tablescroll = ttk.Scrollbar(Tableframe)
        tablescroll.pack(side="right",fill="y")

        cols = ("Name","Status","Link")
        self.table = ttk.Treeview(Tableframe,show="headings",yscrollcommand=tablescroll.set,columns=cols , height=10)
        self.table.column("Name",width=200)
        self.table.column("Status",width=100)
        self.table.column("Link",width=400)

        # define headings
        self.table.heading('Name', text='Name')
        self.table.heading('Status', text='Status')
        self.table.heading('Link', text='Link')
        self.table.pack()



    def clear_table(self):
        self.table.delete(*self.table.get_children())


    def Clear_table_list(self):
        self.clear_table()
        self.table_list_links.clear() 

    def Insert_link(self):
        #delete all the rows of the table inorder to bypass a bug
        self.clear_table()

        links = self.text_widget.get("1.0", tk.END)

        # Remove empty items from the list
        no_empty_links = [item for item in links.splitlines() if item != ""]

        filtered_links = set(no_empty_links)
        
        self.table_list_links.update(filtered_links)

        #insert the list of links to the table
        for link in self.table_list_links:
            self.table.insert('',tk.END,values=("","",link))


App()