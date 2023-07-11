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

# Chat GPT

response = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",  
  messages=[
    {"role": "system", "content": "You are cricket expert."},
    {"role": "user", "content": "Who won the world cup in 2019?"},
    {"role": "assistant", "content": "England cricket team won the world cup in 2019."},
    {"role": "user", "content": "Who was the opponent?"}
  ]
)
# response = "test"

# Output
def write_to_file(text):
    filename = datetime.datetime.now().strftime("%m-%d-%H-%M-%S")
    filepath = os.path.join("logs", filename)
    with open(filepath, "w") as f:
        f.write(text)

write_to_file(response["choices"][0]["message"]["content"])

@app.route('/')
def hello():
    return response

if __name__ == '__main__':
    app.run()
