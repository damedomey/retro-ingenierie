from github import Github, Repository
import re

from utils.Colors import Couleurs


class Gateway():
    def __init__(self, token):
        print("GATEWAY")
        self.__access_token = token

    def run(self, repo_name):
        g = Github(self.__access_token)
        repository: Repository = g.get_repo(repo_name)

        # Dans le compose
        if self.__check_gateway_in_docker_compose(repository):
            print("[ "+Couleurs.VERT+"Gateway in docker compose"+Couleurs.RESET+" ]")
            return True

        if self.__check_gateway_in_pom_files(repository):
            print("[ "+Couleurs.VERT+"Gateway in pom files"+Couleurs.RESET+" ]")
            return True

        print("[ " + Couleurs.ROUGE + "No gateway" + Couleurs.RESET + " ]")
        return False

    def __check_gateway_in_docker_compose(self, repository):
        gateway_pattern = re.compile(r'\bgateway\b', re.IGNORECASE)
        docker_compose_file = repository.get_contents("docker-compose.yml")
        docker_compose_content = docker_compose_file.decoded_content.decode('utf-8')
        if bool(gateway_pattern.search(docker_compose_content)):
            return True
        return False

    def __check_gateway_in_pom_files(self, repository):
        # Assuming the gateway keyword is case-insensitive
        gateway_pattern = re.compile(r'\bgateway\b', re.IGNORECASE)

        # Get the list of files in the repository
        contents = repository.get_contents("")

        for content in contents:
            # Check if the file is a pom.xml file
            if content.name.lower() == 'pom.xml':
                # Read the content of the pom.xml file
                pom_content = content.decoded_content.decode('utf-8')

                # Check if the gateway keyword is present in the pom.xml content
                if gateway_pattern.search(pom_content):
                    print(f"Gateway keyword found in {content.path}")
                    return True
                else:
                    print(f"Gateway keyword not found in {content.path}")
        return False