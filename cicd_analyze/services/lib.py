class analyzer():
    def __init__(self):
        print("Info CI/CD", flush=True)

    def has_docker_compose(self, repository):
        # Obtenez la liste des fichiers dans le dépôt
        contents = repository.get_contents("")

        # Vérifiez si 'docker-compose.yml' est parmi les fichiers du dépôt
        for content in contents:
            print("Folder name : " + content.name)
            if content.name.lower() == 'docker-compose.yml':
                return True

        return False
    
    def has_Jenkinsfile(self, repository):
        # Obtenez la liste des fichiers dans le dépôt
        contents = repository.get_contents("")

        for content in contents:
            print("Folder name : " + content.name)
            if content.name.lower() == 'Jenkinsfile' or 'travis' in content.name.lower() or 'circle' in content.name.lower() or 'pipeline' in content.name.lower() or 'ci' in content.name.lower() or 'cd' in content.name.lower() :
                return content.name

        return None