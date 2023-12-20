from github import Github
from services.lib import analyzer
import json


def analyse_csv_repos():
    output_json_path = "C:/Users/21264/Videos/retro-ingenierie/cicd_analyze/output.json"
    analyzed_repos = set()  # Maintaining a set to store analyzed repos

    # Load previously analyzed repos from output.json if available
    try:
        with open(output_json_path, 'r') as json_file:
            analyzed_data = json.load(json_file)
            for entry in analyzed_data:
                analyzed_repos.add(entry)  # Assuming the repo name is stored in the first element
    except FileNotFoundError:
        pass  # Ignore if the file doesn't exist yet

    csv_path = "C:/Users/21264/Videos/retro-ingenierie/cicd_analyze/service-oriented.csv"
    with open(csv_path, "r") as csv_file:
        for line in csv_file:
            repo_name = line.strip()

            print("Analyzing repo: " + repo_name, flush=True)

            access_token = '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'
            g = Github(access_token)

            try:
                repository = g.get_repo(repo_name)
            except:
                print("Repo not found", flush=True)
                continue

            if repo_name in analyzed_repos:
                print("Repo already analyzed", flush=True)
                g.close()
                continue

            analyse = analyzer()

            custom = analyse.check_if_there_is_custom_images(repository=repository)

            # Open JSON file to append analyzed repo information
            with open(output_json_path, "a") as json_file:
                # Create a tuple with repo_name and a boolean indicating analysis
                text = (repo_name, bool(custom))
                json_file.write(json.dumps(text))
                json_file.write('\n')  # Add newline for the next entry

            # Add the repo to the set of analyzed repos to prevent reanalysis
            analyzed_repos.add(repo_name)
            g.close()

if __name__ == '__main__':
    analyse_csv_repos()
