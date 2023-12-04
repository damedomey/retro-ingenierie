from github import Github, Repository
import re
import os

class InfoDockerCompose():
    def __init__(self):
        print("Info Docker Compose", flush=True)
        self.docker_compose = None

    def has_docker_compose(self, repository:Repository):
        # Obtenez la liste des fichiers dans le dépôt
        contents = repository.get_contents("")

        # Vérifiez si 'docker-compose.yml' est parmi les fichiers du dépôt
        for content in contents:
            #print("Folder name : " + content.name)
            #print(content)
            if content.name.lower() == 'docker-compose.yml':
                return True

        return False

    def has_gateway(self, repository: Repository):
        # Dans le compose
        gateway_in_docker_compose = self.__check_gateway_in_docker_compose(repository)

        # Dans les pom.xml
        gateway_in_pom_files = self.__check_gateway_in_pom_files(repository)

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
                else:
                    print(f"Gateway keyword not found in {content.path}")

