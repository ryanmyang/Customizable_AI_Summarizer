from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import openai
import os
import io
import datetime
from firebase_utils import add_data, get_data, set_data
# from celery import Celery


# celery = Celery(
#     'tasks',
#     broker='redis://localhost:6379/0',  # Replace with your broker URL
#     backend='rpc'  # You can change this backend based on your needs
# )

app = Flask(__name__)

log_content = ""
MODELS = ['gpt-3.5-turbo', 'gpt-3.5-turbo-16k']

# Input
def read_ref(file):
    filepath = os.path.join("backend", "refs", file)
    with open(filepath, "r") as f:
        output = f.read()
    return output
def read_message(file):
    filepath = os.path.join("backend", "messages", file)
    with open(filepath, "r") as f:
        output = f.read()
    return output

# @app.route('/api/test-api')
# def test_api():
#     return jsonify({"response": "Test API"})

@app.route('/api/start-job', methods=['POST'])
def start_job():
    uid = request.headers.get('Authorization')[7:]  # Remove 'Bearer ' from the token

    data = request.json
    doc_id = data['doc_id']
    extractions = data['extractions']
    combinations = data['combinations']
    # Construct the data to be added to Firestore


    firestore_data = {
        'doc_id': doc_id,
        'extractions': extractions,
        'combinations': combinations,
        'body': 'processing'
    }

    # Use add_data to add the document to the Firestore collection
    path = f'users/{uid}/summaries'
    summary_doc_ref = add_data(path, firestore_data)
    transcript = get_data(f'users/{uid}/files',doc_id)
    
    task = process.delay(uid, summary_doc_ref, transcript, extractions, combinations)

    return jsonify({'message': 'Job starting'})
# Output

# Write to
def write_gpt_log(filename, response, instructions, transcript):
    filepath = os.path.join("backend","logs", filename)
    instructions = "" if instructions is None else instructions
    with open(filepath, "w") as f:
        f.write(response)
        f.write("\n\n\n\n\n\n-------SYSTEM--------\n")
        f.write(instructions)
        f.write("\n\n\n\n\n\n-------USER--------\n")
        f.write(transcript)
    return len(response.splitlines())

#region Old GPT Functions
# def gpt35_16k(sys, usr):
#     print('GPT 3.5 Turbo 16K Called')
#     completion = openai.ChatCompletion.create(
#         model="gpt-3.5-turbo-16k",  
#         messages=[
#             {"role": "system", "content": sys},
#             {"role": "user", "content": usr}
#         ]
#         )
#     return completion

# def gpt35(sys, usr):
#     print('GPT 3.5 Turbo Called')
#     completion = openai.ChatCompletion.create(
#         model="gpt-3.5-turbo",  
#         messages=[
#             {"role": "system", "content": sys},
#             {"role": "user", "content": usr}
#         ]
#         )
#     return completion

# def gpt4(sys, usr):
#     print('GPT 4 Turbo Called')
#     completion = openai.ChatCompletion.create(
#         model="gpt-4",  
#         messages=[
#             {"role": "system", "content": sys},
#             {"role": "user", "content": usr}
#         ]
#         )
#     return completion
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

def completion_text(c):
    return c["choices"][0]["message"]["content"]

# def test_c_s():
#     # Load API Key
#     load_dotenv()
#     openai.api_key = os.getenv('API_KEY')

#     log_time = datetime.datetime.now().strftime("%m-%d-%H-%M-%S")

#     ### Chat GPT
#     responses = list()

#     ## First Grab out the points multiple times

#     all_responses = read_ref("micron_all_responses")
#     ### Combine
#     combine_sys = read_message("01_system_combine")
#     ## GPT CALL
#     no_dupes = gpt(0,combine_sys, all_responses,'_c_test')
#     ## GPT CALL
#     # Combine 2
#     no_dupes2 = gpt35(combine_sys, completion_text(no_dupes))
#     write_gpt_log(log_time+"_c_test_2",completion_text(no_dupes2), combine_sys, completion_text(no_dupes))

#     ### Sorted
#     sort_sys = read_message("01_system_sort")
#     ## GPT CALL
#     sorted = gpt35(sort_sys,completion_text(no_dupes2))
#     write_gpt_log(log_time+"_s_test",completion_text(sorted), sort_sys, completion_text(no_dupes2))

# def test_gpt4():
#     load_dotenv()
#     openai.api_key = os.getenv('API_KEY')

#     log_time = datetime.datetime.now().strftime("%m-%d-%H-%M-%S")
#     response = gpt4("", "Hello there, what model are you?")
#     write_gpt_log(log_time+"_gpt4_test",completion_text(response), "", "Hello there, what model are you?")
#     print(completion_text(response))

# def test_gpt35_16K():
#     load_dotenv()
#     openai.api_key = os.getenv('API_KEY')

#     log_time = datetime.datetime.now().strftime("%m-%d-%H-%M-%S")
#     usr = read_ref('jpmorgan_cv')
#     response = gpt(1,"You are a helpful bot that takes in information about a job and person to write a cover letter based on past provided examples.", usr, log_time+'_test35')
#     print(completion_text(response))


def process(sum_ref, transcript, extraction_count, combine_count):
    print("\n\n\n STARTING PROCESS \n\n\n")
    # Load API Key
    load_dotenv()
    openai.api_key = os.getenv('API_KEY')


    ####################
    ##### CONTROLS #####
    ####################

    transcript = read_ref("chevron")
    # transcript2 = read_ref("chevron_2")
    system_instructions = read_message("system_extract")
    system_questions = read_message("system_questions")
    combine_sys = read_message("system_combine")
    sort_sys = read_message("system_sort")

    ####################
    ####################
    ####################


    log_time = datetime.datetime.now().strftime("%m-%d-%H-%M-%S")

    if (transcript == None or system_instructions == None):
        print("Input file error")
        quit()

    ### Chat GPT

    ## First Grab out the points multiple times


    all_responses = ""
    ### Grab out points a few times
    for i in range(extraction_count):

        ## GPT CALL
        all_responses += completion_text(gpt(1,system_instructions, transcript,log_time+"_e_"+str(i))) + '\n'
        # all_responses += completion_text(gpt(1,system_instructions, transcript2,log_time+"_e2_"+str(i))) + '\n'

    # question_answers = completion_text(gpt(0,"", read_message("system_questions2") + transcript,log_time+"_q"))
    # all_responses += question_answers + '\n'
    # QUIT FOR TESTING
    # quit()
    ### Combine
    last_combined = all_responses
    for i in range(combine_count):
        # GPT CALL
        last_combined = completion_text(gpt(0,combine_sys, last_combined,log_time+"_c_"+str(i)))

    ### Sorted
    ## GPT CALL
    sorted = gpt(0,sort_sys,last_combined,log_time+"_s")

    data = {
        'body': f'{sorted}'
    }
    set_data(sum_ref,data)
    


@app.route('/')
def index():
    return "Testing"
    # file_list = get_file_list('logs')
    # menu = create_menu(file_list)
    # return render_template('menu.html', menu=menu)

if __name__ == '__main__':
    # main()
    # test_gpt35_16K()
    app.run()

