from flask import Flask, request, jsonify
from flask_cors import CORS
from database import get_db_connection

# Inicia o aplicativo Flask
app = Flask(__name__)
#Habilita o CORS para permitir que o Front-end acesse a API
CORS(app)

#(READ)
@app.route('/api/ativos', methods=['GET'])
def listar_ativos():
    #Abrindo conexão com banco de dados
    conn = get_db_connection()

    #Executa os comandos SQL para buscar todos os ativos
    ativos = conn.execute('SELECT * FROM ativos').fetchall()
    conn.close()

    #Transforma os resultados em um dicionario Python
    lista_ativos = [dict(ativo) for ativo in ativos]
    #Retorna a lista de ativos em formato JSON
    return jsonify(lista_ativos)

#(CREATE)
@app.route('/api/ativos', methods=['POST'])
def cadastrar_ativo():
    #Lê os dados enviados em formato JSON
    dados = request.get_json()

    #Extrair as info, se faltar alguma coisa, retorna erro
    nome = dados['nome_moeda']
    sigla = dados['sigla']
    quantidade = dados['quantidade']
    valor = dados['valor_investido']

    #Abre a conexao e insere os dados no banco
    conn = get_db_connection()
    conn.execute('''
        INSERT INTO ativos (nome_moeda, sigla, quantidade, valor_investido)
        VALUES (?, ?, ?, ?)
    ''', (nome, sigla, quantidade, valor))
    conn.commit()
    conn.close()

    #retona mensagem de sucesso em JSON
    return jsonify({'message': 'Ativo cadastrado com sucesso!'}), 201

#(READ ONE)
@app.route('/api/ativos/<int:id>', methods=['GET'])
def buscar_ativo(id):
    conn = get_db_connection()
    #o fetchone() retorna apenas o primeiro resultado encontrado
    ativo = conn.execute('SELECT * FROM ativos WHERE id = ?', (id,)).fetchone()
    conn.close()

    if ativo is None:
        return jsonify({'message': 'Ativo não encontrado!'}), 404
    
    ativo_dict = dict(ativo)
    return jsonify(ativo_dict)

#(UPDATE)
@app.route('/api/ativos/<int:id>', methods=['PUT'])
def atualizar_ativo(id):
    dados = request.get_json()
    #Atualiza apenas a quantidade e o valor
    quantidade = dados['quantidade']
    valor = dados['valor_investido']

    conn = get_db_connection()
    conn.execute('''
        UPDATE ativos
        SET quantidade = ?, valor_investido = ?
        WHERE id = ?
    ''', (quantidade, valor, id))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Aporte atualizado com sucesso!'})

#(DELETE)
@app.route('/api/ativos/<int:id>', methods=['DELETE'])
def excluir_ativo(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM ativos WHERE id = ?', (id,))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Aporte excluído com sucesso!'})

#Inicialização do Servidor
if __name__ == '__main__':
    app.run(debug=True, port=5000)