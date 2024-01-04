import argparse
from utils.Colors import Couleurs
from outils.db_analyser.db_analyser import DB_analyser
from outils.docker_compose_presence_detection.docker_compose_presence_detection import Docker_compose_presence_detection
from outils.gateway.gateway import Gateway

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
    docker_compose_presence_detection = Docker_compose_presence_detection(token_github)
    db_analyser = DB_analyser(token_github)
    gateway = Gateway(token_github)

    # RUN
    docker_compose_presence_detection_resultat = docker_compose_presence_detection.run(repository_github)
    gateway_resultat = gateway.run(repository_github)
    db_analyser_Code_resultat = db_analyser.run(repository_github)

    # SAVE
    # TODO : Save les resultats dans le .csv final
    print(Couleurs.VERT+"\n\n==========================================\n\tRESULTAT FINAL\n\n"+Couleurs.RESET)
    if docker_compose_presence_detection_resultat:
        print("[ "+Couleurs.VERT+"Docker compose present"+Couleurs.RESET+" ] : ", docker_compose_presence_detection_resultat)
    else:
        print("[ "+Couleurs.ROUGE+"Docker compose present"+Couleurs.RESET+" ] : ", docker_compose_presence_detection_resultat)

    if gateway_resultat:
        print("[ "+Couleurs.VERT+"Gateway present"+Couleurs.RESET+" ] : ", gateway_resultat)
    else:
        print("[ "+Couleurs.ROUGE+"Gateway present"+Couleurs.RESET+" ] : ", gateway_resultat)

    print("[ "+Couleurs.JAUNE+"DB analyser resultat"+Couleurs.RESET+" ] : ", db_analyser_Code_resultat)




    print("\n\n")