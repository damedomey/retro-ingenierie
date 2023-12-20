from github import Github
from lib import analyzer
access_token = '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'
g = Github(access_token)

with open("C:/Users/21264/Videos/retro-ingenierie/extracted_data.csv", "r") as csv_file:
    for line in csv_file:
        repo_name = line.strip()

        print("Analyzing repo: " + repo_name, flush=True)


        try:

            repository = g.get_repo(repo_name)
        except:
            print("Repo not found", flush=True)

        analyse = analyzer()

        print(repository)

        ##images = analyse.get_services_from_docker_compose(repository=repository)
        ##directory = analyse.get_all_directories(repository=repository, path="")
        check = analyse.check_if_there_is_custom_images(repository=repository)
        print("custom images")
        print(check)

        if(check==None):
            print("No docker-compose.yml file found", flush=True)
## get first element of tuple
        directories = check[0]
        #dockerfile_count = check[2]
        #print("found" + str(dockerfile_count) + "dockerfiles")
        check_services_in_CI = analyse.check_services_in_CI(repository=repository,directories=directories)
        print("services in CI")
        print(check_services_in_CI)
