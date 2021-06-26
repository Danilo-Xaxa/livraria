from flask import Flask, render_template, request

meu_app = Flask(__name__)

@meu_app.route('/')
def index():
    return render_template('index.html')


@meu_app.route('/cumprimento/', methods=["POST"])
def cumprimento():
    return render_template('cumprimento.html', nome=request.form.get('nome', 'mundo'))
