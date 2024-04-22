from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///orcamentos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Orcamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    categoria = db.Column(db.String(100), nullable=False)
    valor = db.Column(db.Float, nullable=False)

@app.route('/')
def index():
    orcamentos = Orcamento.query.all()
    return render_template('index.html', orcamentos=orcamentos, mensagem=None)

@app.route('/adicionar_orcamento', methods=['POST'])
def adicionar_orcamento():
    categoria = request.form['categoria']
    valor = float(request.form['valor'])  # Convertendo para float

    novo_orcamento = Orcamento(categoria=categoria, valor=valor)
    db.session.add(novo_orcamento)
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/editar_orcamento/<int:id>', methods=['POST'])
def editar_orcamento(id):
    orcamento = Orcamento.query.get_or_404(id)
    orcamento.categoria = request.form['categoria']
    orcamento.valor = float(request.form['valor'])  # Convertendo para float
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/remover_orcamento/<int:id>', methods=['POST'])
def remover_orcamento(id):
    orcamento = Orcamento.query.get_or_404(id)
    db.session.delete(orcamento)
    db.session.commit()

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
