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
    
    def has_load_balancing(self, repository):
        # Check if the repository has a Docker Compose file
        try:
            compose_file = repository.get_contents("docker-compose.yml")
        except:
            return False

        # Parse the Docker Compose file
        compose_data = yaml.safe_load(compose_file.decoded_content)

        # Check for load balancing configurations
        for service_name, service_config in compose_data['services'].items():
            if 'deploy' in service_config and 'replicas' in service_config['deploy']:
                if service_config['deploy']['replicas'] > 1:
                    return True

        return False