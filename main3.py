import tkinter as tk
import PyPDF2
from tkinter import filedialog
import nltk
nltk.download('punkt')
from nltk.tokenize import sent_tokenize
import openai

chunks_width = 50

def split_in_chunks(text):
    sentences = sent_tokenize(text)
    return sentences


def summarize(prompt):
    augmented_prompt = f"summarize this text: {prompt}"
    summary = openai.Completion.create(
        model="text-davinci-003",
        prompt=augmented_prompt,
        temperature=.5,
        max_tokens=1000,
    )["choices"][0]["text"]


def summarize_pdf():
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    pdf_file = open(file_path, 'rb')
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    
    raw_text_file = open('raw_text.txt', 'w')
    extracted_text = ""
    for page in range(len(pdf_reader.pages)):
        page_content = pdf_reader.pages[page].extract_text()
        extracted_text += page_content
        
    raw_text_file.write(extracted_text)
    
    split_text = split_in_chunks(extracted_text)
    chunked_text_file = open('chunked_text.txt', 'w')
    for chunk in split_text:
        chunked_text_file.write(chunk + '\n')
    
    pdf_file.close()
    raw_text_file.close()
    chunked_text_file.close()


    augmented_prompt = f"as long as the answer is contained by this data: '{test_knowledge_base}', reply to '{prompt}', only using the information in the data."

    
root = tk.Tk()
root.title("PDF Summarizer")

summarize_button = tk.Button(root, text="Summarize PDF", command=summarize_pdf)
summarize_button.pack()

root.mainloop()
