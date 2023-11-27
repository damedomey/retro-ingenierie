from services.InfoDockerCompose import InfoDockerCompose

if __name__ == '__main__':
    print("DOCKER COMPOSE ANALYSIS", flush=True)
    repo = InfoDockerCompose()

    if repo.has_docker_compose(owner="cer", repo="microservices-examples"):
        print("DOCKER COMPOSE FOUND :) !", flush=True)
    else:
        print("REPO WITHOUT DOCKER COMPOSE ...", flush=True)