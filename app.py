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

def gpt4(sys, usr):
    print('GPT 4 Turbo Called')
    completion = openai.ChatCompletion.create(
        model="gpt-4",  
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


    ####################
    ##### CONTROLS #####
    ####################

    chat_on = True
    summary_count = 3
    combine_count = 2

    transcript = read_ref("micron_transcript")
    system_instructions = read_message("01_system_topics_no_categories")
    combine_sys = read_message("01_system_combine")
    sort_sys = read_message("01_system_sort")

    ####################
    ####################
    ####################


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
        last_combined = all_responses
        for i in range(combine_count):
            prev_combined = last_combined
            # GPT CALL
            last_combined = completion_text(gpt35(combine_sys, last_combined))
            write_gpt_log(log_time+"_c_"+str(i),last_combined, combine_sys, prev_combined)

        ### Sorted
        ## GPT CALL
        sorted = gpt35(sort_sys,last_combined)
        write_gpt_log(log_time+"_s",completion_text(sorted), sort_sys, last_combined)


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

    all_responses = read_ref("micron_all_responses")
    ### Combine
    combine_sys = read_message("01_system_combine")
    ## GPT CALL
    no_dupes = gpt35(combine_sys, all_responses)
    write_gpt_log(log_time+"_c_test",completion_text(no_dupes), combine_sys, all_responses)
    ## GPT CALL
    # Combine 2
    no_dupes2 = gpt35(combine_sys, completion_text(no_dupes))
    write_gpt_log(log_time+"_c_test_2",completion_text(no_dupes2), combine_sys, completion_text(no_dupes))

    ### Sorted
    sort_sys = read_message("01_system_sort")
    ## GPT CALL
    sorted = gpt35(sort_sys,completion_text(no_dupes2))
    write_gpt_log(log_time+"_s_test",completion_text(sorted), sort_sys, completion_text(no_dupes2))

def test_gpt4():
    load_dotenv()
    openai.api_key = os.getenv('API_KEY')

    log_time = datetime.datetime.now().strftime("%m-%d-%H-%M-%S")
    response = gpt4("", "Hello there, what model are you?")
    write_gpt_log(log_time+"_gpt4_test",completion_text(response), "", "Hello there, what model are you?")
    print(completion_text(response))

def test_gpt35_16K():
    load_dotenv()
    openai.api_key = os.getenv('API_KEY')

    log_time = datetime.datetime.now().strftime("%m-%d-%H-%M-%S")
    usr = read_message('35_test_usr')
    response = gpt35_16k("", usr)
    write_gpt_log(log_time+"_gpt35_test",completion_text(response), "", usr)
    print(completion_text(response))

@app.route('/')
def index():
    return "Testing"
    # file_list = get_file_list('logs')
    # menu = create_menu(file_list)
    # return render_template('menu.html', menu=menu)

if __name__ == '__main__':
    main()
    app.run()

