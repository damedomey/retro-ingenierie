from github import Github, Repository

from utils.Colors import Couleurs


class Docker_compose_presence_detection():
    def __init__(self, token):
        self.__access_token = token

    def run(self, repo_name):
        print("DOCKER COMPOSE PRESENCE DETECTION", flush=True)
        g = Github(self.__access_token)
        repository: Repository = g.get_repo(repo_name)
        return self.__has_docker_compose(repository)

    def __has_docker_compose(self, repository: Repository):
        contents = repository.get_contents("")
        for content in contents:
            if content.name.lower() == 'docker-compose.yml':
                print("[ "+Couleurs.VERT+"DOCKER COMPOSE FOUND"+Couleurs.RESET+" ]")
                return True
        print("[ " + Couleurs.ROUGE + "DOCKER COMPOSE NOT FOUND" + Couleurs.RESET + " ]")
        return False
