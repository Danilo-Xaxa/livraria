from flask import Flask

meu_app = Flask(__name__)

@meu_app.route('/')
def index():
    return 'ola mundo'
