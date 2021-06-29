from flask import Flask, render_template, request, redirect
from cs50 import SQL
from smtplib import SMTP
import teste  # TODO: Deletar saporra dps das env var
import os


meu_app = Flask(__name__)

db = SQL("sqlite:///pessoas.db")


@meu_app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "GET":
        return render_template('index.html')

    elif request.method == "POST":
        if request.form.get('escolha').lower() == 'cadastrar':
            return render_template('cadastrar.html')
        elif request.form.get('escolha').lower() == 'entrar':
            return render_template('entrar.html')
        else: 
            return render_template('erro.html', msg_erro='Deu bosta')

    else:
        return render_template('erro.html', msg_erro='Deu merda')


@meu_app.route('/cadastrar/', methods=['GET', 'POST'])
def route_cadastrar():
    if not request.form.get('nome'):
        return render_template('erro.html', msg_erro='Você não tem nome?')

    elif not request.form.get('email'):
        return render_template('erro.html', msg_erro='Você não tem e-mail?')

    elif not request.form.get('senha1') or not request.form.get('senha2'):
        return render_template('erro.html', msg_erro='Preencha sua senha duas vezes.')

    elif request.form.get('senha1') != request.form.get('senha2'):
        return render_template('erro.html', msg_erro='As senhas não batem.')

    nome = request.form.get('nome').strip().title()
    email = request.form.get('email').lower()
    senha = request.form.get('senha1')

    db.execute("INSERT INTO registrados (nome, email, senha) VALUES(?, ?, ?)", nome, email, senha)

    texto = f"Parabens! Tu foi registrado com sucesso, {nome}!!!"
    assunto = "Registrado!"
    msg_email = (f"Subject: {assunto}\n\n{texto}")
    
    EMAIL_REMETENTE = teste.EMAIL_REMETENTE  # TODO: os.getenv('EMAIL_REMETENTE')
    EMAIL_SENHA = teste.EMAIL_SENHA  # TODO: os.getenv('EMAIL_SENHA')

    servidor = SMTP("smtp.gmail.com", 587)
    servidor.starttls()
    servidor.login(EMAIL_REMETENTE, EMAIL_SENHA)
    servidor.sendmail(EMAIL_REMETENTE, email, msg_email)

    return redirect('/pessoas/')


@meu_app.route('/entrar/', methods=['GET', 'POST'])
def route_entrar():
    if not request.form.get('email'):
        return render_template('erro.html', msg_erro='Você não tem e-mail?')

    elif not request.form.get('senha'):
        return render_template('erro.html', msg_erro='Você não tem senha?')

    email = request.form.get('email')
    senha = request.form.get('senha')

    emails_registrados = []
    senhas_registradas = []

    linhas = db.execute("SELECT email, senha FROM registrados")

    for linha in linhas:
        emails_registrados.append(linha['email'])
        senhas_registradas.append(linha['senha'])

    if email not in emails_registrados:
        msg_erro = 'E-mail incorreto! Tente novamente.'
        return render_template('erro.html', msg_erro=msg_erro)
    elif senha not in senhas_registradas:
        msg_erro = 'Senha incorreta! Tente novamente.'
        return render_template('erro.html', msg_erro=msg_erro)

    return redirect('/pessoas/')


@meu_app.route('/pessoas/')
def route_pessoas():
    msg = 'Parabéns! Você se cadastrou ou entrou com sucesso!'  # TODO: Personalizar mais a msg

    linhas = db.execute("SELECT nome, email FROM registrados")

    return render_template('pessoas.html', pessoas=linhas, msg=msg)
