from pyautogui import *
from PIL import Image, ImageEnhance
import pytesseract
import pyautogui
import time
import keyboard
import random
import win32api, win32con


iml = pyautogui.screenshot(region=(200,200,500,600))
iml.save(r"C:\Users\danie\OneDrive\Desktop\Hackathon\captchaCode.png")
try:
    img = Image.open('captchaCode.png')

except TesseractNotFoundError:
    print("Error")

enhancer1 = ImageEnhance.Sharpness(img)
enhancer2 = ImageEnhance.Contrast(img)

img_edit = enhancer1.enhance(20.0)
img_edit = enhancer2.enhance(1.5)

img_edit.save("edited_image.png")

result = pytesseract.image_to_string(img_edit)

with open('text_result.txt', mode ='w') as file:
    file.write(result)
    print("ready!")
