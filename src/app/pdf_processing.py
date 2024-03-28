import os
import pdf2image
import pytesseract
from PIL import Image
import cv2

pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
def pdf_to_img(src, output):
    # Store all the pages of the PDF in a variable 
    images = pdf2image.convert_from_path(src,500, poppler_path=r'..\assets\poppler-24.02.0\Library\bin')
    for i, image in enumerate(images):
        file = 'image'+str(i)+'.png'
        image.save(output+file, "PNG")

def convert_grayscale(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def thresholding(img):
    return cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

def remove_noise(img):
    return cv2.medianBlur(img, 5)

def img_to_text(img):
    text = pytesseract.image_to_string(img, config='--psm 6 oem=3 -l eng')
    # the config option --psm 6 is CRUCIAL in order to properly 
    # extract data from the table. Page Segmentation Mode 6 
    # treats the image as a uniform block of text which works
    # well for tabular data. 
    return text     

def text_to_csv(text, file_name):
    if file_name != '':
        if len(file_name) < 4 or file_name[-4:] != '.csv':
            file_name += '.csv'
        file = open('../assets/temp_storage/'+file_name, 'w')
        file.write(text)
        file.close()
    else:
        print('Please enter a file name')

# pdf_to_img('../assets/sample.pdf', '../assets/temp_storage/')
img = cv2.imread('../assets/temp_storage/image0.png')
img = convert_grayscale(img)
img = thresholding(img)
img = remove_noise(img)
# cv2.imwrite("new.png", img)
# print(img_to_text(img))
text = img_to_text(img)
text_to_csv(text, 'file.csv')