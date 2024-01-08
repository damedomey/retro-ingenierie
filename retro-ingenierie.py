from github import Github
import pandas as pd
from outils.utils.docker_compose_analyser import Docker_compose_analyser

def analyze_repository(repository, results_df):
    # check docker compose 

    analyse = Docker_compose_analyser()
    dockercompose = analyse.has_docker_compose(repository=repository)
    docker_compose_status = "Present" if dockercompose is not None else "Not"

    if dockercompose:
        
        ## tous les autres outils 




    results_df = results_df._append({
        'Repo Name': repository.full_name,
        'Docker Compose Present': docker_compose_status
    }, ignore_index=True)

    return results_df





def main():
    access_token = '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'
    g = Github(access_token)

    # Create an empty DataFrame to store results
    columns = [
        'Repo Name', 'Docker Compose Present', 'Custom Images in Docker Compose',
        'MongoDB Replication', 'Master Slave Replication', 'Possible Event Sourcing',
        'Microservices in CI/CD', 'Load Balancing', 'DBs unique'
    ]
    results_df = pd.DataFrame(columns=columns)
    output_file = "./output/output.xlsx"

    with open("./extracted_data.csv", "r") as csv_file:
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