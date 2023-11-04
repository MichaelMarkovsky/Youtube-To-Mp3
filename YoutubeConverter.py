#imports for webscraping
from selenium import webdriver#importing a library that will automate the action of openning a web browser
from selenium.webdriver.common.by import By#imports a library that alows us to make specific selections(class,id..)
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#imports for creating the download folder
import os
import sys

import string
from string import punctuation
import time

#IMPORTS FOR UI
#solves the issue of the UI being blurry
from ctypes import windll
windll.shcore.SetProcessDpiAwareness(1)

import tkinter as tk
import tkinter
from tkinter import ttk#sub module to use themed widgests
from tkinter.scrolledtext import ScrolledText
from tkinter import messagebox 

import sv_ttk
import threading
from threading import Event

#IMPORT OF Checking if a YouTube link is valid involves verifying its format and structure
import re






#tkinter.Tk()#the window
class App(tkinter.Tk):
    def __init__(self):
        super().__init__()
        #setup
        self.create_download_folder_if_not_exists()
        sv_ttk.use_dark_theme()
        self.title("Youtube Converter")
        self.resizable(0,0)#Don't allow the screen to be resized
        self.iconbitmap("Icon.ico")#replace the defult icon with a Transparent Icon

        #widgets
        self.widgets = Widgets(self)
        

        self.protocol("WM_DELETE_WINDOW", self.on_closing)#if i close the program at the time its downaloding ,its going to stop the download and close the browser if its open

        #run
        self.mainloop()#the loop of the application

    def on_closing(self):
        try:
            self.widgets.driver_va.quit()
        except:
            pass
        self.destroy()

    @staticmethod
    def create_download_folder_if_not_exists():
        script_directory = os.path.dirname(os.path.abspath(sys.argv[0])) #give me the path of the script

        # checking if the directory downloads 
        # exist or not.
        if not os.path.exists(f"{script_directory}\downloads"):
            # if the downloads directory is not present 
            # then create it.
            os.makedirs(f"{script_directory}\downloads")


    

class Widgets (ttk.Frame):
    def __init__(self,parent):#inherants the window
        super().__init__(parent)
        self.pack()

        self.table_list_links = set()
        self.table_list_of_tuples = list()
        self.event = Event()

        self.elapsed_time_total = float()#total time for the whole runtime of all the table

        self.completed_num = int()#all table's successful downloads
        self.file_exists = int()
        self.not_confirm_file = int()
        self.failed_num = int()

        self.back_error = False

        self.driver_va = None
        
        self.interface()
        self.table()


    def interface(self):
        interface_frame = ttk.LabelFrame(self,text="Interface")
        interface_frame.grid(row=0, column=0,padx=20,pady=10)

        self.text_widget = ScrolledText(interface_frame, wrap="none", width=30, height=4, font=('Arial', 9))
        self.text_widget.grid(row=1,column=0,padx=5,pady=5, sticky="ew")


        self.insert_button = ttk.Button(interface_frame, text="Insert",command=self.Insert_link)
        self.insert_button.grid(row=2,column=0,padx=5,pady=5, sticky="nsew")

        self.delete_row_button = ttk.Button(interface_frame, text="Delete a Link",command=self.delete_selected_row)
        self.delete_row_button.grid(row=3,column=0,padx=5,pady=5, sticky="nsew")

        self.clear_table_button = ttk.Button(interface_frame, text="Clear Table",command=self.Clear_table_list)
        self.clear_table_button.grid(row=4,column=0,padx=5,pady=5, sticky="nsew")


        separator = ttk.Separator(interface_frame)
        separator.grid(row =5,column=0,padx=(20,10),pady=10,sticky="ew")

        
        self.check_var = tk.BooleanVar(value=True)# Create a BooleanVar and set its initial value to True,which means that the button will be checked by default
        self.switch = ttk.Checkbutton(interface_frame, text="Clean Mode", style="Switch.TCheckbutton",variable=self.check_var)
        self.switch.grid(row=6, column=0,pady=5)

        separator = ttk.Separator(interface_frame)
        separator.grid(row =7,column=0,padx=(20,10),pady=10,sticky="ew")

        # Create a StringVar to store the button text
        self.button_var = tk.StringVar()
        self.button_var.set("Download!")
        self.download_button = ttk.Button(interface_frame, textvariable=self.button_var, style="Accent.TButton",command=self.Download)
        self.download_button.grid(row=8,column=0,padx=5,pady=7)


    def on_scroll(self,*args):#will be called whenever the scrollbar is manipulated.    It calls the yview method of the table widget with the provided arguments, allowing the text widget to scroll vertically.
        self.table.yview(*args)

    def table(self):
        Tableframe = ttk.Frame(self)
        Tableframe.grid(row=0, column=1,padx=0,pady=10)

        tablescroll = ttk.Scrollbar(Tableframe,command=self.on_scroll)
        tablescroll.pack(side="right",fill="y")

        cols = ("Name","Status","Link")
        self.table = ttk.Treeview(Tableframe,show="headings",yscrollcommand=tablescroll.set,columns=cols , height=13)
        self.table.column("Name",width=200)
        self.table.column("Status",width=100)
        self.table.column("Link",width=400)

        # define headings
        self.table.heading('Name', text='Name')
        self.table.heading('Status', text='Status')
        self.table.heading('Link', text='Link')
        self.table.pack()


    
    def delete_selected_row(self):
        selected_item = self.table.selection()
        if selected_item:
            values = self.table.item(selected_item, 'values')
            link = values[2]
            print(f"selected Link: {link}")
            try:
                self.table_list_links.remove(link)
            except:#the link must be completed therefore its deleted
                pass

            # Remove tuples containing the specified item
            self.table_list_of_tuples = [tpl for tpl in self.table_list_of_tuples if link not in tpl]
            

            self.table.delete(selected_item)
            

    def clear_table(self):
        self.table.delete(*self.table.get_children())


    def Clear_table_list(self):
        self.clear_table()
        self.table_list_links.clear() 
        self.table_list_of_tuples.clear()

        #clear the counting valeus
        self.elapsed_time_total = float()#total time for the whole runtime of all the table

    @staticmethod
    def is_valid_youtube_link(link):
        # Define a regular expression pattern for a YouTube link
        youtube_pattern = re.compile(
            r'(https?://)?(www\.)?'
            '(youtube|youtu|youtube-nocookie)\.(com|be)/'
            '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')

        # Check if the link matches the pattern
        match = youtube_pattern.match(link)
        return bool(match)

    def Insert_link(self):
        text_content = self.text_widget.get("1.0", tk.END).strip()
        if not text_content:
            messagebox.showerror("Input error", "Your input is empty")

        links_in_treeview = list()
        items = self.table.get_children()
        for item in items:
            values = self.table.item(item, 'values')
            links_in_treeview.append(values[2])
                

        #delete all the rows of the table inorder to bypass a bug
        self.clear_table()

        links = self.text_widget.get("1.0", tk.END)

        # Remove empty items from the list
        no_empty_links = [item for item in links.splitlines() if item != ""]

        filtered_links = set(no_empty_links)

        #Checking if a YouTube link is valid and removing invalid onces from the list inorder to make the process faster.
        filtered_links_copy = filtered_links.copy()
        for link in filtered_links_copy:
            if self.is_valid_youtube_link(link):
                print("Valid YouTube link")
            else:
                print("Invalid YouTube link")
                filtered_links.remove(link)

        for link in filtered_links:
            if link not in links_in_treeview:
                self.table_list_links.add(link)
            else:
                print(f'This link is already in the table: {link}')



        #insert the list of links to the table if not exists
        check_list = list()
        for item in self.table_list_of_tuples:
            check_list.append(item[2])

        for link in self.table_list_links:
            if link not in check_list:
                #self.table.insert('',tk.END,values=("","",link))
                self.table_list_of_tuples.append(tuple(("","",link)))

        for tuple_ in self.table_list_of_tuples:
            self.table.insert('',tk.END,values=(tuple_))

        self.text_widget.delete(1.0, tk.END)  # Delete from the start to the end


    def update_table(self):
        #delete all the rows of the table inorder to bypass a bug
        self.clear_table()
        #insert the list of links to the table
        for link in self.table_list_of_tuples:
            self.table.insert('',tk.END,values=(link[0],link[1],link[2]))

    def Download(self):#the youtube link(that you want to download to mp3) and the file location you want the file to be downloaded to( if not given then it will be downloaded to the default location )
        #download the file to the right path due to the format
        if not self.table_list_links:
            messagebox.showerror("Input error", "Your table is empty")
        else:
            if self.button_var.get() == "Download!":
                self.button_var.set("Stop!")
                
                #disable buttons
                self.switch["state"] = "disabled"
                self.insert_button["state"] = "disabled"
                self.clear_table_button["state"] = "disabled"
                self.delete_row_button["state"] = "disabled"

                def run(event: Event):
                    start_time = time.perf_counter()

                    while True:
                        self.back_error==False
                        script_directory = f"{os.path.dirname(os.path.abspath(sys.argv[0]))}\downloads"
                        File_location = script_directory          
                        #Example:   "C:\\Users\\misha\\Desktop\\" 

                        Youtube_links = list(self.table_list_links)
                        driverr = self.driver(File_location)
                        self.driver_va = driverr                      
                            
                        self.Youtube_To_MP3_Download(Youtube_links,driverr)#the youtube link(that you want to download to mp3) and the file location you want the file to be downloaded to( if not given then it will be downloaded to the default location )                    
                        
                        if self.event.is_set():
                            print("This event has been stopped prematurely")

                            self.button_var.set("Download!")
                            self.event.clear()

                            end_time = time.perf_counter()
                            elapsed_time = end_time - start_time#seconds for this run
                            self.elapsed_time_total+=elapsed_time
                            
                            #enable buttons
                            self.switch["state"] = "normal"
                            self.insert_button["state"] = "normal"
                            self.clear_table_button["state"] = "normal"
                            self.delete_row_button["state"] = "normal"

                            if not self.table_list_links:#empty
                                seconds = str(int(self.elapsed_time_total%60))
                                if int(self.elapsed_time_total%60)<10:
                                    seconds = f'0{int(self.elapsed_time_total%60)}'
                                total_time = f'{int(self.elapsed_time_total/60)}:{seconds} minutes' #minutes
                                
                                completed_num = int()#all table's successful downloads
                                file_exists = int()
                                not_confirm_file = int()
                                failed_num = int()

                                for row in self.table_list_of_tuples:
                                    if row[1] == "Completed" or row[1] == "Error - File exists":
                                        completed_num+=1
                                    if row[1] =="Error - File exists":
                                        file_exists +=1
                                    if row[1] != "Completed" and row[1] != "Error - File exists":
                                        if row[1] =="Error - Timeout ,could not confirm the file":
                                            not_confirm_file+=1
                                        failed_num+=1


                                lines = ["Download Completed","",f"Total completed: {completed_num}",f"Total file exists:  {file_exists}",f"Total file not confirmed:    {not_confirm_file}",f"Total failed:   {failed_num}","",f"Total Runtime:   {total_time}"]
                                messagebox.showinfo("", "\n".join(lines)) 

                            break
                        else:
                            if self.back_error==False:
                                print("This event has been stopped maturely")

                                self.button_var.set("Download!")
                                
                                end_time = time.perf_counter()
                                elapsed_time = end_time - start_time#seconds for this run
                                self.elapsed_time_total+=elapsed_time

                                #enable buttons
                                self.switch["state"] = "normal"
                                self.insert_button["state"] = "normal"
                                self.clear_table_button["state"] = "normal"
                                self.delete_row_button["state"] = "normal"

                                if not self.table_list_links:#empty
                                    seconds = str(int(self.elapsed_time_total%60))
                                    if int(self.elapsed_time_total%60)<10:
                                        seconds = f'0{int(self.elapsed_time_total%60)}'
                                    total_time = f'{int(self.elapsed_time_total/60)}:{seconds} minutes' #minutes
                                    
                                    completed_num = int()#all table's successful downloads
                                    file_exists = int()
                                    not_confirm_file = int()
                                    failed_num = int()

                                    for row in self.table_list_of_tuples:
                                        if row[1] == "Completed" or row[1] == "Error - File exists":
                                            completed_num+=1
                                        if row[1] =="Error - File exists":
                                            file_exists +=1
                                        if row[1] != "Completed" and row[1] != "Error - File exists":
                                            if row[1] =="Error - Timeout ,could not confirm the file":
                                                not_confirm_file+=1
                                            failed_num+=1


                                    lines = ["Download Completed","",f"Total completed: {completed_num}",f"Total file exists:  {file_exists}",f"Total file not confirmed:    {not_confirm_file}",f"Total failed:   {failed_num}","",f"Total Runtime:   {total_time}"]
                                    messagebox.showinfo("", "\n".join(lines)) 
                                    
                                break
                            



                t = threading.Thread(target=run, args=(self.event,))
                t.daemon = True  # Daemon threads are background threads that automatically exit when the main program finishes.
                t.start()
            else:
                self.event.set()
                self.button_var.set("Download!")
    
    
    def driver(self,download_location):
        #SETUP
        # these 2 lines make it so that the browser wont close automaticly
        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach", True)
        
        options.add_argument("--mute-audio")#mute the audio of potential ads

        if self.check_var.get():#Checkbutton Checked
            options.add_argument("--headless")#without a graphical user interface.for a clean download(not seeing the webscraping action of the broswer)
            options.add_argument("--log-level=3")#Sets the minimum log level. Valid values are from 0 to 3: INFO = 0, WARNING = 1, LOG_ERROR = 2, LOG_FATAL = 3
            options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36")#change the user agent to Chrome from HeadlessChrome in order to potentially not get blocked
        else:#Checkbutton Unchecked
            pass
            

        options.binary_location = r"C:\Users\misha\Desktop\Coding\Coding projects\Python\WebScraping and Automation Python\Youtube Converter\chrome-win64\chrome.exe"
        chrome_driver_binary = r"C:\Users\misha\Desktop\Coding\Coding projects\Python\WebScraping and Automation Python\Youtube Converter\chromedriver.exe"
        

        if (download_location!= None):#if ive given a file location then proceed, else download the file to the default folder(which is the "Download" folder)
            #Change the default download location
            prefs = {'download.default_directory': download_location}
            options.add_experimental_option('prefs', prefs)

        driver = webdriver.Chrome(chrome_driver_binary, chrome_options=options)
        return driver


    def Youtube_To_MP3_Download(self,youtube_links,driver):
        
        

        #WEBSCRAPING STARTS HERE
        driver.get("https://ytmp3.nu/nBlF/")#gets into this url(opens this site)

        #timeout:
        driver.implicitly_wait(30)#waits untill finds the elemnt, an x amount of time in order to prevent errors because of slow processes like loading the site,server..its a timeout for all elements

        ##########inserting the first song so that the process will be shorter for this site##############
        Textbox_element = driver.find_element(By.ID,"url")#selects an element and stores it as a web element
        Textbox_element.click()
        Textbox_element.send_keys("https://www.youtube.com/watch?v=3zh9Wb1KuW8&list=RDMM&index=3")#"types"

        

        WebDriverWait(driver, 10).until(    
            EC.element_to_be_clickable(
                (By.XPATH,"/html/body/form/div[2]/input[2]")
            )
        )
        Convert_button = driver.find_element(By.XPATH,"/html/body/form/div[2]/input[2]")
        Convert_button.click()#Clicks on the convert button

        WebDriverWait(driver, 10).until(    
            EC.element_to_be_clickable(
                (By.XPATH,"/html/body/form/div[2]/a[2]")
            )
        )
        
        
        #######################################################################################################

        def download_songs(youtube_links,driver):
            for link in youtube_links:
                if self.event.is_set() == True:#if i pressed the button to stop,then stop downloading the links and quite the driver
                    print("Quites the driver")
                    driver.quit()
                    return
                else:
                    songName = ''
                    def link_index():#returns the index of the item that has this link in order to add name and status
                            for item in self.table_list_of_tuples:
                                if item[2] == link:
                                    return (self.table_list_of_tuples.index(item))
                    try:                        
                        Convert_button2 = driver.find_element(By.XPATH,"/html/body/form/div[2]/a[2]")
                        Convert_button2.click()#Clicks on the convert button

                        Textbox_element = driver.find_element(By.ID,"url")#selects an element and stores it as a web element
                        Textbox_element.send_keys(link)#"types"


                        WebDriverWait(driver, 10).until(    
                            EC.element_to_be_clickable(
                                (By.XPATH,"/html/body/form/div[2]/input[2]")
                            )
                        )
                        Convert_button = driver.find_element(By.XPATH,"/html/body/form/div[2]/input[2]")
                        Convert_button.click()#Clicks on the convert button




                        #waits untill title is visible in the site
                        WebDriverWait(driver, 10).until(    
                            lambda driver:(
                                driver.find_element(By.XPATH,"/html/body/form/div[1]").text.splitlines()[0]!="loading title"
                            )
                        )

                        Song_Name_with_pun = driver.find_element(By.XPATH,"/html/body/form/div[1]").text.splitlines()[0] #Gets the song TITLE + DURATION as a string, then splits the lines into a list , where the first item is the name and the second is the duration
                        Song_Name_without_pun = Song_Name_with_pun        
                                # initializing punctuations string
                        punc = '''!()-[]{};:'"\,<>./?@#$%^&*_~」「+'''
                        
                        # Removing punctuations in string
                        # Using loop + punctuation string
                        for ele in Song_Name_without_pun:
                            if ele in punc:
                                Song_Name_without_pun = Song_Name_without_pun.replace(ele, "")

                        print(f'before : {self.back_error}')

                        print(Song_Name_with_pun)
                        if Song_Name_with_pun=="An backend error occurred. Error code (p:3 / e:0).":
                            self.table_list_of_tuples[link_index()] = (Song_Name_with_pun,"Error",link)
                            self.update_table()
                            
                            self.back_error = True
                            #delete the link from the set
                            try:
                                self.table_list_links.remove(link)
                            except:
                                pass

                            driver.quit()
                            return 
                        else:
                            self.back_error = False
                            
                        songName +=Song_Name_with_pun


                        script_directory = os.path.dirname(os.path.abspath(sys.argv[0])) #give me the path of the script
                        # directory/folder path
                        dir_path = (f"{script_directory}\downloads")
                        dir_list = os.listdir(dir_path)
                        
                        for file in dir_list:
                            pass

                        #code to remove whitespace
                        def remove(string):
                            return string.replace(" ", "")

                        #if the file exists then dont download it,else do.

                        # Removing punctuations in string
                        # Using loop + punctuation string
                        Song_Name_without_pun = Song_Name_without_pun.translate(str.maketrans('', '', string.punctuation))#removes punctuation,but not all(like ’). therefore i make a second remove pun function:

                        # initializing punctuations string
                        punc = '''!()-[]{};:'"\,<>./?@#$%^&*_~’'''
                        
                        # Removing punctuations in string
                        # Using loop + punctuation string
                        for ele in Song_Name_without_pun:
                            if ele in punc:
                                Song_Name_without_pun = Song_Name_without_pun.replace(ele, "")


                        File_Exists = False

                        file_sum = len(os.listdir(dir_path))
                        for file in os.listdir(dir_path):
                                    ftitle = file
                                    ftitle = ftitle.translate(str.maketrans('', '', string.punctuation))#removes punctuation
                                    file_sum -=1
                                    if remove(ftitle.lower()).find(remove(Song_Name_without_pun.lower())) > -1:#if file does not exist,then rename it and complete
                                        File_Exists = True
                                        print("File exists")
                                        self.table_list_of_tuples[link_index()] = (Song_Name_with_pun,"Error - File exists",link)
                                        self.update_table()


                        if File_Exists == False:
                            WebDriverWait(driver, 30).until(    
                            EC.element_to_be_clickable(
                                (By.XPATH,"/html/body/form/div[2]/a[1]")
                                )
                            )

                            Download_button = driver.find_element(By.XPATH,"/html/body/form/div[2]/a[1]")
                            Download_button.click()#Clicks on the download button

                            
                            ###########checks if the download has been completed
                            timeoutError = False
                            try:                        
                                #timeout system
                                start_time = time.time()
                                seconds = 30

                                found = False
                                while(found==False):
                                    #timeout system
                                    current_time = time.time()
                                    elapsed_time = current_time - start_time

                                    if elapsed_time > seconds:
                                        print("Finished iterating in: " + str(int(elapsed_time))  + " seconds")
                                        if(found==False):
                                            print("Error - Timeout ,could not confirm the file.")
                                            self.table_list_of_tuples[link_index()] = (Song_Name_with_pun,"Error - Timeout ,could not confirm the file",link)
                                            self.update_table()
                                            timeoutError = True                                                
                                        break
                                    ##################

                                    for file in os.listdir(dir_path):
                                        ftitle = file
                                        ftitle = ftitle.translate(str.maketrans('', '', string.punctuation))#removes punctuation
                                        if remove(ftitle.lower()).find(remove(Song_Name_without_pun.lower())) > -1:#if file does not exist,then rename it and complete
                                            title = file.title()
                                            if file.endswith("mp3"):
                                                #os.rename(os.path.join(dir_path, file),os.path.join(dir_path,f"{Song_Name_without_pun}.mp3"))
                                                found=True
                                        
                            except:
                                self.table_list_of_tuples[link_index()] = (Song_Name_with_pun,"Error - File name already exists",link)
                                self.update_table()
                            if timeoutError ==False:
                                self.table_list_of_tuples[link_index()] = (Song_Name_with_pun,"Completed",link)
                                self.update_table()
                            driver.switch_to.window(driver.window_handles[1])
                            driver.close()
                            driver.switch_to.window(driver.window_handles[0])
                            

                        if link ==youtube_links[-1]:
                            #after the last song the drive will quite
                            print(f"Last link {link}")
                            print("Quites the driver")
                            self.back_error = False
                            driver.quit()
                            
                        #==============================================================================           
                    
            
                            
                    except:
                        self.table_list_of_tuples[link_index()] = (songName,"Error - Timeout",link)
                        self.update_table()
                        if link ==youtube_links[-1]:
                            #after the last song the drive will quite
                            time.sleep(2)
                            driver.quit()
                    
                    #delete the link from the set
                    try:
                        self.table_list_links.remove(link)
                    except:
                        pass

                    time.sleep(1)  # Sleep for 1 seconds in order to avoid getting blocked by being slower (humanlike behavoir)


        download_songs(youtube_links,driver)




App()#run
