function horarioFavicon() {
    let agora = new Date()
    let hora = agora.getHours()
    let minuto = agora.getMinutes()

    hora = String(hora).length == 1? '0' + hora : hora
    minuto = String(minuto).length == 1? '0' + minuto : minuto

    let meuFavicon

    let msgBomHorario = document.getElementById("bomHorario")

    if (hora > 0 && hora < 5) {
        document.body.style.background = 'black'
        msgBomHorario.innerText = 'Boa madrugada!'
        msgBomHorario.style.color = 'white'
        meuFavicon = '../static/favicons/favicon-madrugada.ico'
    } else if (hora < 12) {
        document.body.style.background = 'rgb(112, 168, 187)'
        msgBomHorario.innerText = 'Bom dia!'
        meuFavicon = '../static/favicons/favicon-manha.ico'
    } else if (hora < 18) {
        document.body.style.background = 'orange'
        msgBomHorario.innerText = 'Boa tarde!'
        meuFavicon = '../static/favicons/favicon-tarde.ico'
    } else if (hora <= 24) {
        document.body.style.background = 'purple'
        msgBomHorario.innerText = 'Boa noite!'
        msgBomHorario.style.color = 'white'
        meuFavicon = '../static/favicons/favicon-noite.ico'
    }

    let link = document.querySelector("link[rel*='icon']") || document.createElement('link');
    link.type = 'image/x-icon';
    link.rel = 'shortcut icon';
    link.href = meuFavicon;
    head = document.getElementsByTagName('head')[0]
    head.appendChild(link);

}

horarioFavicon()
