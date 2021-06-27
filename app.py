from flask import Flask, render_template, request
from cs50 import *


pessoas = {}

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

        nome = request.form.get('nome').strip()
        humor = request.form.get('humor')
        pessoas[nome] = humor

        return render_template('cumprimento.html', nome=request.form.get('nome'), humor=request.form.get('humor'), pessoas=pessoas)

@meu_app.route('/pessoas/')
def route_pessoas():
    return render_template('pessoas.html', pessoas=pessoas)
