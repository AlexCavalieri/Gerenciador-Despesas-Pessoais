import pandas as pd
import numpy as np
import plotly.offline as py
import plotly.graph_objs as go

# Gera um grafico com o total de despesa por categoria a partir de um df com despesas e salva em html

def cria_df_teste():
   df = pd.DataFrame({
        'Categoria': np.random.choice(['compras', 'aluguel', 'utilidades', 'viagem', 'outros'], 100),
        'Valor': np.random.randint(100, 1000, 100)
    })
   return df

def gera_grafico(df):
  df_cat = df.groupby('Categoria')['Valor'].sum().sort_values(ascending=False)

  fig = go.Figure()
  fig.add_trace(go.Bar(
      x = df_cat.index,
      y = df_cat.values,
      marker_color = 'teal',
      width = 0.45
  ))

  fig.update_layout(title = 'Total de despesas por categoria',
                  yaxis = dict(title = 'Valor', title_font_size=30),
                  font = dict(size = 20),
                  margin = dict(l = 100, r = 75, t = 100, b = 100),
                  title_font_size=50,
                  title_y=0.95, title_x=0.5,
                  autosize=False, width=1600, height=800,)

  return fig

def exibir_grafico_html(fig, nome_arquivo='templates/graph.html'):
    py.plot(fig, filename=nome_arquivo, auto_open=False)