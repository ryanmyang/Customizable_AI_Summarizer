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
def write_gpt_log(filename, response, instructions, transcript):
    filepath = os.path.join("logs", filename)
    with open(filepath, "w") as f:
        f.write(response)
        f.write("\n\n\n\n\n\n-------SYSTEM--------\n")
        f.write(instructions)
        f.write("\n\n\n\n\n\n-------USER--------\n")
        f.write(transcript)
    return len(response.splitlines())


def gpt35_16k(sys, usr):
    print('GPT 3.5 Turbo 16K Called')
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",  
        messages=[
            {"role": "system", "content": sys},
            {"role": "user", "content": usr}
        ]
        )
    return completion

def gpt35(sys, usr):
    print('GPT 3.5 Turbo Called')
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  
        messages=[
            {"role": "system", "content": sys},
            {"role": "user", "content": usr}
        ]
        )
    return completion

def completion_text(c):
    return c["choices"][0]["message"]["content"]

def main():
    # Load API Key
    load_dotenv()
    openai.api_key = os.getenv('API_KEY')

    ## CONTROLS ##
    chat_on = True
    summary_count = 3
    transcript = read_ref("micron_transcript")
    system_instructions = read_message("01_system_topics_no_categories")


    log_time = datetime.datetime.now().strftime("%m-%d-%H-%M-%S")

    if (transcript == None or system_instructions == None):
        print("Input file error")
        quit()

    ### Chat GPT
    responses = list()

    ## First Grab out the points multiple times
    if chat_on:
        all_responses = ""
        ### Grab out points a few times
        for i in range(summary_count):

            ## GPT CALL
            responses.append(gpt35_16k(system_instructions, transcript))
            all_responses += completion_text(responses[i]) + '\n'
            log = write_gpt_log(log_time+"_"+str(i),completion_text(responses[i]), system_instructions, transcript)


        ### Combine
        combine_sys = read_message("01_system_combine")
        ## GPT CALL
        no_dupes = gpt35(combine_sys, all_responses)
        write_gpt_log(log_time+"_c",completion_text(no_dupes), combine_sys, all_responses)

        ### Sorted
        sort_sys = read_message("01_system_sort")
        ## GPT CALL
        sorted = gpt35(sort_sys,completion_text(no_dupes))
        write_gpt_log(log_time+"_s",completion_text(sorted), sort_sys, completion_text(no_dupes))


    else:
        for i in range(summary_count):
            responses.append("Summary Test" + str(i))
            log = write_gpt_log(log_time+"_"+str(i),responses[i], system_instructions, transcript)

    ## Then loop through the logs, pull out responses, and combine
    
    ## Then sort
    
        
    print(responses)
    # with open(os.path.join("logs", log), "r") as f:
    #     log_content = f.read()

def test_c_s():
    # Load API Key
    load_dotenv()
    openai.api_key = os.getenv('API_KEY')

    log_time = datetime.datetime.now().strftime("%m-%d-%H-%M-%S")

    ### Chat GPT
    responses = list()

    ## First Grab out the points multiple times

    all_responses = read_ref("micron__all_responses")
    ### Combine
    combine_sys = read_message("01_system_combine")
    ## GPT CALL
    no_dupes = gpt35(combine_sys, all_responses)
    write_gpt_log(log_time+"_c",completion_text(no_dupes), combine_sys, all_responses)

    ### Sorted
    sort_sys = read_message("01_system_sort")
    ## GPT CALL
    sorted = gpt35(sort_sys,completion_text(no_dupes))
    write_gpt_log(log_time+"_s",completion_text(sorted), sort_sys, completion_text(no_dupes))



@app.route('/')
def index():
    return "Testing"
    # file_list = get_file_list('logs')
    # menu = create_menu(file_list)
    # return render_template('menu.html', menu=menu)

if __name__ == '__main__':
    test_c_s()
    app.run()

