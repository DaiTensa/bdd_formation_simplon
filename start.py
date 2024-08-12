import os
import time, subprocess
#from TRAITEMENT_MCF.download import download_json_data, URL
from TRAITEMENT_MCF.treat_files import load_data
import logging
import sys

def get_mcf_data():
    """
    This functions check 'Mon compte formation' fro new data and download them.

    No argument required
    """

    # BASIC SETTINGS & INITIALIZATION
    command = ['poetry', 'run', 'python', '-u', 'download.py']
    spider_directory = os.path.join(os.path.dirname(__file__), 'TRAITEMENT_MCF')

    # RUNNING THE SCRAPER
    print("Récupération des données depuis Mon Compte Formation...")
    command = subprocess.run(command,
                             cwd = spider_directory,
                             text=True,
                             capture_output=True)
    
    # POTENTIAL EXCEPTION MANAGEMENT
    if command.returncode == 0:
        print("Synchronisation site MonCompteFormation réussie.")
        load_data()
        #print(command.stdout)
    else:
        print('Echec de la synchronisation avec MonCompteFromation')
        print(command.stderr)
    pass

def scrape_simplon_trainings():
    """
    Run the Scrapy spider named 'simplonspiderformation' to scrape trainings.
    """

    # BASIC SETTINGS & INITIALIZATION
    command = ["poetry", "run", "scrapy", "crawl", "simplonspiderformation"]
    spider_directory = os.path.join(os.path.dirname(__file__), 'SCRAPER', 'crawl_simplon', 'crawl_simplon')

    # RUNNING THE SCRAPER
    print("Scraping des formations sur le site web de Simplon.co...")
    try:
        result = subprocess.run(command,
                                cwd=spider_directory,
                                text=True,
                                capture_output=True,
                                encoding='utf-8',
                                check=True)
        print("Scraping des formations terminé avec succès.")
        print(result.stdout)
    except UnicodeDecodeError as e:
        print("Erreur de décodage des caractères.")
        print(str(e))
        # Affichage des données brutes pour diagnostic
        print("Sortie brute stdout:")
        print(result.stdout)
        print("Sortie brute stderr:")
        print(result.stderr)
    except subprocess.CalledProcessError as e:
        print('Le processus de scraping a rencontré des erreurs.')
        print(f"Code de retour : {e.returncode}")
        print(f"Erreur : {e.stderr}")
    except Exception as e:
        print('Une erreur inattendue est survenue.')
        print(str(e))

def scrape_simplon_sessions():
    """
    Run the Scrapy spider named 'simplonspidersession' to scrape sessions.
    """

    # BASIC SETTINGS & INITIALIZATION
    command = ["poetry", "run", "scrapy", "crawl", "simplonspidersession"]
    spider_directory = os.path.join(os.path.dirname(__file__), 'SCRAPER', 'crawl_simplon', 'crawl_simplon')

    # RUNNING THE SCRAPER
    print("Scraping des sessions sur le site web de Simplon.co...")
    try:
        result = subprocess.run(command,
                                cwd=spider_directory,
                                text=True,
                                capture_output=True,
                                encoding='utf-8',
                                check=True)
        print("Scraping des sessions terminé avec succès.")
        print(result.stdout)
    except UnicodeDecodeError as e:
        print("Erreur de décodage des caractères.")
        print(str(e))
        # Affichage des données brutes pour diagnostic
        print("Sortie brute stdout:")
        print(result.stdout)
        print("Sortie brute stderr:")
        print(result.stderr)
    except subprocess.CalledProcessError as e:
        print('Le processus de scraping a rencontré des erreurs.')
        print(f"Code de retour : {e.returncode}")
        print(f"Erreur : {e.stderr}")
    except Exception as e:
        print('Une erreur inattendue est survenue.')
        print(str(e))


if __name__ == '__main__':
    #print(type(URL))
    #print(URL)
    
    scrape_simplon_trainings()
    scrape_simplon_sessions()
    # get_mcf_data()
    pass