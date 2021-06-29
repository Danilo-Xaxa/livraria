from flask import Flask, render_template, request, redirect
from cs50 import SQL
from smtplib import SMTP
import teste  # TODO: Deletar saporra dps das env var
import os


meu_app = Flask(__name__)

db = SQL("sqlite:///pessoas.db")


@meu_app.route('/', methods=['GET', 'POST'])
def index():
    global msg_erro

    if request.method == "GET":
        return render_template('index.html')

    elif request.method == "POST":
        if request.form.get('escolha').lower() == 'cadastrar':
            return redirect('/cadastrar')
        elif request.form.get('escolha').lower() == 'entrar':
            return redirect('/entrar')
        else:
            msg_erro = 'Deu bosta'
            return redirect('/erro')


@meu_app.route('/cadastrar', methods=['GET', 'POST'])
def route_cadastrar():
    global msg_erro
    global fez
    global voltar_erro
    voltar_erro = '/cadastrar'

    if request.method == "GET":
        return render_template('cadastrar.html')

    elif request.method == "POST":
        if not request.form.get('nome'):
            msg_erro = 'Você não tem nome?'
            return redirect('/erro')

        elif not request.form.get('email'):
            msg_erro = 'Você não tem e-mail?'
            return redirect('/erro')

        elif not request.form.get('senha1') or not request.form.get('senha2'):
            msg_erro = 'Preencha sua senha duas vezes.'
            return redirect('/erro')

        elif request.form.get('senha1') != request.form.get('senha2'):
            msg_erro = 'As senhas não batem.'
            return redirect('/erro')

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

        fez = 'se cadastrou'

        return redirect('/pessoas')


@meu_app.route('/entrar', methods=['GET', 'POST'])
def route_entrar():
    global msg_erro
    global fez
    global voltar_erro
    voltar_erro = '/entrar'

    if request.method == "GET":
        return render_template('entrar.html')

    elif request.method == "POST":
        if not request.form.get('email'):
            msg_erro = 'Você não tem e-mail?'
            return redirect('/erro')

        elif not request.form.get('senha'):
            msg_erro = 'Você não tem senha?'
            return redirect('/erro')

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
            return redirect('/erro')
        elif senha not in senhas_registradas:
            msg_erro = 'Senha incorreta! Tente novamente.'
            return redirect('/erro')

        fez = 'entrou'

        return redirect('/pessoas')


@meu_app.route('/pessoas')
def route_pessoas():
    msg = f'Parabéns! Você {fez} com sucesso!'  # TODO: Personalizar mais a msg

    linhas = db.execute("SELECT nome, email FROM registrados")

    return render_template('pessoas.html', pessoas=linhas, msg=msg)


@meu_app.route('/erro')
def route_erro():
    return render_template('erro.html', msg_erro=msg_erro, voltar_erro=voltar_erro)