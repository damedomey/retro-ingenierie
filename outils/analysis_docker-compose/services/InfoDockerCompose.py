from github import Github
from github import Auth

class InfoDockerCompose():
    def __init__(self):
        print("Info Docker Compose", flush=True)

    def has_docker_compose(self, owner, repo):
        # Remplacez 'YOUR_ACCESS_TOKEN' par votre propre jeton d'accès GitHub
        access_token = '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'

        # Créez une instance de l'objet Github avec votre jeton d'accès
        g = Github(access_token)

        # Obtenez l'objet Repository pour le dépôt spécifié
        repository = g.get_repo(f"{owner}/{repo}")

        # Obtenez la liste des fichiers dans le dépôt
        contents = repository.get_contents("")

        # Vérifiez si 'docker-compose.yml' est parmi les fichiers du dépôt
        for content in contents:
            print("Folder name : " + content.name)
            if content.name.lower() == 'docker-compose.yml':
                return True

        g.close()
        return False