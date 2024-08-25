import os
import subprocess

def scrape_simplon_trainings():
    """
    Run the Scrapy spider named 'simplonspiderformation' to scrape trainings.
    """

    # BASIC SETTINGS & INITIALIZATION
    command = ["scrapy", "crawl", "simplonspiderformation"]
    spider_directory = os.path.join(os.path.dirname(__file__), 'crawl_simplon', 'crawl_simplon')

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
    command = ["scrapy", "crawl", "simplonspidersession"]
    spider_directory = os.path.join(os.path.dirname(__file__), 'crawl_simplon', 'crawl_simplon')

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
    scrape_simplon_trainings()
    scrape_simplon_sessions()
    pass