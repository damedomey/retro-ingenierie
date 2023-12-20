import csv
from urllib.parse import urlparse


input_file = 'C:/Users/21264/Videos/retro-ingenierie/cicd_analyze/analysis.csv'  # Remplacez par le nom de votre fichier CSV d'entrée
output_file = 'extracted_data.csv'  # Nom du fichier CSV de sortie

def extract_owner_repo(line):
    repo = line.split(';')[0].split('/')
    print(repo[1] + "/" + repo[2])
    return repo[1] + "/" + repo[2]

# Ouvrir le fichier CSV en lecture et créer un nouveau fichier CSV en écriture
with open(input_file, 'r') as csv_in_file:
    for line in csv_in_file:
        repo = extract_owner_repo(line)
        with open(output_file, 'a') as csv_out_file:
            writer = csv.writer(csv_out_file)
            writer.writerow([repo])
