class InfoDockerCompose():
    def __init__(self):
        print("Info Docker Compose", flush=True)

    def has_docker_compose(self, repository):
        # Obtenez la liste des fichiers dans le dépôt
        contents = repository.get_contents("")

        # Vérifiez si 'docker-compose.yml' est parmi les fichiers du dépôt
        for content in contents:
            print("Folder name : " + content.name)
            if content.name.lower() == 'docker-compose.yml':
                return True

        return False