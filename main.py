import argparse

parser = argparse.ArgumentParser(description='Analyse projet microservice')
parser.add_argument('-r', type=str, help='Repository github', required=True)
parser.add_argument('-t', type=str, help='Token github')

if __name__ == "__main__":


    # Analyser les arguments de la ligne de commande
    args = parser.parse_args()

    # Accéder aux valeurs des arguments
    repository_github = args.r
    token_github = args.t
    token_github = "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"

    db_analyser_Code = DB_Analyser_Code(token_github)

