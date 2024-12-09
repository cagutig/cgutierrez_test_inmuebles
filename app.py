import logging
from src.scraping_urls import scrape_urls
from src.scraping_details import scrape_details
from src.bigquery_upload import upload_to_bigquery  
from flask import Flask
import os

app = Flask(__name__)

@app.route("/")
def main():
    logging.basicConfig(level=logging.INFO)
    logging.info("Iniciando el proceso de scraping...")

    try:
        # Paso 1: Scraping de URLs
        logging.info("Extrayendo URLs de propiedades...")
        scrape_urls()

        # Paso 2: Scraping de detalles
        logging.info("Extrayendo detalles de propiedades...")
        scrape_details()

        # Paso 3: Subir datos a BigQuery
        logging.info("Cargando datos en BigQuery...")
        upload_to_bigquery()

        logging.info("Proceso completado exitosamente.")
        return "Scraping completado y datos cargados a BigQuery", 200
    except Exception as e:
        logging.error(f"Error durante el proceso de scraping: {e}")
        return f"Error: {e}", 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))  # Leer el puerto desde la variable de entorno
    app.run(host="0.0.0.0", port=port)
