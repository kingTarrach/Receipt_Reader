from PIL import Image, ImageEnhance
import pytesseract


img = Image.open('/home/danielcalle/HackathonSpring2024/Receipt_Reader/receiptTest_difficult.png')

enhancer1 = ImageEnhance.Sharpness(img)
enhancer2 = ImageEnhance.Contrast(img)

img_edit = enhancer1.enhance(20.0)
img_edit = enhancer2.enhance(1.5)

img_edit.save("edited_image_difficult.png")

result = pytesseract.image_to_string(img_edit)

with open('/home/danielcalle/HackathonSpring2024/Receipt_Reader/text_result3.txt', mode ='w') as file:
    file.write(result)
    print("ready!")
