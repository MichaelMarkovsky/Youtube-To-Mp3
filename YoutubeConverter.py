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

def create_download_folder_if_not_exists():
    script_directory = os.path.dirname(os.path.abspath(sys.argv[0])) #give me the path of the script


    # checking if the directory downloads 
    # exist or not.
    if not os.path.exists(f"{script_directory}\downloads"):
        # if the downloads directory is not present 
        # then create it.
        os.makedirs(f"{script_directory}\downloads")

        #create subfolders
        os.makedirs(f"{script_directory}\downloads\mp3")
        os.makedirs(f"{script_directory}\downloads\mp4")



def Youtube_To_MP3_Download(youtube_links,download_location,file_format):

    # these 2 lines make it so that the browser wont close automaticly
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)

    if (download_location!= None):#if ive given a file location then proceed, else download the file to the default folder(which is the "Download" folder)
        #Change the default download location
        prefs = {'download.default_directory': download_location}
        options.add_experimental_option('prefs', prefs)


    driver = webdriver.Chrome(options=options)#open the browser

    
    if (file_format=="mp3"):
        driver.get("https://en1.y2mate.is/w0p8g/youtube-to-mp3.html")#gets into this url(opens this site)

        #timeout:
        driver.implicitly_wait(10)#waits untill finds the elemnt, an x amount of time in order to prevent errors because of slow processes like loading the site,server..its a timeout for all elements
    
        ##########inserting the first song so that the process will be shorter for this site##############
        Textbox_element = driver.find_element(By.ID,"txtUrl")#selects an element and stores it as a web element
        Textbox_element.click()
        Textbox_element.send_keys("https://www.youtube.com/watch?v=3zh9Wb1KuW8&list=RDMM&index=3")#"types"

        

        WebDriverWait(driver, 10).until(    
            EC.element_to_be_clickable(
                (By.ID,"btnSubmit")
            )
        )
        Start_button = driver.find_element(By.ID,"btnSubmit")
        Start_button.click()#Clicks on the Start button

        WebDriverWait(driver, 10).until(    
            EC.element_to_be_clickable(
                (By.ID,"btn192")
            )
        )
        Textbox_element.clear()
        #######################################################################################################

        def download_songs(youtube_links):
            for link in youtube_links:
                try:
                    print(link)

                    Textbox_element = driver.find_element(By.ID,"txtUrl")#selects an element and stores it as a web element
                    Textbox_element.clear()
                    Textbox_element.click()
                    Textbox_element.send_keys(link)#"types"


                    WebDriverWait(driver, 10).until(    
                        EC.element_to_be_clickable(
                            (By.ID,"btnSubmit")
                        )
                    )
                    Start_button = driver.find_element(By.ID,"btnSubmit")
                    Start_button.click()#Clicks on the Start button


                    WebDriverWait(driver, 10).until(    
                    EC.element_to_be_clickable(
                        (By.ID,"btn192")
                        )
                    )

                    Convert_button = driver.find_element(By.ID,"btn192")
                    Convert_button.click()#Clicks on the Convert button


                    Song_Name_with_pun = driver.find_element(By.ID,"videoTitle").text.splitlines()[0] #Gets the song TITLE + DURATION as a string, then splits the lines into a list , where the first item is the name and the second is the duration
                    Song_Name_without_pun = Song_Name_with_pun        
                            # initializing punctuations string
                    punc = '''!()-[]{};:'"\,<>./?@#$%^&*_~」「+'''
                    
                    # Removing punctuations in string
                    # Using loop + punctuation string
                    for ele in Song_Name_without_pun:
                        if ele in punc:
                            Song_Name_without_pun = Song_Name_without_pun.replace(ele, "")

                    
                    print(Song_Name_with_pun)
                    print(Song_Name_without_pun)


                    #Waits 10 seconds untill it find the element if the id=btn192 when it will have the text Download and then the program will proceed
                    WebDriverWait(driver, 10).until(    
                        EC.text_to_be_present_in_element(
                            (By.ID,"btn192"), #the element
                            "Download"#expected text
                        )
                    )

                    Download_button = driver.find_element(By.ID,"btn192")
                    Download_button.click()#clicks on the Download button



                    ###########Renames the file to be user friendly + checks if the download has been completed
                    script_directory = os.path.dirname(os.path.abspath(sys.argv[0])) #give me the path of the script
                    # directory/folder path
                    dir_path = (f"{script_directory}\downloads\mp3")

                    dir_list = os.listdir(dir_path)
                    print("Files and directories in '", dir_path, "' :")

                    # prints all files
                    print(dir_list)


                    #code to remove whitespace
                    def remove(string):
                        return string.replace(" ", "")

                    
                    try:                        
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
                

                        found = False
                        while(found==False):
                            for file in os.listdir(dir_path):
                                ftitle = file
                                ftitle = ftitle.translate(str.maketrans('', '', string.punctuation))#removes punctuation
                                if remove(ftitle.lower()).find(remove(Song_Name_without_pun.lower())) > -1:#if file does not exist,then rename it and complete
                                    title = file.title()
                                    if file.endswith("mp3"):
                                        os.rename(os.path.join(dir_path, file),os.path.join(dir_path,f"{Song_Name_without_pun}.mp3"))
                                        found=True
                                
                                        
                    except:
                        print("file name already exists")

                    print('download has been completed')
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
                    if link ==youtube_links[-1]:
                        #after the last song the drive will quite
                        print(f"last item {link}")
                        driver.quit()

        download_songs(youtube_links)

    if (file_format=="mp4"):
        driver.get("https://en1.y2mate.is/w0p8g/youtube-to-mp4.html")#gets into this url(opens this site)

        #timeout:
        driver.implicitly_wait(10)#waits untill finds the elemnt, an x amount of time in order to prevent errors because of slow processes like loading the site,server..its a timeout for all elements


        Textbox_element = driver.find_element(By.ID,"txtUrl")#selects an element and stores it as a web element
        Textbox_element.click()
        Textbox_element.send_keys(youtube_link)#"types"


        WebDriverWait(driver, 10).until(    
            EC.element_to_be_clickable(
                (By.ID,"btnSubmit")
            )
        )
        Start_button = driver.find_element(By.ID,"btnSubmit")
        Start_button.click()#Clicks on the Start button



        Convert_button = driver.find_element(By.ID,"btn22")
        Convert_button.click()#Clicks on the Convert button


        Song_Name_with_pun = driver.find_element(By.ID,"videoTitle").text.splitlines()[0] #Gets the song TITLE + DURATION as a string, then splits the lines into a list , where the first item is the name and the second is the duration
        Song_Name_without_pun = Song_Name_with_pun        
                # initializing punctuations string
        punc = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
        
        # Removing punctuations in string
        # Using loop + punctuation string
        for ele in Song_Name_without_pun:
            if ele in punc:
                Song_Name_without_pun = Song_Name_without_pun.replace(ele, "")

        
        print(Song_Name_with_pun)
        print(Song_Name_without_pun)


        #Waits 10 seconds untill it find the element if the id=btn192 when it will have the text Download and then the program will proceed
        WebDriverWait(driver, 10).until(    
            EC.text_to_be_present_in_element(
                (By.ID,"btn22"), #the element
                "Download"#expected text
            )
        )

        Download_button = driver.find_element(By.ID,"btn22")
        Download_button.click()#clicks on the Download button



        ###########Renames the file to be user friendly + checks if the download has been completed
        script_directory = os.path.dirname(os.path.abspath(sys.argv[0])) #give me the path of the script
        # directory/folder path
        dir_path = (f"{script_directory}\downloads\mp4")

        dir_list = os.listdir(dir_path)
        print("Files and directories in '", dir_path, "' :")

        # prints all files
        print(dir_list)


        #code to remove whitespace
        def remove(string):
            return string.replace(" ", "")


        try:
            found = False
            while(found==False):
                for file in os.listdir(dir_path):
                    if remove(file).find(remove(Song_Name_with_pun)) > -1:
                        title = file.title()
                        #print(f'title -{title}')
                        if file.endswith("mp4"):
                            os.rename(os.path.join(dir_path, file),os.path.join(dir_path,f"{Song_Name_with_pun}.mp4"))
                            found=True
        except:
            print("file name already exists")

        print('download has been completed')
        #==============================================================================









create_download_folder_if_not_exists()

#================
File_format="mp3"
#================

#download the file to the right path due to the format
if File_format == "mp3":
    script_directory = f"{os.path.dirname(os.path.abspath(sys.argv[0]))}\downloads\mp3"
    File_location = script_directory          
    #Example:   "C:\\Users\\misha\\Desktop\\" 
if File_format == "mp4":
    script_directory = f"{os.path.dirname(os.path.abspath(sys.argv[0]))}\downloads\mp4"
    File_location = script_directory         

# Youtube_links=[]

# with open("links.txt") as file:
#   for item in file:
#     Youtube_links.append(item.strip())
#     print(item.strip())

Youtube_links = ["https://www.youtube.com/watch?v=oSf3Nqd0qnY","https://www.youtube.com/watch?v=4GGIdZidcno&list=RDMM&start_radio=1","https://www.youtube.com/watch?v=335VEasxI2E&list=RDMM&index=4","https://www.youtube.com/watch?v=0YF8vecQWYs","https://www.youtube.com/watch?v=WCOvg2rvzmM"]
Youtube_links = list(set(Youtube_links))#if the user entered 2 of the same links,then "set" will remove one of them and ill turn this back into a list. this will be the UPDATED list of links that will be in use, the table in the ui will be updated to this.
print(Youtube_links)


Youtube_To_MP3_Download(Youtube_links,File_location,File_format)#the youtube link(that you want to download to mp3) and the file location you want the file to be downloaded to( if not given then it will be downloaded to the default location )

