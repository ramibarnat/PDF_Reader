import PyPDF2

def read_pdf(src):
    with open(src, 'rb') as pdf_file:
        pdf = PyPDF2.PdfReader(pdf_file)
        text = ''
        for page in pdf.pages:
            text += page.extract_text()
    return text

print(read_pdf('../assets/sample.pdf'))