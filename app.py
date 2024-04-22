# app.py

import os
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
import pandas as pd

app = Flask(__name__, template_folder='C:\gdp\Gerenciador-Despesas-Pessoais')

# Configuração do banco de dados SQLite
db_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'despesas.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelo de Despesa
class Despesa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'), nullable=False)  # Corrigido

    categoria = db.relationship('Categoria', backref=db.backref('despesas', lazy=True))

# Modelo de Categoria
class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False, unique=True)

    limite = db.Column(db.Float, nullable=True)  # Limite de gastos para a categoria


# Rota para a página inicial
@app.route('/')
def index():
    # Consultar todas as despesas no banco de dados
    despesas = Despesa.query.all()
    return render_template('index.html', despesas=despesas)


# Rota para adicionar uma nova despesa
@app.route('/adicionar_despesa', methods=['POST'])
def adicionar_despesa():
    try:
        nome = request.json['nome']
        valor = float(request.json['valor'].replace(',', '.'))
        categoria_nome = request.json['categoria']
        
        categoria = Categoria.query.filter_by(nome=categoria_nome).first()
        
        if categoria:
            limite_categoria = categoria.limite
            if limite_categoria is not None:
                total_despesas_categoria = Despesa.query.with_entities(func.sum(Despesa.valor)).filter_by(categoria_id=categoria.id).scalar()
                if total_despesas_categoria is None:
                    total_despesas_categoria = 0
                if total_despesas_categoria + valor > limite_categoria:
                    return jsonify({'mensagem': f'O limite de gastos para a categoria "{categoria_nome}" foi atingido!'}), 400
            else:
                return jsonify({'mensagem': f'A categoria "{categoria_nome}" não possui um limite de gastos definido.'}), 400
            
            despesa = Despesa(nome=nome, valor=valor, categoria_id=categoria.id)
            db.session.add(despesa)
            db.session.commit()
            return jsonify({'mensagem': 'Despesa adicionada com sucesso!'})
        else:
            return jsonify({'mensagem': f'A categoria "{categoria_nome}" não existe.'}), 404
    except Exception as e:
        db.session.rollback()
        print("Erro ao adicionar despesa:", str(e))
        return jsonify({'mensagem': 'Erro ao adicionar despesa. Verifique o console para mais informações.'}), 500

    

# Rota para cadastrar as categorias
@app.route('/cadastrar_categorias', methods=['POST'])
def cadastrar_categorias():
    categorias = [
        {'nome': 'Alimentação', 'limite': 500},
        {'nome': 'Moradia', 'limite': 1000},
        {'nome': 'Transporte', 'limite': 300},
        {'nome': 'Saúde', 'limite': 200},
        {'nome': 'Educação', 'limite': 400},
        {'nome': 'Lazer', 'limite': 200},
        {'nome': 'Vestuário', 'limite': 300},
        {'nome': 'Serviços financeiros', 'limite': 100},
        {'nome': 'Outros', 'limite': 500}
    ]

    for categoria_data in categorias:
        nome = categoria_data['nome']
        limite = categoria_data['limite']
        categoria = Categoria(nome=nome, limite=limite)
        db.session.add(categoria)

    db.session.commit()


# Rota para obter o limite de gastos associado a uma categoria
@app.route('/obter_limite')
def obter_limite():
    categoria_nome = request.args.get('categoria')
    categoria = Categoria.query.filter_by(nome=categoria_nome).first()
    if categoria:
        limite = categoria.limite
    else:
        limite = None
    return jsonify({'limite': limite})

# Rota para listar todas as despesas do banco de dados
@app.route('/listar_despesas')
def listar_despesas():
    despesas = Despesa.query.all()
    despesas_json = [{'nome': despesa.nome, 'valor': despesa.valor, 'categoria': despesa.categoria} for despesa in despesas]
    return jsonify(despesas_json)

# Rota para editar uma despesa existente no banco de dados
@app.route('/editar_despesa/<int:id>', methods=['PUT'])
def editar_despesa(id):
    try:
        despesa = Despesa.query.get_or_404(id)
        
        nome = request.json.get('nome', despesa.nome)
        valor = float(request.json.get('valor', despesa.valor))
        categoria_id = request.json.get('categoria_id', despesa.categoria_id)

        # Verificar se a categoria existe no banco de dados
        categoria = Categoria.query.get(categoria_id)
        if not categoria:
            return jsonify({'mensagem': f'A categoria com o ID {categoria_id} não existe.'}), 400

        despesa.nome = nome
        despesa.valor = valor
        despesa.categoria_id = categoria_id

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
        despesa = Despesa.query.get_or_404(id)
        db.session.delete(despesa)
        db.session.commit()
        return jsonify({'mensagem': 'Despesa removida com sucesso!'})
    except Exception as e:
        db.session.rollback()
        print("Erro ao remover despesa:", str(e))
        return jsonify({'mensagem': 'Erro ao remover despesa. Verifique o console para mais informações.'}), 500
    
def get_dataframe_despesas():
    # Consultar todas as despesas do banco de dados
    despesas = Despesa.query.all()
    
    # Criar uma lista de dicionários com os valores de valor e categoria de cada despesa
    dados_despesas = [{'valor': despesa.valor, 
                       'categoria': despesa.categoria.nome}  # Acessa o nome da categoria diretamente através do objeto de categoria
                      for despesa in despesas]
    
    # Criar DataFrame pandas com os dados das despesas
    dataframe_despesas = pd.DataFrame(dados_despesas)
    
    return dataframe_despesas


if __name__ == '__main__':
    with app.app_context():  #criar o banco de dados dentro da aplicação Flask
        if not os.path.exists(db_path):
            db.create_all()
    app.run(debug=True)

