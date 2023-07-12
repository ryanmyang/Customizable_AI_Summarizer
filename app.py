from flask import Flask
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

transcript = read_ref("01_transcript")
system_instructions = read_message("01_system")


### Chat GPT
response = "test"

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

@app.route('/')
def hello():
    return log_content

if __name__ == '__main__':
    app.run()
