import tkinter as tk
import PyPDF2
import textwrap
import tqdm
from tkinter import filedialog

chunks_width = 50

def split_in_chunks(text):
    chunks = textwrap.wrap(text, chunks_width) 
    return chunks

def summarize_pdf():
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    pdf_file = open(file_path, 'rb')
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    
    text_file = open('file.txt', 'w')
    extracted_text = ""
    for page in tqdm.tqdm(range(len(pdf_reader.pages)), desc='Summarizing PDF'):
        page_content = pdf_reader.pages[page].extract_text()
        extracted_text += page_content
        
    split_text = split_in_chunks(extracted_text)
    for chunk in split_text:
        text_file.write(chunk + '\n')
    
    pdf_file.close()
    text_file.close()
    
root = tk.Tk()
root.title("PDF Summarizer")

summarize_button = tk.Button(root, text="Summarize PDF", command=summarize_pdf)
summarize_button.pack()

root.mainloop()
