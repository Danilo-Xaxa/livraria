# [DX Livraria](https://xaxadanilo.pythonanywhere.com/)

<img src="https://github.com/Danilo-Xaxa/livraria/blob/main/static/imagens/screenshot_home.png"/>

<img src="https://github.com/Danilo-Xaxa/livraria/blob/main/static/imagens/screenshot_livros.png"/>

[DX Livraria](https://xaxadanilo.pythonanywhere.com/) é uma aplicação web que simula um e-commerce de livros reais onde você pode: criar ou acessar sua conta, ver quais são os livros em estoque, adicionar livros ao seu carrinho, comprar os livros (que chegarão em seu e-mail em .pdf) e ver quais são os membros do Clube do Livro (pessoas que estão cadastradas no site).

Ao acessar o site sem ter se cadastrado ou entrado ainda, o usuário vê a página inicial (home). Para acessar as outras páginas, o usuário pode navegar pelo cabeçalho do site. As páginas dos livros em estoque, carrinho e Clube do Livro só podem ser acessados quando o usuário cria uma conta ou entra.

Ao se cadastrar, chegará um e-mail avisando que o cadastro foi realizado com sucesso, mas não há necessidade de confirmar cadastro via e-mail.

Ao entrar sem ter clicado em nenhuma outra aba do cabeçalho, o usuário será redirecionado para a página "Livros em Estoque".

---

Na página "Livros em Estoque", o usuário vê quais livros estão disponíveis na loja e adicionar eles ao carrinho. Para selecionar, pode-se clicar nos livros ou digitar o nome do livro escolhido na caixa de input.

Na página "Carrinho", o usuário vê quais livros foram adicionados ao seu carrinho e pode removê-los ou comprá-los. Ao comprar, os livros chegarão via e-mail em formato PDF.

Na página "Clube do Livro", o usuário vê os nomes e e-mails das outras pessoas cadastradas no site.

---

O usuário pode cadastrar, entrar ou desconectar sempre que quiser.

O site é totalmente responsivo e é capaz de lidar com erros básicos.

OBS: Não use nenhuma senha importante que você usa em outros lugares, pois ela pode acabar vazando. Já que o medidor de força de senha está desabilitado, o usuário pode usar qualquer senha simples que desejar, como "123" ou "abc".

---

O projeto foi desenvolvido com Python e o framework Flask no back-end e JavaScript puro no front-end. O banco de dados utilizado é o SQLite. Para a maioria dos detalhes de design/layout, o Bootstrap foi utilizado, especialmente o Bootstrap Examples Product.

A hospedagem foi realizada via PythonAnywhere.

DX Livraria é o meu primeiro projeto usando Flask, desenvolvido a partir dos meus primeiros estudos do framework.

O projeto é inspirado inspirado na aula de Flask do curso CS50 de Harvard e tem fins apenas educacionais.
