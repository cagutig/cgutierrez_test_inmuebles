from flask import Flask, jsonify
from google.cloud import bigquery
from google.oauth2 import service_account

# Inicializar la aplicación Flask
app = Flask(__name__)

# Ruta al archivo de credenciales
CREDENTIALS_PATH = r"C:\Users\carlo\Downloads\scraping_proyect\credentials\papyrus-technical-test-727542e11411.json"

# Configurar cliente de BigQuery
credentials = service_account.Credentials.from_service_account_file(CREDENTIALS_PATH)
client = bigquery.Client(credentials=credentials, project=credentials.project_id)

# Nombres de las tablas en BigQuery
DATASET_ID = "db_arrendamientos_cgutierrez"
ARRENDAMIENTO_TABLE = f"{client.project}.{DATASET_ID}.arriendo"
VENTA_TABLE = f"{client.project}.{DATASET_ID}.venta"


@app.route('/', methods=['GET'])
def home():
    """
    Ruta principal que describe las rutas disponibles en el API.
    """
    return jsonify({
        "message": "API de Propiedades - Rutas disponibles",
        "endpoints": {
            "/api/properties/arriendo": "Devuelve todos los registros de la tabla 'arriendo'",
            "/api/properties/venta": "Devuelve todos los registros de la tabla 'venta'",
            "/api/properties/arriendo/<barrio>": "Filtra los registros de 'arriendo' por 'barrio'",
            "/api/properties/venta/<barrio>": "Filtra los registros de 'venta' por 'barrio'",
        }
    })


@app.route('/api/properties/arriendo', methods=['GET'])
def get_arriendo_properties():
    """
    Devuelve todos los datos de la tabla 'arriendo' en formato JSON.
    """
    query = f"SELECT * FROM `{ARRENDAMIENTO_TABLE}`"
    query_job = client.query(query)
    results = [dict(row) for row in query_job]
    return jsonify(results)


@app.route('/api/properties/venta', methods=['GET'])
def get_venta_properties():
    """
    Devuelve todos los datos de la tabla 'venta' en formato JSON.
    """
    query = f"SELECT * FROM `{VENTA_TABLE}`"
    query_job = client.query(query)
    results = [dict(row) for row in query_job]
    return jsonify(results)


@app.route('/api/properties/arriendo/<string:barrio>', methods=['GET'])
def get_arriendo_properties_by_barrio(barrio):
    """
    Devuelve los datos filtrados por barrio en la tabla 'arriendo'.
    """
    query = f"""
    SELECT * 
    FROM `{ARRENDAMIENTO_TABLE}`
    WHERE Barrio = @barrio
    """
    query_job = client.query(query, job_config=bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("barrio", "STRING", barrio)
        ]
    ))
    results = [dict(row) for row in query_job]
    return jsonify(results)


@app.route('/api/properties/venta/<string:barrio>', methods=['GET'])
def get_venta_properties_by_barrio(barrio):
    """
    Devuelve los datos filtrados por barrio en la tabla 'venta'.
    """
    query = f"""
    SELECT * 
    FROM `{VENTA_TABLE}`
    WHERE Barrio = @barrio
    """
    query_job = client.query(query, job_config=bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("barrio", "STRING", barrio)
        ]
    ))
    results = [dict(row) for row in query_job]
    return jsonify(results)


if __name__ == '__main__':
    app.run(debug=True)
