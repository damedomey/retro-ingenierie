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

        is_naive_works, resutlat = self.__naive_analyse(repository)
        if is_naive_works:
            print("\nNaive analyse OK 🎉\n")
            g.close()
            return resutlat

        is_code_works, resutlat = self.__code_analse(repository)
        if is_code_works:
            print("\nCode analyse OK 🎉\n")
            g.close()
            return resutlat

        print("\nDB analyse KO .... 🔥\n")
        g.close()
        return {}

    def __naive_analyse(self, repository):
        analyser = DB_Analyser_Naive()
        return analyser.run(repository)

    def __code_analse(self, repository):
        analyser = DB_Analyser_Code(self.access_token)
        return analyser.run(repository)
