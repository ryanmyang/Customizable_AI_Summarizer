from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import openai
import os
import io
import datetime
from _utils.firebase_utils import add_data, get_data, set_data

app = Flask(__name__)


@app.route('/api')
def home():
    add_data("test",{"Test": "Value"})
    return jsonify({'message': 'Job starting'})

@app.route('/about')
def about():
    return 'About'