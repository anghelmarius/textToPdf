import tkinter as tk
import PyPDF2
from tkinter import filedialog
import textwrap

chunks_width = 50

def split_in_chunks(text):
    chunks = textwrap.wrap(text, chunks_width) 
    return chunks

def summarize_pdf():
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    pdf_file = open(file_path, 'rb')
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    
    for page in range(len(pdf_reader.pages)):
        page_content = pdf_reader.pages[page].extract_text()
        text += page_content
    
    pdf_file.close()
    
    chunks = split_in_chunks(text)
    
    with open('file.txt', 'w') as text_file:
        for chunk in chunks:
            text_file.write(chunk + "\n")

root = tk.Tk()
root.title("PDF Summarizer")

summarize_button = tk.Button(root, text="Summarize PDF", command=summarize_pdf)
summarize_button.pack()

root.mainloop()
