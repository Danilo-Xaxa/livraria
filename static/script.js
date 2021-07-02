function horarioBackgroundFavicon() {
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
    let tagsA = document.getElementsByTagName('a')
    let corTexto
    let corA
    

    if (hora >= 0 && hora < 5) {
        meuFavicon = '../static/favicons/favicon-madrugada.ico'
        msgBomHorario = 'Boa madrugada!'
        document.body.style.background = '#000'
        corTexto = '#EFF9F0'
        corA = '#DDC8C4'
    } else if (hora < 12) {
        meuFavicon = '../static/favicons/favicon-manha.ico'
        msgBomHorario = 'Bom dia!'
        document.body.style.background = '#70A8BB'
        corTexto = '#37323E'
        corA = '#C03221'
    } else if (hora < 18) {
        meuFavicon = '../static/favicons/favicon-tarde.ico'
        msgBomHorario = 'Boa tarde!'
        document.body.style.background = '#FFA500'
        corTexto = '#121619'
        corA = '#DD1C1A'
    } else if (hora <= 23) {
        meuFavicon = '../static/favicons/favicon-noite.ico'
        msgBomHorario = 'Boa noite!'
        document.body.style.background = '#800080'
        corTexto = '#FABC2A'
        corA = '#F2EDEB'
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

    if (tagsA) {
        for (let tagA of Array.from(tagsA)) {
            tagA.style.color = corA
        }
    }
}

horarioBackgroundFavicon()


/*
function ajax() {
    // tem que importar jquery, né?
}

ajax()
*/
