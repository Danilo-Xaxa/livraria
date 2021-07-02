function horarioBackgroundFavicon() {
    let agora = new Date()
    let hora = agora.getHours()
    let minuto = agora.getMinutes()

    hora = String(hora).length == 1? '0' + hora : hora
    minuto = String(minuto).length == 1? '0' + minuto : minuto

    let meuFavicon

    let msgBomHorario
    let h1BomHorario = document.getElementById('bomHorario')

    let tagsH1 = document.getElementsByTagName('h1')
    let tagsP = document.getElementsByTagName('p')
    let tagsA = document.getElementsByTagName('a')
    let corTexto
    let corA
    

    if (hora >= 0 && hora < 5) {
        document.body.style.background = 'black'
        meuFavicon = '../static/favicons/favicon-madrugada.ico'
        msgBomHorario = 'Boa madrugada!'
        corTexto = 'white'
        corA = 'pink'
    } else if (hora < 12) {
        document.body.style.background = 'rgb(112, 168, 187)'
        meuFavicon = '../static/favicons/favicon-manha.ico'
        msgBomHorario = 'Bom dia!'
        corA = 'brown'
    } else if (hora < 18) {
        document.body.style.background = 'orange'
        meuFavicon = '../static/favicons/favicon-tarde.ico'
        msgBomHorario = 'Boa tarde!'
        corA = 'purple'
    } else if (hora <= 23) {
        corTexto = 'white'
        document.body.style.background = 'purple'
        meuFavicon = '../static/favicons/favicon-noite.ico'
        msgBomHorario = 'Boa noite!'
        corTexto = 'white'
        corA = 'yellow'
    }


    let link = document.querySelector("link[rel*='icon']") || document.createElement('link');
    link.type = 'image/x-icon';
    link.rel = 'shortcut icon';
    link.href = meuFavicon;
    head = document.getElementsByTagName('head')[0]
    head.appendChild(link);


    if (h1BomHorario) {
        h1BomHorario.innerText = `${msgBomHorario}`
    }

    if (tagsH1) {
        for (let tagH1 of Array.from(tagsH1)) {
            tagH1.style.color = corTexto || 'black'
        }
    }

    if (tagsP) {
        for (let tagP of Array.from(tagsP)) {
            tagP.style.color = corTexto
        }
    }

    if (tagsA) {
        for (let tagA of Array.from(tagsA)) {
            tagA.style.color = corA
        }
    }
}

horarioBackgroundFavicon()


/*
function corBotoes() {
    if (getElementsByTagName('label')) {
        const botoes = getElementsByTagName('label')
        ...
    }
}
corBotoes()
*/


/*
function ajax() {
    // tem que importar jquery, né?
}

ajax()
*/