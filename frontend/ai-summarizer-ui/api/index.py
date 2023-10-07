from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import openai
import os
import io
import datetime
from ._utils.firebase_utils import add_data, get_data, set_data
# comment
app = Flask(__name__)

MODELS = ['gpt-3.5-turbo', 'gpt-3.5-turbo-16k']

def completion_text(c):
    return c["choices"][0]["message"]["content"]

def write_gpt_log(filename, response, instructions, transcript):
    instructions = "" if instructions is None else instructions
    output = ''
    output+=response
    output+="\n\n\n\n\n\n-------SYSTEM--------\n"
    output+=instructions
    output+="\n\n\n\n\n\n-------USER--------\n"
    output+=transcript
    add_data('logs',{'output': output})


#region Random Helper Functions
def read_ref(file):
    filepath = os.path.join("backend", "refs", file)
    with open(filepath, "r") as f:
        output = f.read()
    return output
def read_message(file):
    filepath = os.path.join("messages", file)
    with open(filepath, "r") as f:
        output = f.read()
    return output
#endregion

def gpt(model_num, sys,usr, log_name):
    print('GPT Called: ' + MODELS[model_num])

    if sys is not None:
        completion = openai.ChatCompletion.create(
            model=MODELS[model_num],  
            messages=[
                {"role": "system", "content": sys},
                {"role": "user", "content": usr}
            ]
            )
    else: 
        completion = openai.ChatCompletion.create(
            model=MODELS[model_num],  
            messages=[
                {"role": "user", "content": usr}
            ]
            )
    write_gpt_log(log_name, completion_text(completion), sys, usr)
    return completion

@app.route('/api')
def home():
    load_dotenv()
    system = read_message('01_system')

    openai.api_key = os.getenv('API_KEY')
    add_data("test",{"Test": "Value"})
    response = completion_text(gpt(0, "You are a summarizer. Summarizer whatever you see, whether it be a question or document", system, "lognameirrelevant"))
    add_data("test", {"conversion_result":response})
    return jsonify({'message': 'Job starting', 'response':system})

@app.route('/api/openai')
def about():
    return jsonify({'message': 'OpenAI Test'})