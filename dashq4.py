from dash import Dash, html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from dash_iconify import DashIconify
import plotly.express as px
import pandas as pd

logoRICARD = "https://thumbnail.imgbin.com/14/24/14/imgbin-pastis-ricard-ap-ritif-drink-liqueur-drink-z3uQ8YaXpLFywMJwWnXgAqBYY_t.jpg"

# Création de l'application
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# To deploy on render
server = app.server

# Exemple de données
df = pd.read_csv("https://raw.githubusercontent.com/chriszapp/datasets/main/books.csv",
                 on_bad_lines='skip').rename(columns={"  num_pages" : "num_pages"})

# Mon graph
fig = px.bar(df.head(10), 
             x ='title',
             y = 'num_pages',
             labels={
                     "num_pages": "Nombre de pages",
                     "title": "Titre",
                 },
             title = '10 premiers livres du dataset')

# Définition du layout 
search_bar = dbc.Row(
    [
        dbc.Col(dbc.Input(id='input-exemple', style = {'height': '30px', 'width': '100px'}, type="text", placeholder="Page max")),
        dbc.Col(dcc.Dropdown(
                id='dropdown-author',
                style = {'height': '30px', 'width': '500px'},
                options = [{'label': i, 'value': i} for i in df['authors'].unique().tolist()],
                placeholder = "Recherche auteur"
                )),
        dbc.Col(
            dbc.Button(
                "Recherche", id='my_button', color="primary", className="ms-2", n_clicks=0
            ),
            width="auto",
        ),
    ],
    className="g-0 ms-auto flex-nowrap mt-3 mt-md-0",
    align="center",
)

navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=logoRICARD, height="30px")),
                        dbc.Col(dbc.NavbarBrand("RICARDGANG", className="ms-2")),
                    ],
                    align="center",
                    className="g-0",
                ),
                href="https://www.ricard.com/",
                style={"textDecoration": "none"},
            ),
            dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
            dbc.Collapse(
                search_bar,
                id="navbar-collapse",
                is_open=False,
                navbar=True,
            ),
        ]
    ),
    color="dark",
    dark=True,
)

app.layout = html.Div([
    navbar, 
    html.P("\n\n"),
    dcc.Graph(id='plotly-graph', figure=fig),
    # html.H2(
    #     "Recherche d'auteurs : ",
    #     style={'color': 'red'}),    
    # # dcc.Dropdown(
    # #     id='dropdown-author',
    # #     options= [{'label': i, 'value': i} for i in df['authors'].unique().tolist()]
    # # ),
    
    # html.P("\n\n"),
    
    # html.H2(
    #     "Pages maximum : ",
    #     style={'color': 'red'}),
    # dcc.Input(id='input-exemple', type='text', value='7000'),
])

@app.callback(
    Output('plotly-graph', 'figure'),
    [State('dropdown-author', 'value')],
    [State('input-exemple', 'value')],
    [Input('my_button', 'n_clicks')]
)

def update_graph(author, pagemax, nclick):
    
    data_filtered = df[(df['authors'] == author) & (df['num_pages'] <= int(pagemax))]
    
    # Créez le graphique
    
    fig = px.bar(data_filtered, 
             x ='title',
             y = 'num_pages',
             labels={
                     "num_pages": "Nombre de pages",
                     "title": "Titre",
                 },
             title = 'Livres de ' + author + ', ayant ' + pagemax + ' pages maximum')
    
    if nclick > 0 :

        return fig


if __name__ == '__main__' : 
    app.run_server(debug=True)

