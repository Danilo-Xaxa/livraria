from flask import Flask, render_template, redirect, request, session
from flask_session import Session
from os import getenv
from cs50 import SQL
from smtplib import SMTP


meu_app = Flask(__name__)
meu_app.config["SESSION_PERMANENT"] = False
meu_app.config["SESSION_TYPE"] = "filesystem"
Session(meu_app)

db = SQL("sqlite:///pessoas.db")

todos_livros = [
    'O Mundo de Sofia',
    'O Código Da Vinci',
    'O Pequeno Príncipe',
    'Os Miseráveis',
    'Sapiens',
    'A Metamorfose',
    'O Alquimista',
    'A Arte da Guerra',
    'O Chamado de Cthulhu',
    'Romeu e Julieta',
]


@meu_app.route('/', methods=['GET', 'POST'])
def index():
    global msg_erro
    global nome_pessoa
    global fez
    global carrinho_vazio

    if request.method == "GET":
        if session.get("nome"):
            fez = 'entrou'
            nome_pessoa = session.get("nome")
            carrinho_vazio = False
            return redirect('/pessoas')
        else:
            carrinho_vazio = True
            return render_template('index.html')

    elif request.method == "POST":
        if request.form['botao'] == 'Cadastrar':
            return redirect('/cadastrar')
        elif request.form['botao'] == 'Entrar':
            return redirect('/entrar')


@meu_app.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar():
    global msg_erro
    global fez
    global voltar_erro
    global nome_pessoa
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
        email = request.form.get('email').strip().lower()
        senha = request.form.get('senha1').strip()

        db.execute("INSERT INTO registrados (nome, email, senha) VALUES(?, ?, ?)", nome, email, senha)

        texto = f"Parabéns! Você foi registrado com sucesso, {nome}!"
        assunto = "Registrado"
        msg_email = (f"Subject: {assunto}\n\n{texto}")
        
        EMAIL_REMETENTE = getenv('EMAIL_REMETENTE')
        EMAIL_SENHA = getenv('EMAIL_SENHA')

        servidor = SMTP("smtp.gmail.com", 587)
        servidor.starttls()
        servidor.login(EMAIL_REMETENTE, EMAIL_SENHA)
        servidor.sendmail(EMAIL_REMETENTE, email, msg_email.encode("utf8"))

        fez = 'se cadastrou'

        session["nome"] = db.execute(f"SELECT nome FROM registrados WHERE email='{email}'")[0]['nome']  # eu deveria usar a sintaxe de placeholder (?)

        session["livros"] = []

        nome_pessoa = session.get("nome")

        return redirect('/pessoas')


@meu_app.route('/entrar', methods=['GET', 'POST'])
def entrar():
    global msg_erro
    global fez
    global voltar_erro
    global nome_pessoa
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
            msg_erro = 'E-mail não cadastrado! Tente novamente.'
            return redirect('/erro')
        elif senha not in senhas_registradas:
            msg_erro = 'Senha incorreta! Tente novamente.'
            return redirect('/erro')

        fez = 'entrou'

        session["nome"] = db.execute(f"SELECT nome FROM registrados WHERE email='{email}'")[0]['nome']  # eu deveria usar a sintaxe de placeholder (?)

        session["livros"] = []

        nome_pessoa = session.get("nome")

        return redirect('/pessoas')


@meu_app.route('/pessoas')
def pessoas():
    msg_sucesso = f'Parabéns, {nome_pessoa}! Você {fez} com sucesso!'

    linhas = db.execute("SELECT nome, email FROM registrados")

    return render_template('pessoas.html', pessoas=linhas, msg_sucesso=msg_sucesso)


@meu_app.route('/produtos', methods=['GET', 'POST'])
def produtos():
    global livros_carrinho
    global livros_adicionados
    global carrinho_vazio

    if carrinho_vazio:
        livros_carrinho = []
    else:
        livros_carrinho = session.get("livros")

    livros_restantes = [livro for livro in todos_livros if livro not in livros_carrinho]

    if request.method == "GET":
        return render_template('produtos.html', livros=livros_restantes)

    elif request.method == "POST":
        if request.form.getlist('escolhido'):
            livros_adicionados = request.form.getlist('escolhido')

            for livro in livros_adicionados:
                livros_carrinho.append(livro)

            carrinho_vazio = False
            session["livros"] = livros_carrinho

    return redirect('/carrinho')


@meu_app.route('/carrinho')
def carrinho():
    livro_removido = request.args.get('removido')
    if livro_removido:
        livros_carrinho.remove(livro_removido)
        session["livros"] = livros_carrinho
        
    return render_template('carrinho.html', livros_carrinho=livros_carrinho)


@meu_app.route("/desconectar")
def desconectar():
    session["nome"] = None
    session["livros"] = None 
    return redirect("/")


@meu_app.route('/erro')
def erro():
    return render_template('erro.html', msg_erro=msg_erro, voltar_erro=voltar_erro)
