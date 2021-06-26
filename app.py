from flask import Flask, render_template, request

meu_app = Flask(__name__)

@meu_app.route('/')
def index():
    return render_template('index.html')


@meu_app.route('/cumprimento/')
def cumprimento():
    return render_template('cumprimento.html', nome=request.args.get('nome', 'mundo'))
