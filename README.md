# Youtube-To-Mp3
>A script which automates the process of downloading Youtube songs via a website.

![Downloading in progress example](https://github.com/MichaelMarkovsky/Youtube-To-Mp3/assets/133515749/9141d69a-a7c3-46a9-8d5e-7f82aca02a54)

## Fetures
- Easy to use
- A simple web automation process
- Download multiple links with a press of a button
- Clean mode, to hide the browser automation

## Overview
This python script uses Selenuim's package in order to automate the web browser and Tkinter's package for the GUI.
#### Inserting the links
After the user pastes the links (link under link) to the interface and inserts them to the table, invalid links wont be inserted by a simple
process of a format check by using Regular Expression.
links are already in the table are being filtered as well.

#### Download the links
On a pressing the download button the scripts checks for the essential drivers (for web automation),
if passed and if there are any links then the download process proceeds.
The scipt automaticly converts a link via a site,then checks if the name the site outputs is already in the download folder,
and proceeds to download there is none..
and then to the NEXT!!

> REMEMBER: You aren't allowed to download material that is copyrighted if you do not have express permission,
> therefore its the user's responsibility for any action!


## Installation
#### 1. For webscraping:
Download and install a specific selenuim version:
```
pip install selenium==4.9.0
```
Download and extract *chromedriver-win64* and *chrome-win64* to the script's folder:
https://googlechromelabs.github.io/chrome-for-testing/

#### 2. For GUI:
Download and install tkinter:
```
pip install tk
```

Download and install a custom version of tkinter(themed):
```
pip install sv-ttk
```
#### Essentials:
- YoutubeConverter.py
- Icon.ico
- chromedriver-win64
- chrome-win64

## License
[MIT License](LICENSE)
