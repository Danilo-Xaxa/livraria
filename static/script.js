function horarioFavicon() {
    let agora = new Date()
    let hora = agora.getHours()
    let minuto = agora.getMinutes()

    hora = String(hora).length == 1? '0' + hora : hora
    minuto = String(minuto).length == 1? '0' + minuto : minuto

    hora = 03

    let meuFavicon
    let bomHorario

    if (hora > 0 && hora < 5) {
        document.getElementById('bomHorario').style.color = 'white'
        document.body.style.background = 'black'
        meuFavicon = '../static/favicons/favicon-madrugada.ico'
        bomHorario = 'Boa madrugada!'
    } else if (hora < 12) {
        document.body.style.background = 'rgb(112, 168, 187)'
        meuFavicon = '../static/favicons/favicon-manha.ico'
        bomHorario = 'Bom dia!'
    } else if (hora < 18) {
        document.body.style.background = 'orange'
        meuFavicon = '../static/favicons/favicon-tarde.ico'
        bomHorario = 'Boa tarde!'
    } else if (hora <= 24) {
        document.getElementById('bomHorario').style.color = 'white'
        document.body.style.background = 'purple'
        meuFavicon = '../static/favicons/favicon-noite.ico'
        bomHorario = 'Boa noite!'
    }

    let link = document.querySelector("link[rel*='icon']") || document.createElement('link');
    link.type = 'image/x-icon';
    link.rel = 'shortcut icon';
    link.href = meuFavicon;
    head = document.getElementsByTagName('head')[0]
    head.appendChild(link);

    return bomHorario
}

minhaVar = horarioFavicon()

function msgBomHorario() {
    let aqueleH1 = document.getElementById('bomHorario')
    aqueleH1.innerText = minhaVar
}

msgBomHorario()
