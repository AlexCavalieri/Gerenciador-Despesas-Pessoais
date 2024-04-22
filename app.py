import graph
from flask import Flask, render_template

#dataframe_despesas = get_dataframe_despesas()
dataframe_despesas = graph.cria_df_teste()

figura = graph.gera_grafico(dataframe_despesas)

graph.exibir_grafico_html(figura)


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('exibicao_grafico.html')

if __name__ == '__main__':
    app.run(debug=True)
