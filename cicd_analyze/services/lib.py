from dockerfile_parse import DockerfileParser
import yaml

class analyzer():
    def __init__(self):
        print("Info ", flush=True)

    def get_all_directories(self, repository, path=""):
        directories = []

        def get_directories_recursive(repo, directory_path):
            nonlocal directories
            for content in repo.get_contents(directory_path):
                if content.type == "dir":
                    directories.append(content.path)
                    get_directories_recursive(repo, content.path)

        get_directories_recursive(repository, path)
        return directories

    def calculate_directory_sizes(self, repo, directories):
        directory_sizes = {}
        for directory in directories:
            contents = repo.get_contents(directory)
            size = sum(file.size for file in contents if file.type == "file")
            directory_sizes[directory] = size

        return directory_sizes
    
    def check_if_there_is_custom_images(self, repository,images_from_dockercompose,directories):
        correspondences = []
        deployed_services = 0
        directories = directories
        repo_images = images_from_dockercompose

        if repo_images!=None and directories!=None:
            # Comparer les services du docker-compose avec les noms de dossiers
            
            for service_name in repo_images:
                for directory in directories:
                    if directory.lower() == service_name.lower() or (directory.lower() in service_name.lower()) or (service_name.lower() in directory.lower()):
                        if service_name not in correspondences:
                            deployed_services += 1
                            correspondences.append(service_name)
                        

            return (correspondences, deployed_services)
        
        else:
            print("No docker-compose.yml file found", flush=True)
        # Comparer les services du docker-compose avec les noms de dossiers
        

        

        
  

    def has_docker_compose(self, repository):
        def search_for_docker_compose(contents, current_path=""):
            dockerfile=0
            for content in contents:
                if content.type == "dir":
                    sub_contents = repository.get_contents(content.path)
                    path = current_path + "/" + content.name if current_path else content.name
                    docker_compose_path = search_for_docker_compose(sub_contents, path)
                    if docker_compose_path:
                        return docker_compose_path
                elif content.name.lower() == 'docker-compose.yml' or 'docker-compose' in content.name.lower():
                    docker_compose_content = repository.get_contents(content.path).decoded_content.decode("utf-8")
                    return docker_compose_content  # Retourne le contenu du fichier 'docker-compose.yml'
                elif content.name.lower()=='dockerfile':
                    dockerfile+=1
                    
            return None

    # Obtient la liste des fichiers dans le dépôt
        contents = repository.get_contents("")

        # Recherche récursive du fichier 'docker-compose.yml'
        return search_for_docker_compose(contents)


  
    
    def get_services_from_docker_compose(self, repository,dockercompose):
        # Obtenez le contenu du fichier 'docker-compose.yml'
        ##print("file_content : " + str(file_content), flush=True)
        if dockercompose is None:
            return None

        # Obtenez la liste des services
        return get_docker_services_from_compose(dockercompose)
        


    
    def has_Jenkinsfile(self, repository):
        # Obtenez la liste des fichiers dans le dépôt
        contents = repository.get_contents("")

        for content in contents:
            #print("Folder name : " + content.name)
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
    
    def detect_mongo_replication(self,dockercompose):

        dockercompose = yaml.safe_load(dockercompose)
        if dockercompose is None:
            return None

        replication_keywords = [' --replSet rs0']
        replication_detected = False

        for service_name, service_config in dockercompose.get('services', {}).items():
            if 'image' in service_config and service_config['image'] == 'mongo':
                if 'command' in service_config:
                    command = service_config['command']
                    for keyword in replication_keywords:
                        if keyword in command:
                            replication_detected = True
                            break

        return replication_detected


        

    def detect_master_slave_replication(self, repository,dockercompose):
        file_content = dockercompose
        if file_content is None:
            return None

        replication_keywords = ['master', 'slave', 'replica']

        for line in file_content.split('\n'):
            for keyword in replication_keywords:
                if keyword in line.lower():
                    # Vous pouvez ajuster cette logique selon vos besoins
                    return True  # Détecté une configuration de réplication maître-esclave

        return False  # Aucune configuration de réplication détectée
    
    def check_services_in_CI(self, repository,directories):
        services = []
        cpt=0
        # Obtenez le contenu du fichier 'docker-compose.yml'
        file_content = self.has_Jenkinsfile(repository)
        print("CI/CD file" + str(file_content), flush=True)
        ##print("file_content : " + str(file_content), flush=True)
        if file_content is None:
            return None
        
        ## parse file_content to a string
        print(file_content)
        
        for directory in directories:
            if directory.lower() in file_content.lower():
                services.append(directory)
                cpt+=1

        return (services,cpt)
        




def get_docker_images_from_compose(file_content):
    images_list = []

    # Charger le contenu du fichier YAML
    compose_data = yaml.safe_load(file_content)

    # Vérifier si 'services' est présent dans le fichier docker-compose.yml
    if 'services' in compose_data:
        services = compose_data['services']

        # Parcourir chaque service pour obtenir les images
        for service_name, service_config in services.items():
            if 'image' in service_config:
                images_list.append(service_config['image'])
            elif 'build' in service_config:
                dockerfile_path = service_config['build']
                if isinstance(dockerfile_path, str):  # Handle different build configurations
                    dockerfile_path = dockerfile_path.split(' ')[0]
                dockerfile = DockerfileParser(path=dockerfile_path)
                for instruction in dockerfile.structure:
                    if instruction['instruction'] == 'FROM':
                        images_list.append(instruction['value'])

    return images_list


def get_docker_services_from_compose(file_content):
    service_names = []

    # Charger le contenu du fichier YAML
    compose_data = yaml.safe_load(file_content)

    # Vérifier si 'services' est présent dans le fichier docker-compose.yml
    if 'services' in compose_data:
        services = compose_data['services']

        # Obtenir les noms des services
        service_names = list(services.keys())

    return service_names
