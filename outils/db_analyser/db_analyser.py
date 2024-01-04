from github import Github, Repository

from outils.db_analyser.src.db_analyser_naive import DB_Analyser_Naive
from outils.db_analyser.src.db_analyser_code import DB_Analyser_Code

class DB_analyser():
    def __init__(self, access_token):
        print("DB analyser")
        self.__access_token = access_token

    def run(self, repo_name):
        print("DOCKER COMPOSE ANALYSIS", flush=True)
        g = Github(self.__access_token)
        repository: Repository = g.get_repo(repo_name)

        if self.__naive_analyse(repository):
            print("\nNaive analyse OK 🎉\n")
        elif self.__code_analse(repository):
            print("\nCode analyse OK 🎉\n")
        else:
            print("\nDB analyse KO .... 🔥\n")

        g.close()

    def __naive_analyse(self, repository):
        analyser = DB_Analyser_Naive()
        return analyser.run(repository)

    def __code_analse(self, repository):
        analyser = DB_Analyser_Code(self.access_token)
        return analyser.run(repository)
