from github import Github, Repository
from src.db_analyser import DB_Analyser

if __name__ == '__main__':
    print("DOCKER COMPOSE ANALYSIS", flush=True)
    analyserDockerCompose = DB_Analyser()

    repo_name = "cer/microservices-examples"
    #repo_name= "pns-si5-al-course/soa-marsy-marsy-23-24-team-c"

    access_token = ''
    g = Github(access_token)
    repository:Repository = g.get_repo(repo_name)
    analyserDockerCompose.check_docker_compose(repository)

    g.close()