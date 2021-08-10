from flask import Flask, render_template, redirect, flash, request, session
from flask.helpers import url_for
from flask_session import Session
from cs50 import SQL
from smtplib import SMTP
from os import getenv


app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///pessoas.db")

todos_livros = [
    'O Mundo de Sofia',
    'O Código Da Vinci',
    'O Pequeno Príncipe',
    'Os Miseráveis',
    'A Metamorfose',
    'O Alquimista',
    'A Arte da Guerra',
    'O Chamado de Cthulhu',
    'Romeu e Julieta',
]


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "GET":
        return render_template('index.html')


@app.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar():
    session['voltar_erro'] = '/cadastrar'

    if request.method == "GET":
        return render_template('cadastrar.html')

    elif request.method == "POST":
        dicios = db.execute("SELECT email FROM registrados")

        if not request.form.get('nome'):
            session['msg_erro'] = 'Você não tem nome?'
            return redirect('/erro')

        elif not request.form.get('email'):
            session['msg_erro'] = 'Você não tem e-mail?'
            return redirect('/erro')

        elif not request.form.get('senha1') or not request.form.get('senha2'):
            session['msg_erro'] = 'Preencha sua senha duas vezes.'
            return redirect('/erro')

        elif request.form.get('senha1') != request.form.get('senha2'):
            session['msg_erro'] = 'As senhas não batem.'
            return redirect('/erro')

        elif request.form.get('email') in [chave['email'] for chave in dicios]:
            session['msg_erro'] = 'Esse e-mail já está cadastrado.'
            return redirect('/erro')

        EMAIL_REMETENTE = getenv('EMAIL_REMETENTE')
        EMAIL_SENHA = getenv('EMAIL_SENHA')

        servidor = SMTP("smtp.gmail.com", 587)
        servidor.starttls()
        servidor.login(EMAIL_REMETENTE, EMAIL_SENHA)

        nome = request.form.get('nome').strip().title()
        email = request.form.get('email').strip().lower()
        senha = request.form.get('senha1').strip()

        db.execute("INSERT INTO registrados (nome, email, senha) VALUES(?, ?, ?)", nome, email, senha)

        texto = f"Parabéns! Você foi registrado com sucesso, {nome}!"
        assunto = "Registrado"
        msg_email = (f"Subject: {assunto}\n\n{texto}")
        
        servidor.sendmail(EMAIL_REMETENTE, email, msg_email.encode("utf8"))

        session['fez'] = 'se cadastrou'

        session["nome"] = db.execute("SELECT nome FROM registrados WHERE email= ?", email)[0]['nome']

        session["livros_carrinho"] = []

        return redirect(session.get('pagina_retorno') or '/pessoas')  # mudar pra redirect('/produtos')


@app.route('/entrar/rota_<rota>', methods=['GET', 'POST'])
def entrar(rota):
    session['voltar_erro'] = f"/entrar/rota_{rota}"

    if request.method == "GET":
        return render_template('entrar.html', rota=rota)

    elif request.method == "POST":
        if not request.form.get('email'):
            session['msg_erro'] = 'Você não tem e-mail?'
            return redirect('/erro')

        elif not request.form.get('senha'):
            session['msg_erro'] = 'Você não tem senha?'
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
            session['msg_erro'] = 'E-mail não cadastrado! Tente novamente.'
            return redirect('/erro')
        elif senha not in senhas_registradas:
            session['msg_erro'] = 'Senha incorreta! Tente novamente.'
            return redirect('/erro')

        session['fez'] = 'entrou'

        session["nome"] = db.execute("SELECT nome FROM registrados WHERE email= ?", email)[0]['nome']

        session["livros_carrinho"] = []

        return redirect(session.get('pagina_retorno') or '/pessoas')  # mudar pra redirect('/produtos')


@app.route('/pessoas')
def pessoas():
    if not session.get("nome"):
        session['pagina_retorno'] = '/pessoas'
        return redirect(url_for('entrar', rota="indireta"))

    msg_sucesso = f'Parabéns, {session.get("nome")}! Você {session.get("fez")} com sucesso!'

    nomes_emails = db.execute("SELECT nome, email FROM registrados")

    return render_template('pessoas.html', nomes_emails=nomes_emails, msg_sucesso=msg_sucesso)


@app.route('/produtos', methods=['GET', 'POST'])
def produtos():
    if not session.get("nome"):
        session['pagina_retorno'] = '/produtos'
        return redirect(url_for('entrar', rota="indireta"))

    session['voltar_erro'] = '/produtos'
        
    if session.get("carrinho_vazio") == True:
        session['livros_carrinho'] = []

    livros_restantes = [livro for livro in todos_livros if livro not in session['livros_carrinho']]

    if request.method == "GET":
        return render_template('produtos.html', livros=livros_restantes)

    elif request.method == "POST":
        if request.form.getlist('escolhido'):
            session['livros_adicionados'] = request.form.getlist('escolhido')

            for livro in session['livros_adicionados']:
                if livro in livros_restantes:
                    session['livros_carrinho'].append(livro)
                else:
                    session['msg_erro'] = 'Algum livro selecionado não está disponível...'
                    return redirect('/erro')

            session['carrinho_vazio'] = False

    return redirect('/carrinho')


@app.route('/carrinho')
def carrinho():
    if not session.get("nome"):
        session['pagina_retorno'] = '/carrinho'
        return redirect(url_for('entrar', rota="indireta"))

    livro_removido = request.args.get('removido')
    if livro_removido:
        session['livros_carrinho'].remove(livro_removido)
    
    try:
        livros_carrinho = session['livros_carrinho']
    except:
        livros_carrinho = []

    return render_template('carrinho.html', livros_carrinho=livros_carrinho)


@app.route("/desconectar")
def desconectar():
    if not session.get("nome") and not session.get("livros_carrinho"):
        flash('Você já está desconectado!')
        return redirect("/")
    else:
        session["nome"] = None
        session["livros_carrinho"] = None 
        return redirect("/")


@app.route('/erro')
def erro():
    return render_template('erro.html', msg_erro=session['msg_erro'], voltar_erro=session['voltar_erro'])
    