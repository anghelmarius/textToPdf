import tkinter as tk
import PyPDF2
from tkinter import filedialog
import nltk
nltk.download('punkt')
from nltk.tokenize import sent_tokenize
import openai
import time

# Add your OpenAI API key
openai.api_key = "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"

max_requests_per_minute = 10
time_between_requests = 60 / max_requests_per_minute

def split_in_chunks(text):
    sentences = sent_tokenize(text)
    return sentences


def summarize(prompt, file_name):
    augmented_prompt = f"summarize this text: {prompt}"
    start_time = time.time()
    for i in range(max_requests_per_minute):
        summary = openai.Completion.create(
            engine="text-davinci-002",
            prompt=augmented_prompt,
            temperature=.5,
            max_tokens=1000,
        )["choices"][0]["text"]
        # Store the summary in a file
        with open(file_name, 'a') as f:
            f.write(summary)
        elapsed_time = time.time() - start_time
        if elapsed_time < time_between_requests * (i + 1):
            time.sleep(time_between_requests * (i + 1) - elapsed_time)


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

    for chunk in split_text:
         summarize(chunk + '\n', 'summary.txt')
    
    pdf_file.close()
    raw_text_file.close()
    chunked_text_file.close()
    
   

    
root = tk.Tk()
root.title("PDF Summarizer")

summarize_button = tk.Button(root, text="Summarize PDF", command=summarize_pdf)
summarize_button.pack()

root.mainloop()
