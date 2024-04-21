from flask import Flask, render_template, request

app = Flask(__name__)

# Rota para a página inicial
@app.route('/')
def index():
    return render_template('inserir_despesa.html')

# Rota para lidar com o envio dos dados do formulário
@app.route('/inserir_despesa', methods=['POST'])
def inserir_despesa():
    valor = request.form['valor']
    categoria = request.form['categoria']
    
    # lógica para inserir os dados no backend

    # Por enquanto, vamos apenas imprimir os valores
    print(f'Valor: {valor}, Categoria: {categoria}')
    
    return render_template('inserir_despesa.html')

if __name__ == '__main__':
    app.run(debug=True)