from github import Github
from services.lib import analyzer
import json


def analyse_csv_repos():
    ## output csv 
    output_csv_path = "C:/Users/21264/Videos/retro-ingenierie/cicd_analyze/output.json"


    csv_path = "C:/Users/21264/Videos/retro-ingenierie/cicd_analyze/service-oriented.csv"
    csv_file = open(csv_path, "r")
    for line in csv_file:
        print(line.split('/'))
        #owner = line.strip().split('/')[3]
        #name = line.strip().split('/')[4]

        repo_name = line.strip()


        print("Analyzing repo: " + repo_name, flush=True)
        access_token = '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'
        g = Github(access_token)
        try:

            repository = g.get_repo(repo_name)
        except:
            print("Repo not found", flush=True)
            continue

        analyse = analyzer()
        
        path_to_docker_compose = analyse.has_docker_compose(repository)

        if path_to_docker_compose!=None:
            images = analyse.get_images_from_docker_compose(repository=repository)

            if images!=None:
                ## open json file
                json_file = open(output_csv_path, "a")
                ## write in json file
                json_file.write(json.dumps(images))
                ## close json file
                json_file.close()
                

        else:
            print("REPO WITHOUT docker compose ...", flush=True)

        g.close()

def list_to_string(liste):
    string = " , "
    for i in liste:
        string += i
    return string

if __name__ == '__main__':
    analyse_csv_repos()
