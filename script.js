const lis = document.document.querySelector('#listinha'); //puxa o que tem dentro

fetch("http://localhost:8000/get_listinha").then((res) => {
    return res.json();
}).then((data) => {
    data.map((lista) => {
        console.log(lista)
        lis.innerHTML += `
        <li>
            <img src="${lista.capa}"/> <br>
            <strong>Nome do Filme:</strong> ${lista.nome} </br>
            <strong>Atores: </strong> ${lista.nome} </br>
            <strong>Diretor (a): </strong> ${lista.nome} </br>
            <strong>Data de Lançamento: </strong> ${lista.nome} </br>
            <strong>Gênero: </strong> ${lista.nome} </br>
            <strong>Sinopse: </strong> ${lista.nome} </br>
            <strong>Produtora: </strong> ${lista.nome} </br>
        </li>

        `
    })
})