from flask import Flask, render_template, request

app = Flask(__name__)

# Rota para a página inicial
@app.route('/')
def index():
    return render_template('definir_orcamento.html')

# Rota para lidar com o envio dos dados do formulário
@app.route('/definir_orcamento', methods=['POST'])
def definir_orcamento():
    limite = request.form['limite']
    categoria = request.form['categoria']
    
    # lógica para definir o orçamento no backend

    # Por enquanto, vamos apenas imprimir os valores
    print(f'Limite: {limite}, Categoria: {categoria}')
    
    # Redirecionar de volta para a página inicial
    return render_template('definir_orcamento.html')

if __name__ == '__main__':
    app.run(debug=True)
