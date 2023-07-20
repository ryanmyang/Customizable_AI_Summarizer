from flask import Flask, render_template
from dotenv import load_dotenv
import openai
import os
import io
import datetime
app = Flask(__name__)

log_content = ""

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



# Output

# Write to
def write_gpt_log(filename, text, instructions, transcript):
    filepath = os.path.join("logs", filename)
    with open(filepath, "w") as f:
        f.write(text)
        f.write("\n\n\n\n\n\n-------INSTRUCTIONS--------")
        f.write(instructions)
        f.write("\n\n\n\n\n\n-------TRANSCRIPT--------")
        f.write(transcript)
    return filename


def gpt35_16k(sys, usr):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",  
        messages=[
            {"role": "system", "content": sys},
            {"role": "user", "content": usr}
        ]
        )
    return completion

def gpt35(sys, usr):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  
        messages=[
            {"role": "system", "content": sys},
            {"role": "user", "content": usr}
        ]
        )
    return completion

def main():
    # Load API Key
    load_dotenv()
    openai.api_key = os.getenv('API_KEY')

    ## CONTROLS ##
    chat_on = False
    summary_count = 2
    transcript = read_ref("01_transcript")
    system_instructions = read_message("01_system_topics_no_categories")


    log_time = datetime.datetime.now().strftime("%m-%d-%H-%M-%S")
    if (transcript == None or system_instructions == None):
        print("Input file error")
        quit()

    ### Chat GPT
    responses = list()

    if chat_on:
        for i in range(summary_count):
            responses.append(gpt35_16k(system_instructions, transcript))
            log = write_gpt_log(log_time+"_"+str(i),responses[i]["choices"][0]["message"]["content"])
    else:
        for i in range(summary_count):
            responses.append("Summary Test" + str(i))
            log = write_gpt_log(log_time+"_"+str(i),responses[i], system_instructions, transcript)
    
        
    print(responses)
    # with open(os.path.join("logs", log), "r") as f:
    #     log_content = f.read()

@app.route('/')
def index():
    return "Testing"
    # file_list = get_file_list('logs')
    # menu = create_menu(file_list)
    # return render_template('menu.html', menu=menu)

if __name__ == '__main__':
    main()
    app.run()

