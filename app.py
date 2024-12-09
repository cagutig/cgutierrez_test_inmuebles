from google.cloud import bigquery
from google.oauth2 import service_account
import pandas as pd
import os


CREDENTIALS_PATH = '/app/credentials/papyrus-technical-test-727542e11411.json'

# Configura el cliente de BigQuery
def get_bigquery_client():
    credentials = service_account.Credentials.from_service_account_file(CREDENTIALS_PATH)
    return bigquery.Client(credentials=credentials, project=credentials.project_id)

# Función para cargar un DataFrame y crear la tabla si no existe
def load_to_bigquery(df, table_id):
    """Carga un DataFrame a BigQuery y crea la tabla si no existe."""
    client = get_bigquery_client()
    project_id = client.project

    # Configurar referencia a la tabla
    table_ref = client.dataset("db_arrendamientos_cgutierrez").table(table_id)

    # Configuración del job de carga
    job_config = bigquery.LoadJobConfig(
        write_disposition="WRITE_APPEND",  # Realiza un append a la tabla
        autodetect=True,  # Autodetectar el esquema
        source_format=bigquery.SourceFormat.CSV,  # Cambiar a CSV si es necesario
    )

    # Inicia el trabajo de carga
    job = client.load_table_from_dataframe(df, table_ref, job_config=job_config)
    job.result()  # Espera a que el trabajo se complete

    print(f"Datos cargados o tabla creada en {table_id} del dataset db_arrendamientos_cgutierrez en el proyecto {project_id}")


# Función principal para cargar los datos
def upload_to_bigquery():
    """Lee los CSV generados y carga los datos en BigQuery."""
    try:
        # Verificar si existen los archivos CSV generados
        if os.path.exists("detalles_venta.csv"):
            df_venta = pd.read_csv("detalles_venta.csv")
            print(f"Cargando {len(df_venta)} registros a la tabla 'venta' en BigQuery...")
            load_to_bigquery(df_venta, "venta")

        if os.path.exists("detalles_arrendamiento.csv"):
            df_arrendamiento = pd.read_csv("detalles_arrendamiento.csv")
            print(f"Cargando {len(df_arrendamiento)} registros a la tabla 'arriendo' en BigQuery...")
            load_to_bigquery(df_arrendamiento, "arriendo")

    except Exception as e:
        print(f"Error al cargar datos a BigQuery: {e}")