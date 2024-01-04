import argparse
from outils.db_analyser.db_analyser import DB_Analyser_Code

parser = argparse.ArgumentParser(description='Analyse projet microservice')
parser.add_argument('-r', type=str, help='Repository github', required=True)
parser.add_argument('-t', type=str, help='Token github', required=True)

if __name__ == "__main__":
    # Analyser les arguments de la ligne de commande
    args = parser.parse_args()

    # Accéder aux valeurs des arguments
    repository_github = args.r
    token_github = args.t

    db_analyser_Code = DB_Analyser_Code(token_github)