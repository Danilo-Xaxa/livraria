(function horarioFaviconCores() {
    // ARRUMAR ESSA GAMBIARRA MONSTRUOSA QUE É ESSA IIFE
    let agora = new Date()
    let hora = agora.getHours()
    let minuto = agora.getMinutes()

    hora = hora // pra manipular a hora manualmente (e o minuto abaixo)
    minuto = minuto

    hora = String(hora).length == 1? '0' + hora : hora
    minuto = String(minuto).length == 1? '0' + minuto : minuto

    let meuFavicon

    let msgBomHorario
    let h1BomHorario = document.getElementById('bomHorario')

    let tagsH1 = document.getElementsByTagName('h1')
    let tagsH2 = document.getElementsByTagName('h2')
    let tagsP = document.getElementsByTagName('p')

    let tagsTr = document.getElementsByTagName('tr')
    let tagsA = document.getElementsByTagName('a')
    let botoes = document.getElementsByTagName('label')

    let corTexto
    
    let corTr
    let corA
    let corBotao
    

    if (hora >= 0 && hora < 5) {
        meuFavicon = '../static/favicons/favicon-madrugada.ico'
        msgBomHorario = 'Boa madrugada!'
        document.body.style.background = '#000'
        corTexto = '#EFF9F0'
        corTr = '#09814A'
        corA = '#DDC8C4'
        corBotao = '#8C1C13'
        document.documentElement.style.setProperty('--corTdButton', corTr);
    } else if (hora < 12) {
        meuFavicon = '../static/favicons/favicon-manha.ico'
        msgBomHorario = 'Bom dia!'
        document.body.style.background = '#70A8BB'
        corTexto = '#37323E'
        corTr = '#679436'
        corA = '#C03221'
        corBotao = '#EF3E36'
        document.documentElement.style.setProperty('--corTdButton', corA);
    } else if (hora < 18) {
        meuFavicon = '../static/favicons/favicon-tarde.ico'
        msgBomHorario = 'Boa tarde!'
        document.body.style.background = '#FFA500'
        corTexto = '#121619'
        corTr = '#14591D'
        corA = '#DD1C1A'
        corBotao = '#B9314F'
        document.documentElement.style.setProperty('--corTdButton', corA);
    } else if (hora <= 23) {
        meuFavicon = '../static/favicons/favicon-noite.ico'
        msgBomHorario = 'Boa noite!'
        document.body.style.background = '#800080'
        corTexto = '#F2EDEB'
        corTr = '#31572C'
        corA = '#FABC2A'
        corBotao = '#BD93BD'
        document.documentElement.style.setProperty('--corTdButton', corTr);
    }


    document.documentElement.style.setProperty('--botaoSelecionado', corTr);
    document.documentElement.style.setProperty('--tabela', corTr);


    let link = document.querySelector("link[rel*='icon']") || document.createElement('link');
    link.type = 'image/x-icon';
    link.rel = 'shortcut icon';
    link.href = meuFavicon;
    head = document.getElementsByTagName('head')[0]
    head.appendChild(link);


    if (tagsH1) {
        for (let tagH1 of Array.from(tagsH1)) {
            tagH1.style.color = corTexto
        }
    }

    if (tagsH2) {
        for (let tagH2 of Array.from(tagsH2)) {
            tagH2.style.color = corTexto
        }
    }

    if (tagsP) {
        for (let tagP of Array.from(tagsP)) {
            tagP.style.color = corTexto
        }
    }

    if (tagsTr) {
        for (let tagTr of Array.from(tagsTr)) {
            tagTr.style.backgroundColor = corTr
        }
    }

    if (tagsA) {
        for (let tagA of Array.from(tagsA)) {
            tagA.style.color = corA
        }
    }

    if (botoes) {
        for (let botao of Array.from(botoes)) {
            botao.style.backgroundColor = corBotao
            botao.style.borderColor = corBotao
        }
    }

    if (h1BomHorario) {
        h1BomHorario.innerText = msgBomHorario
    }
})()



function removerLivro(livro) {
    window.location.href=`/carrinho?removido=${encodeURI(livro)}`
}



function ajax() {
    // tem que importar jquery, né?
}
