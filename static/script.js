function horarioFavicon() {
    let agora = new Date()
    let hora = agora.getHours()
    let minuto = agora.getMinutes()

    hora = String(hora).length == 1? '0' + hora : hora
    minuto = String(minuto).length == 1? '0' + minuto : minuto

    hora = 03
    minuto = 00

    let meuFavicon
    let msgBomHorario
    let corA
    let corTexto
    let bomHorario = document.getElementById('bomHorario')
    let tagsA = document.getElementsByTagName('a')
    let tagsP = document.getElementsByTagName('p')
    let h1 = Array.from(document.getElementsByTagName('h1'))[0]

    if (hora > 0 && hora < 5) {
        corTexto = 'white'
        document.body.style.background = 'black'
        meuFavicon = '../static/favicons/favicon-madrugada.ico'
        msgBomHorario = 'Boa madrugada!'
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
        corA = 'red'
    } else if (hora <= 24) {
        corTexto = 'white'
        document.body.style.background = 'purple'
        meuFavicon = '../static/favicons/favicon-noite.ico'
        msgBomHorario = 'Boa noite!'
        corA = 'yellow'
    }

    let link = document.querySelector("link[rel*='icon']") || document.createElement('link');
    link.type = 'image/x-icon';
    link.rel = 'shortcut icon';
    link.href = meuFavicon;
    head = document.getElementsByTagName('head')[0]
    head.appendChild(link);

    if (h1) {
        h1.style.color = `${corTexto}` || 'black'
    }

    if (tagsA) {
        for (let tagA of Array.from(tagsA)) {
            tagA.style.color = corA
        }
    }

    if (tagsP) {
        for (let tagP of Array.from(tagsP)) {
            tagP.style.color = corTexto
        }
    }

    if (bomHorario) {
        bomHorario.innerText = `${msgBomHorario}`
    }
}

horarioFavicon()
