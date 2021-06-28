from flask import Flask, render_template, request
from cs50 import SQL
from smtplib import SMTP
from remetente_senha import remetente, senha
# from unidecode import unidecode (usar se o e-mail nao suportar utf-8 ou unicode)


meu_app = Flask(__name__)

db = SQL("sqlite:///pessoas.db")


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

        nome = request.form.get('nome').strip().title()
        humor = request.form.get('humor')
        email = request.form.get('email')

        db.execute("INSERT INTO registrados (nome, humor, email) VALUES(?, ?, ?)", nome, humor, email)

        texto = f"Tu foi registrado, {nome}. Mais um motivo para ficar {humor}!"
        assunto = "Oi!"
        msg = (f"Subject: {assunto}\n\n{texto}")
        servidor = SMTP("smtp.gmail.com", 587)
        servidor.starttls()
        servidor.login(remetente, senha)
        servidor.sendmail(remetente, email, msg)

        return render_template('cumprimento.html', nome=nome, humor=humor)


@meu_app.route('/pessoas/')
def route_pessoas():
    linhas = db.execute("SELECT * FROM registrados")
    return render_template('pessoas.html', pessoas=linhas)
