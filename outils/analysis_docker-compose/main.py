from github import Github, Repository
from services.InfoDockerCompose import InfoDockerCompose

if __name__ == '__main__':
    print("DOCKER COMPOSE ANALYSIS", flush=True)
    analyserDockerCompose = InfoDockerCompose()

    repo_name = "cer/microservices-examples"

    access_token = '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'
    g = Github(access_token)
    repository:Repository = g.get_repo(repo_name)

    if analyserDockerCompose.has_docker_compose(repository):
        print("DOCKER COMPOSE FOUND :) !", flush=True)
        has_gatway = analyserDockerCompose.has_gateway(repository)
        if has_gatway:
            print("Has a gateway")
        else:
            print("Has not a gateway")
    else:
        print("REPO WITHOUT DOCKER COMPOSE ...", flush=True)

    g.close()