function horarioFavicon() {
    let agora = new Date()
    let hora = agora.getHours()
    let minuto = agora.getMinutes()

    hora = String(hora).length == 1? '0' + hora : hora
    minuto = String(minuto).length == 1? '0' + minuto : minuto

    let meuFavicon
    let msgBomHorario

    if (hora > 0 && hora < 5) {
        corBomHorario = white
        document.body.style.background = 'black'
        meuFavicon = '../static/favicons/favicon-madrugada.ico'
        msgBomHorario = 'Boa madrugada!'
    } else if (hora < 12) {
        document.body.style.background = 'rgb(112, 168, 187)'
        meuFavicon = '../static/favicons/favicon-manha.ico'
        msgBomHorario = 'Bom dia!'
    } else if (hora < 18) {
        document.body.style.background = 'orange'
        meuFavicon = '../static/favicons/favicon-tarde.ico'
        msgBomHorario = 'Boa tarde!'
    } else if (hora <= 24) {
        corBomHorario = 'white'
        document.body.style.background = 'purple'
        meuFavicon = '../static/favicons/favicon-noite.ico'
        msgBomHorario = 'Boa noite!'
    }

    try {
        let bomHorario = document.getElementById('bomHorario')
        bomHorario.innerText = `${msgBomHorario}`
        bomHorario.style.color = `${corBomHorario}` || 'black'
    } catch(e) {}

    let link = document.querySelector("link[rel*='icon']") || document.createElement('link');
    link.type = 'image/x-icon';
    link.rel = 'shortcut icon';
    link.href = meuFavicon;
    head = document.getElementsByTagName('head')[0]
    head.appendChild(link);

}

horarioFavicon()
