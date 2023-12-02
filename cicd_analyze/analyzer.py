from github import Github
from services.lib import analyzer


def analyse_csv_repos():
    ## output csv 
    output_csv_path = "C:/Users/21264/Videos/retro/output.csv"

    csv_path = "C:/Users/21264/Videos/retro/repos.csv"
    csv_file = open(csv_path, "r")
    for line in csv_file:
        print(line.split('/'))
        owner = line.strip().split('/')[3]
        name = line.strip().split('/')[4]

        repo_name = owner + '/' + name

        print("Analyzing repo: " + repo_name, flush=True)
        access_token = ''
        g = Github(access_token)
        try:

            repository = g.get_repo(repo_name)
        except:
            print("Repo not found", flush=True)
            continue

        analyse = analyzer()

        if analyse.has_Jenkinsfile(repository)!=None:

            with open(output_csv_path, 'a') as f:
                
                f.write(repo_name + "    :    " + analyse.has_Jenkinsfile(repository) + "\n")
                f.close()
            
        else:
            print("REPO WITHOUT CI/CD ...", flush=True)

        g.close()

if __name__ == '__main__':
    analyse_csv_repos()
