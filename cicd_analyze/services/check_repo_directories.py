from github import Github
from lib import analyzer
access_token = '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'
g = Github(access_token)

with open("C:/Users/21264/Videos/retro-ingenierie/good_dataset.csv", "r") as csv_file:
    for line in csv_file:
        repo_name = line.strip()

        print("Analyzing repo: " + repo_name, flush=True)


        try:

            repository = g.get_repo(repo_name)
        except:
            print("Repo not found", flush=True)

        analyse = analyzer()

        print(repository)

        dockercompose = analyse.has_docker_compose(repository=repository)

        if(dockercompose==None):
            print("No docker-compose.yml file found", flush=True)

        else : 
            print("docker-compose.yml file found", flush=True)
            directories = analyse.get_all_directories(repository=repository, path="")
            images = analyse.get_services_from_docker_compose(repository=repository,dockercompose=dockercompose)
            check = analyse.check_if_there_is_custom_images(repository=repository,images_from_dockercompose=images,directories=directories)
            if(check==None):
                print("No custom images found in docker compose", flush=True)
            else:
                print("custom images found in docker compose", flush=True)
                print(check)

                ## Check mongo db replication
                ongo_replication = analyse.detect_mongo_replication(dockercompose=dockercompose)
                if(ongo_replication==None):
                    print("No mongo replication", flush=True)

                else:
                    print("mongo replication", flush=True)
                    print(ongo_replication)

                ## Check Master SLave
                detect_master_slave_replication = analyse.detect_master_slave_replication(repository=repository,dockercompose=dockercompose)

                if(detect_master_slave_replication==None):
                    print("No master slave replication", flush=True)
                else:
                    print("master slave replication", flush=True)
                    print(detect_master_slave_replication)

                ## CI/CD

                directories = check[0]
                check_services_in_CI = analyse.check_services_in_CI(repository=repository,directories=directories)

                if(check_services_in_CI==None):
                    print("No microservices in CI/CD", flush=True)
                else:
                    print("microservices in CI/CD", flush=True)
                    print(check_services_in_CI)






