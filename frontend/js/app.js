// URL da nossa API Pyhton(Flask)
const API_URL = 'http://127.0.0.1:5000/api/ativos';


/**
 * Função responsavel por buscar os dados no backend e atualizar a tabela de ativos
 */
async function carregarAtivos() {
    try {
        // fetch para buscar os dados da API e await para esperar a resposta
        const resposta = await fetch(API_URL);
        const ativos = await resposta.json();

        // Seleciona o corpo da tabela
        const tbody = document.getElementById('tabela-ativos');
        tbody.innerHTML = ''; // Limpa o conteúdo atual da tabela

        //Percorre cada ativo e cria uma linha na tabela
        ativos.forEach(ativo => {
            // nova linha try
            const tr = document.createElement('tr');

            //Preenche as colunas da linha com os dados do ativo
            tr.innerHTML = ` 
                <td class="ps-3 fw-bold text-secondary">#${ativo.id}</td>
                <td class="fw-semibold">${ativo.nome_moeda}</td>
                <td><span class="budge bg-secondary">${ativo.sigla}</span></td>
                <td>${ativo.quantidade}</td>
                <td>R$ ${ativo.valor_investido.toFixed(2)}</td>
                <td>${formatarData(ativo.data_aporte)}</td>
                <td class="text-end pe-3">
                    <button class="btn btn-sm btn-outiline-primary me-1" title="Editar">
                        <i class="bi bi-pencil"></i>
                    </button>
                    <button class="btn btn-sm btn-outiline-danger" title="Excluir">
                        <i class="bi bi-trash"></i>
                    </button>
                </td>
            `;
            tbody.appendChild(tr); // Adiciona a linha na tabela
        });
    } catch (erro) {
        console.error("Erro ao carregar os ativos:", erro);
        alert("Ocorreu um erro ao carregar os ativos. Por favor, tente novamente mais tarde.");
    }
}

/**
 * Função para formatar a data no formato DD/MM/AAAA
 */
function formatarData(dataString) {
    if (!dataString) return '-';
    // O SQLite pega os horario junto, vou utilizar somente a data
    const dataParte = dataString.split(' ')[0];
    const [ano, mes, dia] = dataParte.split('-');
    return `${dia}/${mes}/${ano}`;
}

//Depois do HTML ser carregado, chama a função para carregar os ativos
document.addEventListener('DOMContentLoaded', carregarAtivos);

/**
 * Função que captura os dados do formulario html
 */
async function salvarAporte() {
    // Captura os dados digitados
    const nome = document.getElementById('nome_moeda').value;
    const sigla = document.getElementById('sigla').value;
    // convertendo texto para numero, para o banco de dados
    const quantidade = parseFloat(document.getElementById('quantidade').value);
    const valor = parseFloat(document.getElementById('valor_investido').value);

    //monta o Json
    const novoAporte = {
        nome_moeda: nome,
        sigla: sigla,
        quantidade: quantidade,
        valor_investido: valor
    };

    try {
        //Requisição POST para o Flask
        const resposta = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(novoAporte)
        });

        if (!resposta.ok) {
            // Se a resposta for OK
            const modal = bootstrap.Modal.getInstance(document.getElementById('modalAporte')).hide();

            //Limpa os dados do formulario
            document.getElementById('form-aporte').reset();

            carregarAtivos();
        } else {
            alert("Erro ao salvar o aporte!!")
        }

    } catch (erro) {
        console.error("Erro ao salvar o aporte:", erro);
        alert("Falha na comunicação com o servidor.");
    }
}