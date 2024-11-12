# I cannot take credit for a lot in this program, some was taken from this link: https://www.geeksforgeeks.org/python-using-pil-imagegrab-and-pytesseract/
# GitHub copilot was also used heavily.


# cv2.cvtColor takes a numpy ndarray as an argument 
import numpy as nm 

import time

import pytesseract 
# importing OpenCV 
import cv2 
  
from PIL import ImageGrab 
import pyautogui
import re
  
  
def imToString(): 
  
    # Path of tesseract executable 
    pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
    while(True): 
  
        # ImageGrab-To capture the screen image in a loop.  
        # Bbox used to capture a specific area.
        cap = ImageGrab.grab(bbox =(612, 967, 1450, 1226)) 
        # You most likely WILL have to change this value to fit your screen resolution, I have a 2560x1440 monitor so this is the value I used.
        # I used this program: https://sourceforge.net/projects/mpos/
  
        # Converted the image to monochrome for it to be easily  
        # read by the OCR and obtained the output String. 
        tesstr = pytesseract.image_to_string( 
                cv2.cvtColor(nm.array(cap), cv2.COLOR_BGR2GRAY),  
                lang ='eng') 
        print(tesstr) 
        if "to continue playing:" in tesstr:

            # Extract the code after "to continue playing:"
            match = re.search('to continue playing: (\w+)', tesstr)
            if match:
                code = match.group(1)
                # Type out the command and press enter
                pyautogui.typewrite(f"/verify {code}")
                pyautogui.press("enter")
                # In case it didn't work the first time (this happened to me once)
                pyautogui.press("enter")
                time.sleep(2)

        if "Dismiss message" in tesstr:
            # Find the location of the "Dismiss message" text on the screen
            dismiss_location = pyautogui.locateCenterOnScreen("dismiss_message.png", confidence=0.8)
            if dismiss_location:
                # Click on the "Dismiss message" text
                pyautogui.click(dismiss_location)
                time.sleep(2)
                # Teleport the mouse to coordinates 816, 1144. These are the coordinates of the "Farm" button, and will have to change depending on your screen resolution.
                pyautogui.moveTo(816, 1144)

# Calling the function 
imToString() 