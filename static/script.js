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
