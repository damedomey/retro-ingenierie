from github import Github
import csv

# Replace 'YOUR_ACCESS_TOKEN' with your actual GitHub access token
ACCESS_TOKEN = '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'
g = Github(ACCESS_TOKEN)

# Keywords related to microservices architecture
architecturePatterns = ["microservices","microservice"]
# toolsAndFramework = ["docker", "kubernetes", "istio", "helm", "ci/cd", "jenkins", "travis", "circleci", "argo"]
# developmentAndLanguageSpecific = ["spring", "nestjs", "django", "fastapi", "java", "go", "ruby", "python", "quarkus", "vertx", "react", "angular", "vuejs"]
# messagingAndCommunication = ["kafka", "rabbitmq", "pub/sub", "grpc", "rest", "restful"]
topics = [architecturePatterns]


def should_exclude_repo(repo):
    keywords_to_exclude = ["framework", "tool", "library", "platform", "plateforme", 
                           "sdk", "api", "solution", "example", "sample", "test", 
                           "demo", "template", "boilerplate", "plugin", "starter", 
                           "prototype", "playground", "experiment", "scratch", 
                           "deprecated", "old", "legacy", "obsolete", "deprecated"]
    description = repo.description.lower() if repo.description else ""
    name = repo.name.lower() if repo.name else ""
    
    for keyword in keywords_to_exclude:
        if keyword in description or keyword in name:
            return True
    
    return False


for topic in topics:
    print("------------------------------------------")
    print("Now fetching repositories for the following keywords: " + str(topic))
    print("------------------------------------------")

    for keyword in topic:
        print("Looking for : " + keyword)
        csv_file = keyword + ".csv"
        repo_names = []
        query = f'"{keyword}" in:readme,description,repo'
        repos = g.search_repositories(query)

        for repo in repos:
            if not should_exclude_repo(repo):
                repo_names.append(repo.full_name)

        csv_file = csv_file.replace("/", "-")

        with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Repository Name'])  # Header
            for name in repo_names:
                writer.writerow([name])
