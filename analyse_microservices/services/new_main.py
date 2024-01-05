import pandas as pd
from github import Github
from utils.lib import analyzer
from utils.mongo_analyse import mongo_analyzer
from utils.gateway import gateway_analyzer
from utils.cicd_analyzer import cicd_analyzer
from utils.event_sourcing import check_event_sourcing
from utils.load_balacing import detect_load_balancer
from utils.master_slave import masterslave_analyzer
from utils.individualdeployment import individualdeployment



def analyze_repository(repository, results_df):
    print("Analyzing repo: " + repository.full_name, flush=True)

    analyse = analyzer()
    dockercompose = analyse.has_docker_compose(repository=repository)
    docker_compose_status = "Present" if dockercompose is not None else "Not"

    if dockercompose is not None:
        directories = analyse.get_all_directories(repository=repository, path="")
        images = analyse.get_services_from_docker_compose(repository=repository, dockercompose=dockercompose)

        individual_deployment = individualdeployment()

        check = individual_deployment.check_if_there_is_custom_images(repository=repository, images_from_dockercompose=images, directories=directories)
        custom_images = "Present" if check else "Not"

        mongoanalyzer =  mongo_analyzer()

        mongo_replication = mongoanalyzer.detect_mongo_replication(dockercompose=dockercompose)
        mongo_replication_status = "Present" if mongo_replication is True else  "Not"


        masterslave = masterslave_analyzer()
        detect_master_slave_replication = masterslave.detect_master_slave_replication(repository=repository, dockercompose=dockercompose)
        master_slave_replication_status = "Present" if detect_master_slave_replication is True else "Not"


        possible_event_sourcing = check_event_sourcing(images)
        event_sourcing_status = "Present" if possible_event_sourcing else "Not"

        directories = check[0]

        cicd = cicd_analyzer()
        check_services_in_CI = cicd.check_services_in_CI(repository=repository, directories=directories)
        microservices_in_CI_status = "Present" if check_services_in_CI is not None else "Not"

        #lb = loadbalancer_analyzer()
        load_balancing_check = detect_load_balancer(repository=repository, images=images)
        load_balancing_status = process_load_balancer_result(load_balancing_check)



        gatewayanalyse = gateway_analyzer()
        gateway = gatewayanalyse.detect_gateway(dockercompose=dockercompose,directories=directories)
        gateway_status = "Present" if gateway is True else "Not"
    else:
        mongo_replication_status = "Not"
        master_slave_replication_status = "Not"
        event_sourcing_status = "Not"
        custom_images = "Not"

        directories = analyse.get_all_directories(repository=repository, path="")
        check_services_in_CI = analyse.check_services_in_CI(repository=repository, directories=directories)
        microservices_in_CI_status = "Present" if check_services_in_CI is not None else "Not"


        load_balancing = detect_load_balancer(repository=repository, images=None)
        load_balancing_status = process_load_balancer_result(load_balancing)

    # Append the results to the DataFrame
    results_df = results_df._append({
        'Repo Name': repository.full_name,
        'Docker Compose Present': docker_compose_status,
        'Custom Images in Docker Compose': custom_images,
        'MongoDB Replication': mongo_replication_status,
        'Master Slave Replication': master_slave_replication_status,
        'Possible Event Sourcing': event_sourcing_status,
        'Microservices in CI/CD': microservices_in_CI_status,
        'Load Balancing': load_balancing_status,
        'Gateway': gateway_status
    }, ignore_index=True)


    return results_df

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


def process_load_balancer_result(result):
    load_balancing_status, message = result
    if load_balancing_status:
        if message == "scalability present":
            return "LoadBalancing and Scalability"
        else:
            return"LoadBalancing and no Scalability"
    else:
        return "Not present"



def main():
    access_token = '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'
    g = Github(access_token)

    # Create an empty DataFrame to store results
    columns = [
        'Repo Name', 'Docker Compose Present', 'Custom Images in Docker Compose',
        'MongoDB Replication', 'Master Slave Replication', 'Possible Event Sourcing',
        'Microservices in CI/CD', 'Load Balancing'
    ]
    results_df = pd.DataFrame(columns=columns)
    output_file = "C:/Users/21264/Videos/retro-ingenierie/output/output.xlsx"

    with open("C:/Users/21264/Videos/retro-ingenierie/extracted_data.csv", "r") as csv_file:
        for line in csv_file:
            repo_name = line.strip()
            repository = g.get_repo(repo_name)
            print(repository)
            try:
                results_df = analyze_repository(repository, results_df)
                print(results_df)
            except Exception as e:
                continue


            save_to_excel(results_df, output_file)

if __name__ == "__main__":
    main()
