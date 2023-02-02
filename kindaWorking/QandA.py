import openai

# Add your OpenAI API key
openai.api_key = "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"

def answer_question(question, file_name):
    augmented_prompt = f"as long as the answer is contained by this data: '{file_name}', reply to {question} only using the information in the data, not from any other sources."
    answer = openai.Completion.create(
        engine="text-davinci-002",
        prompt=augmented_prompt,
        temperature=.3,
        max_tokens=1000,
    )["choices"][0]["text"]
    return answer


def ask_question():
    question = input("Type: ")
    answer = answer_question(question, 'summary.txt')
    print("Answer: " + answer)

    # Log the question and answer
    with open("qa_log.txt", "a") as log_file:
        log_file.write("Question: " + question + "\n")
        log_file.write("Answer: " + answer + "\n")
        log_file.write("\n")

while True:
    ask_question()
