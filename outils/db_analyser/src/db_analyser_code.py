from github import Github
import requests
import yaml
from src.csv_manager import CSV_Manager
from utils.Colors import Couleurs

class DB_Analyser_Code():
    def __init__(self, access_token):
        print("DB_Analyser_Code")
        self.access_token = access_token
        self.csv_manager = CSV_Manager()

    def run(self, repository):
        docker_compose_file = "docker-compose.yml"
        content = repository.get_contents(docker_compose_file)

        db_names_in_services = set()

        if content:
            compose_data = self.__load_docker_compose(content.decoded_content)

            for service_name, service_config in compose_data.get('services', {}).items():
                image_name = service_config.get('image', '')
                if self.__is_database_service(service_name, image_name):
                    db_names_in_services.add(service_name.lower())

            db_count_list = self.__find_db(repository, db_names_in_services)
            self.csv_manager.right(db_count_list)
            if len(db_count_list) > 0:
                return True
            else:
                return False
        else:
            return False

    def __find_db(self, repository, db_name_list):
        db_count_list = {}
        db_files = self.__found_db_file(repository, db_name_list)

        for found_files in db_files:
            if found_files:
                print(f"Mot-clé trouvé dans les fichiers suivants:")
                #print("NAME : " , found_files[0])
                for file in found_files[1]:
                    print(f" - {file}")

                count = self.__compter_repertoires_diff(found_files[1])
                db_count_list[found_files[0]] = count
            else:
                print("Aucun fichier ne contient le mot-clé.")
        print("db_count_list : " , db_count_list)
        return db_count_list

    def __compter_repertoires_diff(self, liste_fichiers):
        repertoires_diff = set()

        for fichier in liste_fichiers:
            # Ignorer docker-compose.yml
            if 'docker-compose.yml' in fichier:
                continue

            # Extraire le répertoire du chemin du fichier
            repertoire = fichier.split('/')[0]

            # Ajouter le répertoire à l'ensemble (un ensemble ne contient que des éléments uniques)
            repertoires_diff.add(repertoire)

        # Renvoyer le nombre d'éléments uniques dans l'ensemble
        return len(repertoires_diff)

    def __load_docker_compose(self, file_content):
        compose_data = yaml.safe_load(file_content)
        return compose_data

    def __is_database_service(self, service_name, image_name):
        keywords_for_db = ['mongo', 'mysql', 'postgres', 'cassandra']

        for keyword in keywords_for_db:
            if keyword in image_name.lower():
                print("DB detected ... 🚀 : " + image_name.lower())
                return True

        return False

    def __get_repo_files(self, repository):
        url = f'https://api.github.com/repos/{repository.owner.login}/{repository.name}/git/trees/main?recursive=1'

        response = requests.get(url, headers={"Authorization": f"Bearer {self.access_token}"})
        response.raise_for_status()

        files = [item['path'] for item in response.json().get('tree', []) if item.get('type') == 'blob']
        return files

    def __found_db_file(self, repository, keywords):
        files = self.__get_repo_files(repository)

        db_used = []

        for keyword in keywords:
            analyse = self.__search_keyword_in_files(repository, keyword, files)
            db_used.append([keyword, analyse])

        return db_used

    def __search_keyword_in_files(self, repository, keyword, files):
        found_files = []

        for file in files:
            print("[ "+Couleurs.JAUNE+"FILE"+Couleurs.RESET+" ] research BD [ "+Couleurs.VERT+""+keyword+""+Couleurs.RESET+" ]  in : ", file)
            try:
                # Utilisez le mode binaire pour éviter la tentative de décodage en UTF-8
                content = repository.get_contents(file).decoded_content
                # Convertissez keyword en bytes en l'encodant en UTF-8
                keyword_bytes = keyword.encode('utf-8')
                if keyword_bytes in content and "docker-compose" not in file:
                    print("🎉 ............ "+Couleurs.VERT+"FOUND"+Couleurs.RESET+" in "+file+"")
                    found_files.append(file)
            except Exception as e:
                print("[ "+Couleurs.ROUGE+"ERROR"+Couleurs.RESET+" ] : "+Couleurs.ROUGE+"Lors du traitement du fichier "+file+": "+str(e)+""+Couleurs.RESET+"")

        return found_files