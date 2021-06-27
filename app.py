from flask import Flask, render_template, request
from cs50 import *


meu_app = Flask(__name__)

@meu_app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')

    elif request.method == 'POST':
        if not request.form.get('nome').strip():
            return render_template('erro.html', texto_erro='Você não tem nome?')

        elif not request.form.get('humor'):
            return render_template('erro.html', texto_erro='Você não tem emoções?')

        return render_template('cumprimento.html', nome=request.form.get('nome'), humor=request.form.get('humor'))
