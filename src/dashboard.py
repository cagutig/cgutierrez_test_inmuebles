import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
from google.cloud import bigquery
from google.oauth2 import service_account

# Ruta al archivo de credenciales
CREDENTIALS_PATH = r"C:\Users\carlo\Downloads\scraping_proyect\credentials\papyrus-technical-test-727542e11411.json"

# Configurar cliente de BigQuery
credentials = service_account.Credentials.from_service_account_file(CREDENTIALS_PATH)
client = bigquery.Client(credentials=credentials, project=credentials.project_id)

# Función para cargar y procesar datos desde BigQuery
def load_data_from_bigquery(table_name):
    query = f"""
    SELECT *
    FROM `papyrus-technical-test.db_arrendamientos_cgutierrez.{table_name}`
    """
    query_job = client.query(query)
    df = query_job.to_dataframe()
    # Procesamiento de datos
    df['Precio'] = df['Precio'].str.replace('[$,]', '', regex=True).astype(float)
    df['Área'] = df['Área'].str.replace('m2', '').astype(float)
    df['Precio_m2'] = df['Precio'] / df['Área']
    df = df.dropna(subset=['Latitud', 'Longitud', 'Precio_m2'])  # Filtrar valores nulos
    return df

# Cargar datos de arriendos y ventas
try:
    data_arriendo = load_data_from_bigquery('arriendo')
    print("Datos de arriendo cargados y procesados correctamente.")
    data_venta = load_data_from_bigquery('venta')
    print("Datos de venta cargados y procesados correctamente.")
except Exception as e:
    print(f"Error al cargar datos desde BigQuery: {e}")
    exit()

# Inicializar Dash
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1('Mapas de Calor de Propiedades'),
    
    html.Div([
        html.H2('Arriendos'),
        dcc.Dropdown(
            id='dropdown-arriendo',
            options=[{'label': barrio, 'value': barrio} for barrio in data_arriendo['Barrio'].unique()],
            placeholder='Selecciona un barrio para arriendos',
        ),
        dcc.Graph(id='heatmap-arriendo'),
    ]),

    html.Div([
        html.H2('Ventas'),
        dcc.Dropdown(
            id='dropdown-venta',
            options=[{'label': barrio, 'value': barrio} for barrio in data_venta['Barrio'].unique()],
            placeholder='Selecciona un barrio para ventas',
        ),
        dcc.Graph(id='heatmap-venta'),
    ]),
])

@app.callback(
    Output('heatmap-arriendo', 'figure'),
    Input('dropdown-arriendo', 'value')
)
def update_heatmap_arriendo(barrio):
    filtered_data = data_arriendo if not barrio else data_arriendo[data_arriendo['Barrio'] == barrio]
    fig = px.density_mapbox(
        filtered_data,
        lat='Latitud',
        lon='Longitud',
        z='Precio_m2',
        radius=10,
        center=dict(lat=6.2442, lon=-75.5812),  # Coordenadas de Medellín
        zoom=12,
        mapbox_style="open-street-map",
        title=f'Mapa de Calor (Arriendos): Precio/m² en {"todo Medellín" if not barrio else barrio}'
    )
    return fig

@app.callback(
    Output('heatmap-venta', 'figure'),
    Input('dropdown-venta', 'value')
)
def update_heatmap_venta(barrio):
    filtered_data = data_venta if not barrio else data_venta[data_venta['Barrio'] == barrio]
    fig = px.density_mapbox(
        filtered_data,
        lat='Latitud',
        lon='Longitud',
        z='Precio_m2',
        radius=10,
        center=dict(lat=6.2442, lon=-75.5812),  # Coordenadas de Medellín
        zoom=12,
        mapbox_style="open-street-map",
        title=f'Mapa de Calor (Ventas): Precio/m² en {"todo Medellín" if not barrio else barrio}'
    )
    return fig

if __name__ == '__main__':
    app.run_server(debug=True, port=8050)
