import os
import pdf2image
import pytesseract
from PIL import Image
import cv2

dirname = os.path.dirname(__file__)
pytesseract.pytesseract.tesseract_cmd = os.path.join(dirname, 'libraries\Tesseract-OCR\\tesseract.exe')

def pdf_to_img(pdf, output):
    # Store all the pages of the PDF in a variable 
    images = pdf2image.convert_from_bytes(pdf,500, poppler_path=os.path.join(dirname, 'libraries\poppler-24.02.0\Library\\bin'))
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

def text_to_csv(text, file_name, output):
    if file_name != '':
        if len(file_name) < 4 or file_name[-4:] != '.csv':
            file_name += '.csv'
        file = open(output+file_name, 'w')
        file.write(text)
        file.close()
    else:
        print('Please enter a file name')

def process_pdf(pdf):
    output_folder = os.path.join(dirname, 'temp_files\\')

    # clear out temp_files folder
    for file in os.listdir(output_folder):
        if os.path.isfile(output_folder + file):
            os.unlink(output_folder + file)

    filename, extension = os.path.splitext(pdf.name)
    if extension == '.pdf': pdf_to_img(pdf.read(), output_folder)

    text = ''
    for image in os.listdir(output_folder):
        if (image.endswith('.png')):
            transformed_img = cv2.imread(output_folder + image)
            transformed_img = convert_grayscale(transformed_img)
            transformed_img = thresholding(transformed_img)
            transformed_img = remove_noise(transformed_img)
            text += img_to_text(transformed_img)
    text_to_csv(text, 'file2.csv', output_folder)
            
    