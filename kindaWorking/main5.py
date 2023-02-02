import tkinter as tk
import PyPDF2
from tkinter import filedialog
import nltk
import openai
import time

# Add your OpenAI API key
openai.api_key = "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"

max_requests_per_minute = 10
time_between_requests = 60 / max_requests_per_minute

# Download the punkt tokenizer
nltk.download('punkt')
from nltk.tokenize import sent_tokenize

def split_in_chunks(text):
    """
    Splits text into chunks based on sentence tokenization.
    """
    sentences = sent_tokenize(text)
    return sentences

def write_to_file(file_name, text):
    """
    Writes the given text to the specified file.
    """
    with open(file_name, 'a') as f:
        f.write(text)

def summarize(prompt, file_name):
    """
    Summarizes the given prompt and writes the summary to the specified file.
    """
    augmented_prompt = f"summarize this text: {prompt}"
    start_time = time.time()
    for i in range(max_requests_per_minute):
        summary = openai.Completion.create(
            engine="text-davinci-002",
            prompt=augmented_prompt,
            temperature=.5,
            max_tokens=1000,
        )["choices"][0]["text"]
        write_to_file(file_name, summary)
        elapsed_time = time.time() - start_time
        if elapsed_time < time_between_requests * (i + 1):
            time.sleep(time_between_requests * (i + 1) - elapsed_time)

def summarize_pdf():
    """
    Summarizes the content of a selected PDF file and writes the summary to a file.
    """
    # Get the file path of the selected PDF file
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    pdf_file = open(file_path, 'rb')
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    
    # Extract text from the PDF and write it to a file
    extracted_text = ""
    for page in range(len(pdf_reader.pages)):
        page_content = pdf_reader.pages[page].extract_text()
        extracted_text += page_content
    write_to_file('raw_text.txt', extracted_text)
    
    # Split the extracted text into chunks and write each chunk to a file
    split_text = split_in_chunks(extracted_text)
    for chunk in split_text:
        write_to_file('chunked_text.txt', chunk + '\n')
    
    # Summarize each chunk of text and write the summary to a file
    for chunk in split_text:
        summarize(chunk + '\n', 'summary.txt')

    with open("summary.txt", "r") as f:
        text = f.read()

    for chunk in text:
        summarize(chunk + '\n', 'summary_again.txt')

    # Close the opened files
    pdf_file.close()

# GUI setup
root = tk.Tk()
root.title("PDF Summarizer")

summarize_button = tk.Button(root, text="Summarize PDF", command=summarize_pdf)
summarize_button.pack()

root.mainloop()
