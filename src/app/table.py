import os
import pdf2image

def pdftoimg(src):
    # Store all the pages of the PDF in a variable 
    images = pdf2image.convert_from_path(src,500,poppler_path=r'..\assets\poppler-24.02.0\Library\bin')
    for i, image in enumerate(images):
        file = 'image'+str(i)+'.png'
        image.save(file, "PNG")
    

print(pdftoimg('../assets/sample.pdf'))