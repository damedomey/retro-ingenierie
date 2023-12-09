
from github import Github
from services.lib import analyzer


def analyse_csv_repos():
    output_csv_path = r"./output.csv"

    csv_path = r"./repos.csv"
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

        for line in csv_file:
            # Your existing repo processing ...

            if analyse.has_load_balancing(repository):
                with open(output_csv_path, 'a') as f:
                    f.write(repo_name + "    :    Load Balancing Configured\n")
                    f.close()
            else:
                print("REPO WITHOUT LOAD BALANCING ...", flush=True)


        g.close()

if __name__ == '__main__':
    analyse_csv_repos()
