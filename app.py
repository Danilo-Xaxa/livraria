from flask import Flask, render_template, request
from flask_mail import Mail, Message
from email_senha_nome import var_email, var_senha, var_nome
from cs50 import SQL


meu_app = Flask(__name__)

db = SQL("sqlite:///pessoas.db")

meu_app.config["MAIL_DEFAULT_SENDER"] = var_email
meu_app.config["MAIL_PASSWORD"] = var_senha
meu_app.config["MAIL_PORT"] = 587
meu_app.config["MAIL_SERVER"] = "smtp.gmail.com"
meu_app.config["MAIL_USE_TLS"] = True
meu_app.config["MAIL_USERNAME"] = var_nome
mail = Mail(meu_app)


@meu_app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')

    elif request.method == 'POST':
        if not request.form.get('nome').strip():
            return render_template('erro.html', msg_erro='Você não tem nome?')

        elif not request.form.get('humor'):
            return render_template('erro.html', msg_erro='Você não tem emoções?')

        elif not request.form.get('email'):
            return render_template('erro.html', msg_erro='Você não tem e-mail?')

        nome = request.form.get('nome').strip()
        humor = request.form.get('humor')
        email = request.form.get('email')

        db.execute("INSERT INTO registrados (nome, humor, email) VALUES(?, ?, ?)", nome, humor, email)  # TODO: incluir e-mail

        mensagem = Message(f"Você está registrado, {nome}! Mais um motivo para ficar {humor}!", recipients=[email])
        mail.send(mensagem)

        return render_template('cumprimento.html', nome=request.form.get('nome'), humor=request.form.get('humor'))


@meu_app.route('/pessoas/')
def route_pessoas():
    linhas = db.execute("SELECT * FROM registrados")
    return render_template('pessoas.html', pessoas=linhas)
