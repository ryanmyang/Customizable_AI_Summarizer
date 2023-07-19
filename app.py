from flask import Flask, render_template
from dotenv import load_dotenv
import openai
import os
import io
import datetime
app = Flask(__name__)

# Load API Key
load_dotenv()
openai.api_key = os.getenv('API_KEY')

# Input
def read_ref(file):
    filepath = os.path.join("logs", "refs", file)
    with open(filepath, "r") as f:
        output = f.read()
    return output
def read_message(file):
    filepath = os.path.join("messages", file)
    with open(filepath, "r") as f:
        output = f.read()
    return output

## CONTROLS ##
chat_on = True
transcript = read_ref("01_transcript")
system_instructions = read_message("01_system_topics")


### Chat GPT
response = "test"

if chat_on:
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo-16k",  
    messages=[
        {"role": "system", "content": system_instructions},
        {"role": "user", "content": transcript}
    ]
    )

# response = openai.ChatCompletion.create(
#   model="gpt-3.5-turbo",  
#   messages=[
#     {"role": "system", "content": "You are an expert in summarizing earnings call transcripts for use by businesses. you provide a summary of parts. 1. An overview in concise paragraph form with the most important, impactful information, explained in a way that emphasizes "},
#     {"role": "user", "content": "Who won the world cup in 2019?"},
#     {"role": "assistant", "content": "England cricket team won the world cup in 2019."},
#     {"role": "user", "content": "Who was the opponent?"}
#   ]
# )



# Output

# Write to
def write_log(text):
    filename = datetime.datetime.now().strftime("%m-%d-%H-%M-%S")
    filepath = os.path.join("logs", filename)
    with open(filepath, "w") as f:
        f.write(text)
        f.write("\n\n\n\n\n\n-------INSTRUCTIONS--------")
        f.write(system_instructions)
        f.write("\n\n\n\n\n\n-------TRANSCRIPT--------")
        f.write(transcript)
    return filename

# Write to log
if (type(response) is str):
    log = write_log(response)
else:
    log = write_log(response["choices"][0]["message"]["content"])


print(response)
log_content=""
with open(os.path.join("logs", log), "r") as f:
    log_content = f.read()

def get_file_list(directory):
    """Returns a list of all the files in the directory."""
    file_list = []
    for file in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, file)):
            file_list.append(file)
    return file_list

def create_menu(file_list):
    """Creates a menu with a link for each file in the list."""
    menu = ""
    for file in file_list:
        menu += f"<a href='{file}'>{file}</a>"
    return menu

def redirect_to_file(file):
    """Redirects the user to the file's contents."""
    return f"/file/{file}"

@app.route('/')
def index():
    return log_content
    # file_list = get_file_list('logs')
    # menu = create_menu(file_list)
    # return render_template('menu.html', menu=menu)

if __name__ == '__main__':
    app.run()
