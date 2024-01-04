import argparse
from outils.db_analyser.db_analyser import DB_analyser
from utils.Colors import Couleurs

parser = argparse.ArgumentParser(description='Analyse projet microservice')
parser.add_argument('-r', type=str, help='Repository github', required=True)
parser.add_argument('-t', type=str, help='Token github', required=True)

# TODO : génération d'un .csv pour chaque service dans le dossier ./datas
# TODO : faire des readme dans chaque service
# TODO : faire des dossier et des classes pour chaque outils présent dans le dossier analyse_microservice

if __name__ == "__main__":
    args = parser.parse_args()
    repository_github = args.r
    token_github = args.t

    # INIT
    db_analyser = DB_analyser(token_github)

    # RUN
    db_analyser_Code_resultat = db_analyser.run(repository_github)

    # SAVE
    # TODO : Save les resultats dans le .csv final
    print(Couleurs.VERT+"\n\n==========================================\n\tRESULTAT FINAL\n\n"+Couleurs.RESET)
    print("[ "+Couleurs.VERT+"DB analyser resultat"+Couleurs.RESET+" ] : ", db_analyser_Code_resultat)




    print("\n\n")