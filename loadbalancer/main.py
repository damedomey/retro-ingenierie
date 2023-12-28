import os
import time
import csv
import argparse
import glob

from functions import clone_repo, remove_repo, is_load_balancing_configured


def process_repo(url, tmpPath):
    clone_repo(url, tmpPath)
    conf_files = glob.glob(os.path.join(tmpPath, '**', '*.conf'), recursive=True)

    is_nginx_balancing = False
    for file in conf_files:
        if 'node_modules' in file:
            continue
        if is_load_balancing_configured(file):
            is_nginx_balancing = True
            break

    return is_nginx_balancing


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Clone GitHub repositories and check load balancing')

    # Add arguments
    parser.add_argument('-u', "--url", type=str, help='URL of the GitHub repository or path to CSV file', required=True)
    parser.add_argument('--list-true', action='store_true', help='List repositories with load balancing configured')
    parser.add_argument('--list-false', action='store_true', help='List repositories without load balancing configured')

    # Parse arguments
    args = parser.parse_args()

    list_true_repos = []
    list_false_repos = []

    if args.url.endswith('.csv'):
        with open(args.url, newline='') as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                repo_url = row[0]  # Assuming the URL is in the first column
                tmpPath = 'tmp/' + time.time().__str__()
                is_balancing = process_repo(repo_url, tmpPath)
                if is_balancing:
                    list_true_repos.append(repo_url)
                else:
                    list_false_repos.append(repo_url)

            print(f"Load balancing configured: {len(list_true_repos)}, Not configured: {len(list_false_repos)}")

            if args.list_true:
                print("Repositories with load balancing configured:")
                for repo in list_true_repos:
                    print(repo)

            if args.list_false:
                print("Repositories without load balancing configured:")
                for repo in list_false_repos:
                    print(repo)

    else:
        tmpPath = 'tmp/' + time.time().__str__()
        is_balancing = process_repo(args.url, tmpPath)
        if is_balancing:
            print("The configuration is set up for load balancing.")
        else:
            print("The configuration is not set up for load balancing.")
