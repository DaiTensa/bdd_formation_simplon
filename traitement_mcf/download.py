import requests  # Used for making HTTP requests to APIs
import json  # Used for handling JSON data
import dateparser  # Provides functions for parsing and manipulating dates
from urllib.parse import urlencode, quote_plus  # Used for encoding query parameters in URLs
import logging
import os
import sys

# Configure logging
# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Create a stream handler
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)


# Base URL for accessing the dataset through the API
BASE_URL = "https://opendata.caissedesdepots.fr/api/explore/v2.1/catalog/datasets/"

# Specify the dataset ID used in the API request
DATASET_ID = "moncompteformation_catalogueformation"

# Define the format in which data will be requested (e.g., JSON)
FORMAT_DATA = "json"

# Define the field name for the date of extraction in the dataset
DATE_EXTRACT_ITEM = "date_extract"

# File to store the last update date
DATE_FILE = 'last_update_date.txt'
# DATE_FILE = '/mnt/azure/last_update_date.txt' # Chemin du fichier sur Azure

# Query parameters to refine the dataset request
query_params = {
    # Uncomment the line below to specify particular fields to select from the dataset
    #"select": "date_extract, nom_of, nom_departement, nom_region, type_referentiel, code_rncp, code_inventaire, intitule_certification, libelle_niveau_sortie_formation, code_formacode_1, code_formacode_2, code_formacode_3, code_formacode_4, code_formacode_5, libelle_code_formacode_principal, libelle_nsf_1, code_nsf_1, code_nsf_2, code_nsf_3, code_certifinfo, siret, intitule_formation, points_forts, nb_action, nb_session_active, nb_session_a_distance, nombre_heures_total_min, nombre_heures_total_max, nombre_heures_total_mean, frais_ttc_tot_min, frais_ttc_tot_max, frais_ttc_tot_mean, code_departement, code_region",
    
    # Filter to include only records where 'libelle_nsf_1' is like the given value
    "where": 'libelle_nsf_1 like "Informatique, traitement de l\'information, réseaux de transmission"',

    # Limit the number of records returned to -1, which means no limit (retrieve all records)
    "limit": -1,

    # Offset for pagination, set to 0 to start from the beginning
    "offset": 0,

    # Timezone for the data returned, set to UTC
    "timezone": "UTC",

    # Whether to include links in the response, set to false to exclude
    "include_links": "false",

    # Whether to include metadata about the app in the response, set to false to exclude
    "include_app_metas": "false"
}

# Encode the query parameters dictionary into a URL-encoded format
# 'quote_via=quote_plus' ensures that spaces are replaced with '+' signs in the query string
encoded_query_params = urlencode(query_params, quote_via=quote_plus)

# Construct the final URL by appending the encoded query parameters to the base URL
# This forms the complete URL for making the API request with all specified query parameters
URL = f"{BASE_URL}{DATASET_ID}/exports/{FORMAT_DATA}?{encoded_query_params}"

# Construct the URL to get the last update date from the dataset
# This URL will request the most recent record's date of extraction
URL_UPDATE_DATE = f"{BASE_URL}{DATASET_ID}/records?select={DATE_EXTRACT_ITEM}&limit=1&offset=0&timezone=UTC&include_links=false&include_app_metas=false"

def get_last_update_date_from_file():
    """Retrieve the last update date from the file. If the file doesn't exist, create it with a default date."""
    default_date = "2000-01-01"  # La date par défaut à utiliser si le fichier n'existe pas

    # Vérifiez si le fichier existe déjà

    if not os.path.exists(DATE_FILE):
        # Si le fichier n'existe pas, créez-le et écrivez la date par défaut
        with open(DATE_FILE, 'w') as file:
            file.write(default_date)
        # Retournez la date par défaut après avoir créé le fichier
        return default_date
    
    # Si le fichier existe, lisez et retournez son contenu
    with open(DATE_FILE, 'r') as file:
        return file.read().strip()

def save_last_update_date_on_file(date):
    """Save the last update date to the file."""
    with open(DATE_FILE, 'w') as file:
        file.write(date)

def get_last_update_date(url_to_last_date, item_to_extract):
    """Fetch the last update date from the moncompteformation API."""
    response = requests.get(url_to_last_date)
    response.raise_for_status()
    last_update_date = response.json()
    return last_update_date["results"][0][item_to_extract]

def download_json_data(url_to_json):
    """Download JSON data if there is a new update."""
    try:
        # Retrieve the last update date from moncompteformation site
        last_update_date = get_last_update_date(url_to_last_date=URL_UPDATE_DATE, item_to_extract=DATE_EXTRACT_ITEM)

        # Retrieve the last update date stored in the local file
        current_update_date = get_last_update_date_from_file()

        # Compare the dates to determine if a new update is available
        if dateparser.parse(last_update_date) > dateparser.parse(current_update_date):
            logging.info(f"New update found: {last_update_date}")

            # Perform an HTTP request to download the JSON data
            logging.info(f"Download data in progress...")
            response = requests.get(url_to_json)
            response.raise_for_status() # Check if the HTTP request failed

            # Convert the HTTP response to JSON
            data_formation_json = response.json()
            
            # Check if the JSON data is empty
            if not data_formation_json:
                logging.info("No data found.")
            else:
                # Save the last update date to the local file
                save_last_update_date_on_file(date=last_update_date)
                
                # Write the JSON data to a local file
                # utiliser with open('data/data_formation.json') en local '/mnt/azure/data_formation.json' azure
                with open('data/data_formation.json', 'w', encoding='utf-8') as json_file:
                    json.dump(data_formation_json, json_file, ensure_ascii=False, indent=4)

                logging.info("Data download completed successfully, have a nice day!")
        else:
            logging.info("No new updates")
                
    except requests.exceptions.RequestException as e:
        # Handle all HTTP request-related exceptions
        logging.error(f"HTTP request error: {e}")
    except json.JSONDecodeError as e:
        # Handle JSON decoding errors
        logging.error(f"JSON decoding error: {e}")
    except Exception as e:
        # Handle all other exceptions
        logging.error(f"An error occurred: {e}")


if __name__ == "__main__":
   download_json_data(url_to_json=URL)