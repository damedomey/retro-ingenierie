from github import Github
from services.InfoDockerCompose import InfoDockerCompose

if __name__ == '__main__':
    print("DOCKER COMPOSE ANALYSIS", flush=True)
    analyserDockerCompose = InfoDockerCompose()

    repo_name = "cer/microservices-examples"

    access_token = ''
    g = Github(access_token)
    repository = g.get_repo(repo_name)

    if analyserDockerCompose.has_docker_compose(repository):
        print("DOCKER COMPOSE FOUND :) !", flush=True)
    else:
        print("REPO WITHOUT DOCKER COMPOSE ...", flush=True)

    g.close()