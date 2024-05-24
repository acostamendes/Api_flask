from flask import Flask, request, jsonify
from flask_restful  import Resource, Api
from sqlalchemy import create_engine, text
from flask import jsonify
from sqlalchemy import text
from flask import make_response

#Flask: É o framework web utilizado para criar a aplicação web.
#request: Permite acessar os dados enviados nas solicitações HTTP.
#jsonify: Transforma objetos Python em respostas JSON válidas.
#Resource: Classe base para definir recursos RESTful.
#Api: Facilita a criação de APIs RESTful em Flask.
#create_engine: Cria uma conexão com o banco de dados SQLAlchemy.
#text: Cria um objeto de texto para representar uma instrução SQL.
#make_response: Cria uma resposta HTTP personalizada.

#db_connect -> representa a conexão com o banco de dados. (fornecido pela a bibliotece "sqlalchemy")
#create_engine('sqlite://bd_api_flask') -> criar uma conexão com esse bando de dados 
db_connect = create_engine('sqlite:///bd_api_flask')

create_table_sql = """
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    celular TEXT NOT NULL
);
"""
# Executar o Script SQL para criar a tabela 'user'
    #conn -> executar consultar no banco de dados

with db_connect.connect() as conn:
    #como para criar a table 'users' no banco de dados.
    conn.execute(text(create_table_sql))

#Inicialização do aplicativo Flask e da Api
app = Flask(__name__)
api = Api(app)

class Users(Resource):
    def get(self):
        #Método GET: retorna todos os usuários do banco de dados
        conn = db_connect.connect()
        #Criar a consulta SQL com um objeto TextClause
        query = conn.execute(text("SELECT * FROM users"))
        #Formatar o rsultado como um dicionário e retornar como JSON
        result = [dict(zip(tuple(query.keys()), i))for i in query.cursor]
        return jsonify(result)
    
    def post(self):
        try:
            conn = db_connect.connect()
            name = request.json['name']
            email = request. json['email']
            celular = request.json['celular']

            #Criar a instrução SQL compilida com SQLAlchemy
            stmt = text("INSERT INTO user(name, email, celular) VALUES(:name, :email, :celular)")

            #Executar a instrução SQL compiliada passando os parâmetros como um dicionário
            conn.execute(stmt, {"name":name, "email": email, "celular": celular})        

            #consulta para obter o registro recém-inserido
            query = conn.execute
            result = [dict(zip(tuple(query.keys()), i))for i in query.cursor]
            response = make_response(jsonify(result), 201)
            return response 
        except Exception as e:

            app.logger.error(f"Erro durante a operação: {str(e)}")
            response = make_response(jsonify({'messange':'Ocorreu um erro durante a operação'}),500)
            return response





if __name__ == '__main__':
    app.run()
