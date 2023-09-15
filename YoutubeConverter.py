from selenium import webdriver#importing a library that will automate the action of openning a web browser
from selenium.webdriver.common.by import By#imports a library that alows us to make specific selections(class,id..)
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#imports for creating the download folder
import os
import sys


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



def Youtube_To_MP3_Download(youtube_link,download_location,file_format):

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
    

        my_element = driver.find_element(By.ID,"txtUrl")#selects an element and stores it as a web element
        my_element.click()
        my_element.send_keys(youtube_link)#"types"

        

        WebDriverWait(driver, 10).until(    
            EC.element_to_be_clickable(
                (By.ID,"btnSubmit")
            )
        )
        my_element = driver.find_element(By.ID,"btnSubmit")
        my_element.click()#Clicks on the Start button


        my_element = driver.find_element(By.ID,"btn192")
        print(my_element)
        my_element.click()#Clicks on the Convert button


        Song_Name = driver.find_element(By.ID,"videoTitle").text.splitlines()[0] #Gets the song TITLE + DURATION as a string, then splits the lines into a list , where the first item is the name and the second is the duration
        print(Song_Name)#Prints the song name


        #Waits 10 seconds untill it find the element if the id=btn192 when it will have the text Download and then the program will proceed
        WebDriverWait(driver, 10).until(    
            EC.text_to_be_present_in_element(
                (By.ID,"btn192"), #the element
                "Download"#expected text
            )
        )

        my_element = driver.find_element(By.ID,"btn192")
        my_element.click()#clicks on the Download button

        

    if (file_format=="mp4"):
        driver.get("https://en1.y2mate.is/w0p8g/youtube-to-mp4.html")#gets into this url(opens this site)

        #timeout:
        driver.implicitly_wait(10)#waits untill finds the elemnt, an x amount of time in order to prevent errors because of slow processes like loading the site,server..its a timeout for all elements


        my_element = driver.find_element(By.ID,"txtUrl")#selects an element and stores it as a web element
        my_element.click()
        my_element.send_keys(youtube_link)#"types"
        my_element = driver.find_element(By.ID,"btnSubmit")
        my_element.click()#Clicks on the Start button

        my_element = driver.find_element(By.ID,"btn22")
        my_element.click()#Clicks on the Convert button


        Song_Name = driver.find_element(By.ID,"videoTitle").text.splitlines()[0] #Gets the song TITLE + DURATION as a string, then splits the lines into a list , where the first item is the name and the second is the duration
        print(Song_Name)#Prints the song name


        #Waits 10 seconds untill it find the element if the id=btn192 when it will have the text Download and then the program will proceed
        WebDriverWait(driver, 10).until(    
            EC.text_to_be_present_in_element(
                (By.ID,"btn22"), #the element
                "Download"#expected text
            )
        )

        my_element = driver.find_element(By.ID,"btn22")
        my_element.click()#clicks on the Download button






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


Youtube_link="https://www.youtube.com/watch?v=8wfTugYicqc"

Youtube_To_MP3_Download(Youtube_link,File_location,File_format)#the youtube link(that you want to download to mp3) and the file location you want the file to be downloaded to( if not given then it will be downloaded to the default location )

