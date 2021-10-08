from flask import Flask, render_template, redirect, flash, request, session
from flask.helpers import url_for
from flask_session import Session
from cs50 import SQL
from smtplib import SMTP
from email.message import EmailMessage
from os import getenv 


app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:////home/XaxaDanilo/livraria/pessoas.db")

todos_livros = [
    #'O Código Da Vinci',
    #'O Mundo de Sofia',
    #'O Pequeno Príncipe',
    'A Arte da Guerra',
    'A Metamorfose',
    'Romeu e Julieta',
    'Os Miseráveis',
    #'O Alquimista',
    'O Chamado de Cthulhu',
    'A República'
]


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "GET":
        return render_template('index.html')


@app.route('/cadastrar/por_<pagina>', methods=['GET', 'POST'])
def cadastrar(pagina):
    session['voltar_erro'] = f"/cadastrar/por_{pagina}"

    if request.method == "GET":
        return render_template('cadastrar.html', pagina=pagina)

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

        EMAIL_REMETENTE = getenv("EMAIL_REMETENTE")
        SENHA_REMETENTE = getenv("SENHA_REMETENTE")

        servidor = SMTP("smtp.gmail.com", 587)
        servidor.starttls()
        servidor.login(EMAIL_REMETENTE, SENHA_REMETENTE)

        nome = request.form.get('nome').strip().title()
        email = request.form.get('email').strip().lower()
        senha = request.form.get('senha1').strip()

        db.execute("INSERT INTO registrados (nome, email, senha) VALUES(?, ?, ?)", nome, email, senha)

        texto = f"Parabéns! Você foi registrado com sucesso, {nome}!"
        assunto = "Registrado"
        msg_email = (f"Subject: {assunto}\n\n{texto}")

        servidor.sendmail(EMAIL_REMETENTE, email, msg_email.encode("utf8"))

        session["nome"] = db.execute("SELECT nome FROM registrados WHERE email= ?", email)[0]['nome']

        session["livros_carrinho"] = []

        if pagina in ["produtos", "carrinho", "pessoas"]:
            return redirect('/' + pagina)
        else:
            return redirect('/produtos')


@app.route('/entrar/por_<pagina>', methods=['GET', 'POST'])
def entrar(pagina):
    session['voltar_erro'] = f"/entrar/por_{pagina}"

    if request.method == "GET":
        return render_template('entrar.html', pagina=pagina)

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

        session["nome"] = db.execute("SELECT nome FROM registrados WHERE email= ?", email)[0]['nome']

        session["livros_carrinho"] = []

        if pagina in ["produtos", "carrinho", "pessoas"]:
            return redirect('/' + pagina)
        else:
            return redirect('/produtos')


@app.route('/pessoas')
def pessoas():
    if not session.get("nome"):
        return redirect(url_for('entrar', pagina="pessoas"))

    nomes_emails = db.execute("SELECT nome, email FROM registrados")

    return render_template('pessoas.html', nomes_emails=nomes_emails)


@app.route('/produtos', methods=['GET', 'POST'])
def produtos():
    if not session.get("nome"):
        return redirect(url_for('entrar', pagina="produtos"))

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


@app.route('/carrinho', methods=['GET', 'POST'])
def carrinho():
    if not session.get("nome"):
        return redirect(url_for('entrar', pagina="carrinho"))

    if request.method == "GET":
        livro_removido = request.args.get('removido')
        if livro_removido:
            session['livros_carrinho'].remove(livro_removido)

        try:
            livros_carrinho = session['livros_carrinho']
            flash('Ao clicar em "Comprar", pode demorar um pouco mas os livros serão enviados para você :)')
        except:
            livros_carrinho = []

        return render_template('carrinho.html', livros_carrinho=livros_carrinho)

    elif request.method == "POST":
        nome = session.get("nome")
        livros_carrinho = session.get("livros_carrinho")

        EMAIL_REMETENTE = getenv("EMAIL_REMETENTE")
        SENHA_REMETENTE = getenv("SENHA_REMETENTE")
        email = db.execute("SELECT email FROM registrados WHERE nome = ?", nome)[0]['email']

        msg = EmailMessage()
        msg['From'] = EMAIL_REMETENTE
        msg['To'] = email
        msg['Subject'] = 'Seus livros comprados'

        corpo = f'Olá, {nome}! Aqui estão os livros que você comprou conosco, volte sempre!'
        msg.set_content(corpo)

        for livro in livros_carrinho:
            arquivo = f"{livro.replace(' ', '_')}.pdf"
            with open(f'/home/XaxaDanilo/livraria/static/pdfs/{arquivo}', 'rb') as conteudo:
                msg.add_attachment(conteudo.read(), maintype='application/pdf', subtype='pdf', filename=arquivo)

        texto = msg.as_string()

        servidor = SMTP("smtp.gmail.com", 587)
        servidor.starttls()
        servidor.login(EMAIL_REMETENTE, SENHA_REMETENTE)

        servidor.sendmail(EMAIL_REMETENTE, email, texto)

        session['livros_carrinho'] = []
        return render_template('compra.html')


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


@app.errorhandler(404)
def page_not_found(e):
    session['msg_erro'] = 'Página inválida... Evite navegar diretamente pela URL neste site, por favor.'
    return redirect('/erro')
