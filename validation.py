from github import Github
import pandas as pd
from outils.utils.check_microservice import microservice_keywords
from outils.utils.check_directories_size import  services_size



def main():
    access_token = ''
    print("RETRO ANALYSE")
    access_token = ''
    g = Github(access_token)


    columns_validation = ['Repo Name', 'Microservice or not','Giant Service']
    validation_df = pd.DataFrame(columns=columns_validation)
    validation_output_file = "./output/validation.xlsx"


    with   open("./extracted_data.csv", "r") as csv_file:
        for line in csv_file:
            repo_name = line.strip()
            repository = g.get_repo(repo_name)
            print(repository)
            try:

                result_validation = microservice_keywords().identify_microservice_keywords(repository)
                is_large, largest_directory, largest_directory_size, average_size = services_size().is_large_directory(repository)

                validation_df = validation_df._append({
                    'Repo Name': repository.full_name,
                    'Microservice or not': result_validation,
                    'Giant Service': largest_directory,
                    'Giant service size': largest_directory_size,
                    'Average_size': average_size
                }, ignore_index=True)

                save_to_excel(validation_df, validation_output_file)
                print(validation_df)
            except Exception as e:
                print("ERROR : ", e)
                continue


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