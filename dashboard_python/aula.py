from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
from sqlalchemy import create_engine
import psycopg2


# conexão com a Stage
# Configurar detalhes da conexão
db_params = {
    'dbname': 'stage',
    'user': 'postgres',
    'password': '',
    'host': '192.168.9.105',
    'port': '5432',
}

# Estabelecer a conexão
connection = psycopg2.connect(**db_params)
cursor = connection.cursor()
query = """select extract (year from pes_dat_nasc) as ano_nascimento, pes_ind_sexo as sexo, count(pes_cod) as qtd  
             from sgu.pessoa 
            where pes_ind = 'F' 
            group by extract (year from pes_dat_nasc), pes_ind_sexo"""
cursor.execute(query)
# Recuperar os resultados
resultados = cursor.fetchall()
# Fechar o cursor e a conexão
cursor.close()
connection.close()
# Transformar os resultados em um DataFrame
df = pd.DataFrame(resultados, columns=['ano_nascimento','sexo','qtd'])



app = Dash(__name__)

#df = pd.read_excel("Vendas.xlsx")

# criando o gráfico
fig = px.bar(df, x="ano_nascimento", y="qtd", color="sexo", barmode="group")

opcoes = list(df['sexo'].unique())
opcoes.append("Todos")

app.layout = html.Div(children=[
    html.H1(children='Quantidade de pessoas físicas'),
    html.H2(children='Gráfico com a quantidade de pessoas por ano de nascimento e sexo'),
    dcc.Dropdown(opcoes, value='Todos', id='lista_lojas'),
    dcc.Graph(
        id='grafico_quantidade_vendas',
        figure=fig
    )
])


@app.callback(
    Output('grafico_quantidade_vendas', 'figure'),
    Input('lista_lojas', 'value')
)
def update_output(value):
    if value == "Todos":
        fig = px.bar(df, x="ano_nascimento", y="qtd", color="sexo", barmode="group")
    else:
        tabela_filtrada = df.loc[df['sexo']==value, :]
        fig = px.bar(tabela_filtrada, x="ano_nascimento", y="qtd", color="sexo", barmode="group")
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)