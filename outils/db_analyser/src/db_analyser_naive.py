import yaml

from utils.Colors import Couleurs
from src.csv_manager import CSV_Manager

class DB_Analyser_Naive():
    def __init__(self):
        print("BD ANALYSER", flush=True)
        self.csv_manager = CSV_Manager()

    def run(self, repository):
        docker_compose_file = "docker-compose.yml"
        content = repository.get_contents(docker_compose_file)

        if content:
            compose_data = self.__load_docker_compose(content.decoded_content)
            if compose_data:
                db_usage_count = self.__count_db_usage_naive(compose_data)
                self.__check_single_usage(db_usage_count)
                if len(db_usage_count) > 0:
                    print("\n[ " + Couleurs.VERT + "OK" + Couleurs.RESET + " ] Depends_on trouvé 🎉\n")
                    return True
                else:
                    print("\n[ "+Couleurs.ROUGE + "KO" + Couleurs.RESET+" ] Pas de depends_on trouvé 🔥 ...\n")
                    return False
            else:
                return False

        return False

    def __load_docker_compose(self, file_content):
        compose_data = yaml.safe_load(file_content)
        return compose_data

    def __is_database_service(self, service_name, image_name):
        keywords_for_db = ['mongo', 'mysql', 'postgres', 'cassandra']

        for keyword in keywords_for_db:
            if keyword in image_name.lower():
                print("DB detected ... 🚀 : " + image_name)
                return True

        return False

    def __count_db_usage_naive(self, compose_data):
        db_names_in_services = set()
        db_usage_count = {}

        for service_name, service_config in compose_data.get('services', {}).items():
            image_name = service_config.get('image', '')
            if self.__is_database_service(service_name, image_name):
                db_names_in_services.add(service_name.lower())


        for service_name, service_config in compose_data.get('services', {}).items():
            depends_on = service_config.get('depends_on', [])
            for dependency_name in depends_on:
                db_name = dependency_name.lower()
                #print("NAME : ", db_name)
                if db_name in db_names_in_services:
                    db_usage_count[db_name] = db_usage_count.get(db_name, 0) + 1

        print(db_usage_count)

        return db_usage_count

    def __check_single_usage(self, db_usage_count):
        self.csv_manager.right(db_usage_count)
        for db_name, usage_count in db_usage_count.items():
            if usage_count > 1:
                print( f"WARNING: Database '{db_name}' is used by {usage_count} services. It should be used by at most one service. KO")
            else:
                print(f"Database '{db_name}' is used by {usage_count} services. OK")