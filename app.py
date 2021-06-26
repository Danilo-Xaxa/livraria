from flask import Flask, render_template, request


meu_app = Flask(__name__)

@meu_app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
        
    elif request.method == 'POST':
        return render_template('cumprimento.html', nome=request.form.get('nome', 'mundo'))
