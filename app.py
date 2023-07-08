from flask import Flask
from dotenv import load_dotenv
import os

app = Flask(__name__)
load_dotenv()
api_key = os.getenv('API_KEY')

@app.route('/')
def hello():
    return api_key

if __name__ == '__main__':
    app.run()
