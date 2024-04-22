# app.py

import os
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='C:\gdp\Gerenciador-Despesas-Pessoais')

# Configuração do banco de dados SQLite
db_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'despesas.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Definição do modelo de Despesa
class Despesa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    categoria = db.Column(db.String(100), nullable=False)

# Rota para a página inicial
@app.route('/')
def index():
    # Consultar todas as despesas no banco de dados
    despesas = Despesa.query.all()
    return render_template('index.html', despesas=despesas)

# Rota para adicionar uma nova despesa ao banco de dados
@app.route('/adicionar_despesa', methods=['POST'])
def adicionar_despesa():
    try:
        nome = request.json['nome']
        valor = float(request.json['valor'].replace(',', '.'))  # Substitui vírgula por ponto
        categoria = request.json['categoria']
        despesa = Despesa(nome=nome, valor=valor, categoria=categoria)
        db.session.add(despesa)
        db.session.commit()
        return jsonify({'mensagem': 'Despesa adicionada com sucesso!'})
    except Exception as e:
        db.session.rollback()
        print("Erro ao adicionar despesa:", str(e))
        return jsonify({'mensagem': 'Erro ao adicionar despesa. Verifique o console para mais informações.'}), 500
    
# Rota para editar uma despesa existente no banco de dados
@app.route('/editar_despesa/<int:id>', methods=['PUT'])
def editar_despesa(id):
    try:
        despesa = db.session.query(Despesa).get_or_404(id)
        
        nome = request.json.get('nome', despesa.nome)
        valor = float(request.json.get('valor', despesa.valor))
        categoria = request.json.get('categoria', despesa.categoria)

        despesa.nome = nome
        despesa.valor = valor
        despesa.categoria = categoria

        db.session.commit()
        return jsonify({'mensagem': 'Despesa editada com sucesso!'})
    except Exception as e:
        db.session.rollback()
        print("Erro ao editar despesa:", str(e))
        return jsonify({'mensagem': 'Erro ao editar despesa. Verifique o console para mais informações.'}), 500

# Rota para remover uma despesa do banco de dados
@app.route('/remover_despesa/<int:id>', methods=['DELETE'])
def remover_despesa(id):
    try:
        despesa = db.session.query(Despesa).get_or_404(id)
        db.session.delete(despesa)
        db.session.commit()
        return jsonify({'mensagem': 'Despesa removida com sucesso!'})
    except Exception as e:
        db.session.rollback()
        print("Erro ao remover despesa:", str(e))
        return jsonify({'mensagem': 'Erro ao remover despesa. Verifique o console para mais informações.'}), 500

# Rota para listar todas as despesas do banco de dados
@app.route('/listar_despesas')
def listar_despesas():
    despesas = Despesa.query.all()
    despesas_json = [{'nome': despesa.nome, 'valor': despesa.valor, 'categoria': despesa.categoria} for despesa in despesas]
    return jsonify(despesas_json)


if __name__ == '__main__':
    with app.app_context():  #criar o banco de dados dentro da aplicação Flask
        if not os.path.exists(db_path):
            db.create_all()
    app.run(debug=True)

