from dockerfile_parse import DockerfileParser
import yaml

class individual_deployment():
    def __init__(self):
        print("Info ", flush=True)

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
        

    
