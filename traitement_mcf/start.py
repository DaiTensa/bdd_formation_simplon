import os
import subprocess
import treat_files
import sys


def get_mcf_data():
    """
    This functions check 'Mon compte formation' fro new data and download them.

    No argument required
    """

    # BASIC SETTINGS & INITIALIZATION
    command = ['python', '-u', 'download.py']
    spider_directory = os.path.join(os.path.dirname(__file__))

    # RUNNING THE SCRAPER
    print("Récupération des données depuis Mon Compte Formation...")
    command = subprocess.run(command,
                             cwd = spider_directory,
                             text=True,
                             capture_output=True)
    
    # Display the logs from download.py
    print(command.stdout)
    print(command.stderr, file=sys.stderr)
    
    # POTENTIAL EXCEPTION MANAGEMENT
    if command.returncode == 0:
        print("Synchronisation site MonCompteFormation réussie.")
        treat_files.load_data()
        #print(command.stdout)
    else:
        print('Echec de la synchronisation avec MonCompteFromation')
        print(command.stderr)
    pass

if __name__ == '__main__':
    print(os.path.dirname(__file__))
    get_mcf_data()
    pass