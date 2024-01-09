import requests
import yaml
#from outils.db_analyser.src.csv_manager import CSV_Manager
from utils.Colors import Couleurs

class DB_Analyser_Code():
    def __init__(self, access_token):
        print("DB_Analyser_Code")
        self.__access_token = access_token
        #self.__csv_manager = CSV_Manager()

    def run(self, repository, docker_compose_content):
        db_names_in_services = set()

        if docker_compose_content:
            compose_data = self.__load_docker_compose(docker_compose_content)

            for service_name, service_config in compose_data.get('services', {}).items():
                image_name = service_config.get('image', '')
                if self.__is_database_service(service_name, image_name):
                    db_names_in_services.add(service_name.lower())

            db_count_list = self.__find_db(repository, db_names_in_services, docker_compose_content)

            #self.__csv_manager.right(db_count_list)
            print(db_count_list)
            if len(db_count_list) > 0:
                return True, db_count_list
            else:
                print("Pas de depends_on pour les DBs ....")
                return False, {}
        else:
            return False, {}

    def __find_db(self, repository, db_name_list, docker_compose_content):
        db_count_list = {}
        db_files = self.__found_db_file(repository, db_name_list, docker_compose_content)

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
            if 'docker' in fichier:
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
        repo_url = "https://api.github.com/repos/" + str(repository.full_name)
        print("repo_url : ", repo_url)

        branches_url = f"{repo_url}/git/refs/heads"
        default_branch = self.__get_default_branch(branches_url)

        if default_branch:
            print(f"Default branch: {default_branch}")
            tree = self.__get_directory_tree(repo_url, default_branch)
            print("Directory tree:")
            for item in tree:
                print(item)
        #url = f'https://api.github.com/repos/{repository.owner.login}/{repository.name}/git/trees/main?recursive=1'

        response = requests.get(url, headers={"Authorization": f"Bearer {self.__access_token}"})
        response.raise_for_status()

        files = [item['path'] for item in response.json().get('tree', []) if item.get('type') == 'blob']
        return files

    def __found_db_file(self, repository, keywords, docker_compose_content):
        files = self.__get_repo_files(repository)

        db_used = []

        for keyword in keywords:
            analyse = self.__search_keyword_in_files(docker_compose_content, keyword, files)

            if len(analyse) <= 0:
                print("\n" + Couleurs.JAUNE + "WARNING : no file found ..." + Couleurs.RESET + "\n")
                analyse = self.__var_env_docker_compose_research(keyword, repository)

            db_used.append([keyword, analyse])

        return db_used

    def __search_keyword_in_files(self, docker_compose_content, keyword, files):

        found_files = []

        for file in files:
            print("[ "+Couleurs.JAUNE+"FILE"+Couleurs.RESET+" ] research BD [ "+Couleurs.VERT+""+keyword+""+Couleurs.RESET+" ]  in : ", file)
            try:
                # Utilisez le mode binaire pour éviter la tentative de décodage en UTF-8
                content = docker_compose_content
                # Convertissez keyword en bytes en l'encodant en UTF-8
                keyword_bytes = keyword.encode('utf-8')
                if keyword_bytes in content and "docker-compose" not in file:
                    print("🎉 ............ "+Couleurs.VERT+"FOUND"+Couleurs.RESET+" in "+file+"")
                    found_files.append(file)
            except Exception as e:
                print("[ "+Couleurs.ROUGE+"ERROR"+Couleurs.RESET+" ] : "+Couleurs.ROUGE+"Lors du traitement du fichier "+file+": "+str(e)+""+Couleurs.RESET+"")

        return found_files

    def __var_env_docker_compose_research(self, db_name, repository):
        print("[ "+Couleurs.JAUNE+"COMPOSE"+Couleurs.RESET+" ]" + db_name + " in docker compose var env ? ")

        docker_compose_file = "docker-compose.yml"
        content = repository.get_contents(docker_compose_file)
        compose_data = yaml.safe_load(content.decoded_content)

        #print(compose_data)
        occurrences = self.__count_db_name_occurrences(compose_data, db_name)

        print(f"Nombre d'apparitions de {db_name} : {len(occurrences)}")

        return occurrences

    def __count_db_name_occurrences(self, compose_data, db_name):

        services = compose_data.get("services", {})
        tmp = False
        cpt = []

        for service_name, service in services.items():
            #print(f"Variables d'environnement pour le service '{service_name}':")

            if service_name.lower() != db_name.lower():
                environment_vars = service.get("environment", [])
                for env_var in environment_vars:
                    #print(f"  - {env_var}")
                    if db_name.lower() in env_var.lower():
                        #print("TEST ok")
                        print("[ "+Couleurs.JAUNE+""+db_name+""+Couleurs.RESET+" ] in " + service_name + " : " + env_var)
                        tmp = True
                if tmp:
                    tmp= False
                    cpt.append("VAR_ENV_IN_" + service_name)

        return cpt

    def __get_default_branch(self, api_url):
        try:
            response = requests.get(api_url)
            response.raise_for_status()  # Raise an error for bad responses
            branches = response.json()
            if branches:
                print("Branch name : ", branches[0]['name'], flush=True)
                return branches[0]['name']
            print("NONE", flush=True)
            return None
        except Exception as e:
            print("Error during request: ", e)
            return None


    def __get_directory_tree(self, api_url, branch):
        tree_url = f"{api_url}/git/trees/{branch}?recursive=1"
        response = requests.get(tree_url)
        response.raise_for_status()
        return response.json().get('tree', [])





