from github import Github
import pandas as pd
from outils.utils.docker_compose_analyser import Docker_compose_analyser
from outils.utils.individualdeployment import individual_deployment
from outils.utils.mongo_analyse import mongo_analyzer
from outils.utils.master_slave import masterslave_analyzer
from outils.utils.events_analyze import event_analyser
from outils.utils.load_balacing import loadbalancer_analyzer
from outils.utils.CI_CD_analyze import cicd_analyzer
from outils.utils.gateway import gateway_analyzer
from outils.utils.db_analyser.db_analyser import DB_analyser

def analyze_repository(repository, results_df, token):
    # check docker compose 

    analyse = Docker_compose_analyser()
    dockercompose = analyse.check_docker_compose(repository=repository)
    docker_compose_status = "Present" if dockercompose is not None else "Not"
    print("here")


    if dockercompose:

        ## get all directories
        directories = analyse.get_all_directories(repository=repository, path="")

        # check custom images

        individualdeployment = individual_deployment()
        check_individual_deployment = individualdeployment.check_if_there_is_custom_images(repository=repository, dockercompose=dockercompose)
        custom_images = "Present" if check_individual_deployment else "Not"

        ## check mongo replication

        mongoanalyzer =  mongo_analyzer()
        mongo_replication = mongoanalyzer.detect_mongo_replication(dockercompose=dockercompose)
        mongo_replication_status = "Present" if mongo_replication is True else  "Not"

        ## check master slave replication

        masterslave = masterslave_analyzer()
        detect_master_slave_replication = masterslave.detect_master_slave_replication(repository=repository, dockercompose=dockercompose)
        master_slave_replication_status = "Present" if detect_master_slave_replication is True else "Not"

        ## check events

        event_analyse = event_analyser()
        images = analyse.get_services_from_docker_compose(repository=repository, dockercompose=dockercompose)
        events_status = event_analyse.check_event_sourcing(images)

        ## load balancing and scaling

        lb = loadbalancer_analyzer()
        load_balancing_status = lb.detect_load_balancer(repository=repository, images=images)

        ## CI/CD

        cicd = cicd_analyzer()
        check_services_in_CI = cicd.check_services_in_CI(repository=repository, directories=directories)
        microservices_in_CI_status = "All services" if check_services_in_CI=="all" else "Some services" if check_services_in_CI=="some" else "Not"
        
        ## check gateway

        gatewayanalyse = gateway_analyzer()
        gateway_check = gatewayanalyse.detect_gateway(dockercompose=dockercompose,directories=directories)
        gateway_status = "Present" if gateway_check is True else "Not"
        ## tous les autres outils 

        ## check db
        db_analyser = DB_analyser(token)
        db_analyser_result = db_analyser.run(repository=repository)
        db_analyser_status = "Not"
        if db_analyser_result == 1:
            db_analyser_status = "Present"
        elif db_analyser_result == -1:
            db_analyser_status = "Unknow"






    results_df = results_df._append({
        'Repo Name': repository.full_name,
        'Docker Compose Present': docker_compose_status,
        'Custom Images in Docker Compose': custom_images,
        'MongoDB Replication': mongo_replication_status,
        'Master Slave Replication': master_slave_replication_status,
        'Events': events_status,
        'Microservices in CI/CD': microservices_in_CI_status   ,
        'Load Balancing': load_balancing_status, 
        'DBs unique': db_analyser_status,
        'Gateway': gateway_status,

    }, ignore_index=True)

    return results_df





def main():
    access_token = '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'
    g = Github(access_token)

    # Create an empty DataFrame to store results
    columns = [
        'Repo Name', 'Docker Compose Present', 'Custom Images in Docker Compose',
        'MongoDB Replication', 'Master Slave Replication', 'Events',
        'Microservices in CI/CD', 'Load Balancing', 'DBs unique','Gateway'
    ]
    results_df = pd.DataFrame(columns=columns)
    output_file = "./output/output.xlsx"

    with open("./extracted_data.csv", "r") as csv_file:
        for line in csv_file:
            repo_name = line.strip()
            repository = g.get_repo(repo_name)
            print(repository)
            try:
                results_df = analyze_repository(repository, results_df, access_token)
                print(results_df)
            except Exception as e:
                continue

            save_to_excel(results_df, output_file)

def save_to_excel(results_df, output_file):
    # Save the results to an Excel file
    results_df.to_excel(output_file, index=False)

    # Adjust column widths
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        results_df.to_excel(writer, index=False, sheet_name='Results')
        worksheet = writer.sheets['Results']
        for column in worksheet.columns:
            max_length = max(len(str(cell.value)) for cell in column)
            adjusted_width = (max_length + 2) * 1.2
            worksheet.column_dimensions[column[0].column_letter].width = adjusted_width

if __name__ == "__main__":
    main()