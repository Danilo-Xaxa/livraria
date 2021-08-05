// Determina o turno, a paleta de cores e o favicon de cada turno
(function principal() {
    // Descobre a hora e o minuto atual
    let agora = new Date()
    let hora = agora.getHours()
    let minuto = agora.getMinutes()

    // Manipula a hora e minuto manualmente
    hora = hora
    minuto = minuto

    // Formata bem o horário (nada de 14:0 ou 8:37)
    hora = String(hora).length == 1? '0' + hora : hora
    minuto = String(minuto).length == 1? '0' + minuto : minuto

    // Declara variáveis com base no turno (que ainda não foi determinado)
    let turno
    let msgBomTurno
    let h1BomTurno = document.getElementById('bomTurno')

    // Declara e inicializa variáveis que são HTMLCollection de elementos
    let tagsH1 = document.getElementsByTagName('h1')
    let tagsH2 = document.getElementsByTagName('h2')
    let tagsP = document.getElementsByTagName('p')
    let tagsTr = document.getElementsByTagName('tr')
    let tagsA = document.getElementsByTagName('a')
    let botoes = document.getElementsByTagName('label')

    // Declara variáveis que serão as cores dos elementos
    let corTexto
    let corTr
    let corA
    let corBotao
    let corBotaoTd

    // Determina as paletas com base no turno (que também será determinado agora)
    if (hora >= 0 && hora < 5) {
        turno = 'madrugada'
        corFundo = '#000'
        corTexto = '#EFF9F0'
        corTr = '#09814A'
        corA = '#DDC8C4'
        corBotao = '#8C1C13'
        corBotaoTd = corTr
    } else if (hora < 12) {
        turno = 'manha'
        corFundo = '#70A8BB'
        corTexto = '#37323E'
        corTr = '#679436'
        corA = '#C03221'
        corBotao = '#EF3E36'
        corBotaoTd = corA
    } else if (hora < 18) {
        turno = 'tarde'
        corFundo = '#FFA500'
        corTexto = '#121619'
        corTr = '#14591D'
        corA = '#DD1C1A'
        corBotao = '#B9314F'
        corBotaoTd = corA
    } else if (hora <= 23) {
        turno = 'noite'
        corFundo = '#800080'
        corTexto = '#F2EDEB'
        corTr = '#31572C'
        corA = '#FABC2A'
        corBotao = '#BD93BD'
        corBotaoTd = corTr
    }

    // Configura a mensagem do bom turno e a cor de fundo
    msgBomTurno = (hora >= 5 && hora < 12) ? 'Bom dia!' : `Boa ${turno}!`
    document.body.style.background = corFundo

    // Cria variáveis CSS de cores
    document.documentElement.style.setProperty('--corBotaoTd', corBotaoTd);
    document.documentElement.style.setProperty('--botaoSelecionado', corTr);
    document.documentElement.style.setProperty('--tabela', corTr);

    // Configura o favicon adequado para o turno
    let link = document.querySelector("link[rel*='icon']") || document.createElement('link');
    link.type = 'image/x-icon';
    link.rel = 'shortcut icon';
    link.href = `../static/favicons/favicon-${turno}.ico`
    head = document.getElementsByTagName('head')[0]
    head.appendChild(link);

    // Determina cor de cada tag (não consegui juntar os HTMLCollection num array)
    if (tagsH1) {
        for (let tag of Array.from(tagsH1)) {
            tag.style.color = corTexto
        }
    }

    if (tagsH2) {
        for (let tag of Array.from(tagsH2)) {
            tag.style.color = corTexto
        }
    }

    if (tagsP) {
        for (let tag of Array.from(tagsP)) {
            tag.style.color = corTexto
        }
    }

    if (tagsTr) {
        for (let tag of Array.from(tagsTr)) {
            tag.style.backgroundColor = corTr
        }
    }

    if (tagsA) {
        for (let tag of Array.from(tagsA)) {
            tag.style.color = corA
        }
    }

    // Configura a cor de fundo e borda dos botões
    if (botoes) {
        for (let botao of Array.from(botoes)) {
            botao.style.backgroundColor = corBotao
            botao.style.borderColor = corBotao
        }
    }

    // Determina a mensagem do bom turno
    if (h1BomTurno) {
        h1BomTurno.innerText = msgBomTurno
    }
})()


// Remove determinado livro do carrinho. Chamada ao clicar o botão "Remover"
function removeLivro(livro) {
    window.location.href=`/carrinho?removido=${encodeURI(livro)}`
}


// Determina quais livros restam em /produtos (ou seja, fora do carrinho)
let livrosRestantes = []
for (let livro of document.getElementsByClassName('btn-check')) {
    livrosRestantes.push(livro.id)
}


// Remove todos os acentos do texto digitado. Usado no input "Livro"
function removeAcento(texto) {                                                
    texto = texto.replace(new RegExp('[ÁÀÂÃ]','gi'), 'a')
    texto = texto.replace(new RegExp('[ÉÈÊ]','gi'), 'e')
    texto = texto.replace(new RegExp('[ÍÌÎ]','gi'), 'i')
    texto = texto.replace(new RegExp('[ÓÒÔÕ]','gi'), 'o')
    texto = texto.replace(new RegExp('[ÚÙÛ]','gi'), 'u')
    texto = texto.replace(new RegExp('[Ç]','gi'), 'c')
    return texto;                 
}


// Trabalha a seleção dos botões dos livros com base no input "Livro"
let inputLivro = document.getElementById('inputLivro')
if (inputLivro) {
    inputLivro.addEventListener('keyup', function() {
        // Pra cada vez que uma tecla digitada for solta:
        let digitado = removeAcento(inputLivro.value.toLowerCase())
        let correspondentes = []

        // Pega os livros correspondentes com o texto digitado
        for (let livro of livrosRestantes) {
            if (removeAcento(livro.toLowerCase()).startsWith(digitado) && digitado != '') {
                correspondentes.push(livro)
            }
        }

        // Se tem algum correspondente, clica nele artificialmente
        if (correspondentes) {
            for (let correspondente of correspondentes) {
                let checkbox = document.getElementById(correspondente)
                if (checkbox.checked == false) {
                    checkbox.checked = true
                    checkbox.className = 'artificalmenteClicado'
                }
            }
        }

        // Se tem algum livro que não corresponde mais com o novo texto digitado (nova tecla solta), desclica nele
        for (let checkbox of document.getElementsByTagName('input')) {
            let naoCorrespondeMais = checkbox.className == 'artificalmenteClicado' && !(correspondentes.includes(checkbox.id))

            if (naoCorrespondeMais) {
                checkbox.checked = false
                checkbox.className = 'artificalmenteDesclicado'
            }
        }
    })
}
