import yaml

class DB_Analyser():
    def __init__(self):
        print("BD ANALYSER", flush=True)

    def __load_docker_compose(self, file_content):
        compose_data = yaml.safe_load(file_content)
        return compose_data

    def __is_database_service(self, service_name, image_name):
        keywords_for_db = ['mongo', 'mysql', 'postgres']

        for keyword in keywords_for_db:
            if keyword in image_name.lower():
                return True

        return False

    def __count_db_usage(self, compose_data):
        db_usage_count = {}

        for service_name, service_config in compose_data.get('services', {}).items():
            depends_on = service_config.get('depends_on', {})

            if isinstance(depends_on, list):
                for dependency_name in depends_on:
                    db_name = dependency_name.lower()
                    db_usage_count[db_name] = db_usage_count.get(db_name, 0) + 1
            elif isinstance(depends_on, dict):
                for dependency_name, dependency_condition in depends_on.items():
                    if isinstance(dependency_condition,
                                  dict) and 'condition' in dependency_condition and 'service_started' in \
                            dependency_condition['condition']:
                        db_name = dependency_name.lower()
                        db_usage_count[db_name] = db_usage_count.get(db_name, 0) + 1

        return db_usage_count

    def __check_single_usage(self, db_usage_count):
        for db_name, usage_count in db_usage_count.items():
            if usage_count > 1:
                print( f"WARNING: Database '{db_name}' is used by {usage_count} services. It should be used by at most one service.")

    def check_docker_compose(self, repository):
        docker_compose_file = "docker-compose.yml"
        content = repository.get_contents(docker_compose_file)

        if content:
            compose_data = self.__load_docker_compose(content.decoded_content)
            if compose_data:
                db_usage_count = self.__count_db_usage(compose_data)
                self.__check_single_usage(db_usage_count)