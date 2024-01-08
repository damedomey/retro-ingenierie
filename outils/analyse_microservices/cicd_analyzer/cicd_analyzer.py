from github import Github, Repository

class cicd_analyzer():
    def __init__(self, token):
        print("CI/CD analyzer ", flush=True)
        self.__token_github = token

    def run(self, repo_name):
        g = Github(self.__access_token)
        repository: Repository = g.get_repo(repo_name)
        return self.__check_services_in_CI(repository)


    def __has_Jenkinsfile(self, repository):
        contents = repository.get_contents("")
        for content in contents:
            if content.name.lower() == 'Jenkinsfile' or 'travis' in content.name.lower() or 'circle' in content.name.lower() or 'pipeline' in content.name.lower() or 'ci' in content.name.lower() or 'cd' in content.name.lower() :
                return content.name
        return None

    def __check_services_in_CI(self, repository,directories):
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

        return (services,cpt)