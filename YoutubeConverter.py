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

import sv_ttk
import threading
from threading import Event






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

        #run
        self.mainloop()#the loop of the application

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
        
        # self.event = Event()
        # self.Bthread = threading.Thread(target=self.Download)
        # self.Bthread.setDaemon(True)#it will automatically be terminated when the main program exits.

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

        # Create a StringVar to store the button text
        self.button_var = tk.StringVar()
        self.button_var.set("Download!")
        self.download_button = ttk.Button(interface_frame, textvariable=self.button_var, style="Accent.TButton",command=self.Download)
        self.download_button.grid(row=5,column=0,padx=5,pady=7)


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
        self.table_list_of_tuples.clear() 

    def Insert_link(self):
        #delete all the rows of the table inorder to bypass a bug
        self.clear_table()

        links = self.text_widget.get("1.0", tk.END)

        # Remove empty items from the list
        no_empty_links = [item for item in links.splitlines() if item != ""]

        filtered_links = set(no_empty_links)
        
        self.table_list_links.update(filtered_links)

        print(f'self.table_list_links{self.table_list_links}')


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
        print(self.table_list_of_tuples)

        self.text_widget.delete(1.0, tk.END)  # Delete from the start to the end


    def update_table(self):
        #delete all the rows of the table inorder to bypass a bug
        self.clear_table()
        #insert the list of links to the table
        for link in self.table_list_of_tuples:
            self.table.insert('',tk.END,values=(link[0],link[1],link[2]))

    def Download(self):#the youtube link(that you want to download to mp3) and the file location you want the file to be downloaded to( if not given then it will be downloaded to the default location )
        #download the file to the right path due to the format
        
        
        if self.button_var.get() == "Download!":
            self.button_var.set("Stop!")
            def run(event: Event):
                while True:
                    script_directory = f"{os.path.dirname(os.path.abspath(sys.argv[0]))}\downloads"
                    File_location = script_directory          
                    #Example:   "C:\\Users\\misha\\Desktop\\" 

                    Youtube_links = list(self.table_list_links)
                    driverr = self.driver(File_location)
                    self.Youtube_To_MP3_Download(Youtube_links,driverr)#the youtube link(that you want to download to mp3) and the file location you want the file to be downloaded to( if not given then it will be downloaded to the default location )                    
                    if self.event.is_set():
                        print("this event has been stopped prematurely")
                        self.button_var.set("Download!")
                        self.event.clear()
                        break
                    else:
                        print("this event has been stopped maturely")
                        self.button_var.set("Download!")
                        break



            t = threading.Thread(target=run, args=(self.event,))
            t.daemon = True  # Daemon threads are background threads that automatically exit when the main program finishes.
            t.start()
        else:
            self.event.set()
            self.button_var.set("Download!")
        
        print(f'set of links:{self.table_list_links}')
        print(self.table_list_of_tuples)
    
    
    def driver(self,download_location):
        #SETUP
        # these 2 lines make it so that the browser wont close automaticly
        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach", True)

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
        driver.implicitly_wait(10)#waits untill finds the elemnt, an x amount of time in order to prevent errors because of slow processes like loading the site,server..its a timeout for all elements

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
                print(self.event.is_set())
                if self.event.is_set() == True:#if i pressed the button to stop,then stop downloading the links and quite the driver
                    print("quites the driver")
                    driver.quit()
                    return
                else:
                    songName = ''
                    def link_index():#returns the index of the item that has this link in order to add name and status
                            for item in self.table_list_of_tuples:
                                if item[2] == link:
                                    return (self.table_list_of_tuples.index(item))
                    try:
                        print(link)
                        

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

                        
                        print(Song_Name_with_pun)
                        songName +=Song_Name_with_pun
                        #print(Song_Name_without_pun)



                        script_directory = os.path.dirname(os.path.abspath(sys.argv[0])) #give me the path of the script
                        # directory/folder path
                        dir_path = (f"{script_directory}\downloads")
                        dir_list = os.listdir(dir_path)
                        
                        for file in dir_list:
                            #print(f"files in this folder:{file.title()}")
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
                                        print("file exists")
                                        self.table_list_of_tuples[link_index()] = (Song_Name_with_pun,"Error - File exists",link)
                                        self.update_table()


                        if File_Exists == False:
                            WebDriverWait(driver, 10).until(    
                            EC.element_to_be_clickable(
                                (By.XPATH,"/html/body/form/div[2]/a[1]")
                                )
                            )

                            Download_button = driver.find_element(By.XPATH,"/html/body/form/div[2]/a[1]")
                            Download_button.click()#Clicks on the download button



                            
                            ###########checks if the download has been completed
                            #print("Files and directories in '", dir_path, "' :")

                            # prints all files
                            #print(dir_list)

                            timeoutError = False
                            try:                        
                                #timeout system
                                start_time = time.time()
                                seconds = 20


                                found = False
                                while(found==False):
                                    #timeout system
                                    current_time = time.time()
                                    elapsed_time = current_time - start_time

                                    if elapsed_time > seconds:
                                        print("Finished iterating in: " + str(int(elapsed_time))  + " seconds")
                                        if(found==False):
                                            print("Error - Timeout ,could not confirm the file.")
                                            self.table_list_of_tuples[link_index()] = (Song_Name_with_pun,"Error - Timeout ,could not confirm the file.",link)
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
                                print("file name already exists")
                                self.table_list_of_tuples[link_index()] = (Song_Name_with_pun,"Error - File name already exists",link)
                                self.update_table()
                            if timeoutError ==False:
                                print('download has been completed')
                                self.table_list_of_tuples[link_index()] = (Song_Name_with_pun,"Completed",link)
                                self.update_table()
                            driver.switch_to.window(driver.window_handles[1])
                            driver.close()
                            driver.switch_to.window(driver.window_handles[0])


                        if link ==youtube_links[-1]:
                            #after the last song the drive will quite
                            print(f"last item {link}")
                            driver.quit()
                        #==============================================================================           
                    
            
                            
                    except:
                        print("ERROR - timeout")
                        self.table_list_of_tuples[link_index()] = (songName,"Error - timeout",link)
                        self.update_table()
                        if link ==youtube_links[-1]:
                            #after the last song the drive will quite
                            print(f"last item {link}")
                            time.sleep(2)
                            driver.quit()
                    
                    #delete the link from the set
                    self.table_list_links.remove(link)
                    print(f'UPDATED self.table_list_links::{self.table_list_links}')

        download_songs(youtube_links,driver)




App()#run
    

# Youtube_links = ["https://www.youtube.com/watch?v=oSf3Nqd0qnY","https://www.youtube.com/watch?v=4GGIdZidcno&list=RDMM&start_radio=1","https://www.youtube.com/watch?v=335VEasxI2E&list=RDMM&index=4","https://www.youtube.com/watch?v=0YF8vecQWYs","https://www.youtube.com/watch?v=WCOvg2rvzmM"]
# Youtube_links = list(set(Youtube_links))#if the user entered 2 of the same links,then "set" will remove one of them and ill turn this back into a list. this will be the UPDATED list of links that will be in use, the table in the ui will be updated to this.
# print(Youtube_links)

