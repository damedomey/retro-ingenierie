from dockerfile_parse import DockerfileParser
import yaml

class cicd_analyzer():

    def __init__(self):
        print("Info ", flush=True)

    def has_Jenkinsfile(self, repository):
        contents = repository.get_contents("")
        for content in contents:
            if content.name.lower() == 'Jenkinsfile' or 'travis' in content.name.lower() or 'circle' in content.name.lower() or 'pipeline' in content.name.lower() or 'ci' in content.name.lower() or 'cd' in content.name.lower() :
                return content.name
        return None

    def check_services_in_CI(self, repository,directories):
        services = []
        cpt=0
        # Obtenez le contenu du fichier 'docker-compose.yml'
        file_content = self.has_Jenkinsfile(repository)
        ##print("file_content : " + str(file_content), flush=True)
        if file_content is None:
            return None
        
        ## parse file_content to a string
        
        for directory in directories:
            if directory.lower() in file_content.lower():
                services.append(directory)
                cpt+=1

        if cpt==0:
            return None
        
        elif cpt==len(directories):
            return "all"
        
        else:
            return "some"

