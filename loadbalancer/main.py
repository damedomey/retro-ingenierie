import os
import time

from functions import clone_repo, remove_repo, is_load_balancing_configured
import argparse
import glob
tmpPath = r'tmp/' + time.time().__str__()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Clone a GitHub repository and check load balancing')

    # Add arguments
    parser.add_argument('-u', "--url", type=str, help='URL of the GitHub repository to clone')

    # Parse arguments
    args = parser.parse_args()

    # Clone the repository
    clone_repo(args.url, tmpPath)

    conf_files = glob.glob(os.path.join(tmpPath, '**', '*.conf'), recursive=True)

    is_nginx_balancing = False
    for file in conf_files:
        # Skip files within node_modules directories
        if 'node_modules' in file:
            continue
        if is_load_balancing_configured(file):
            is_nginx_balancing = True
            break

    if is_nginx_balancing:
        print("The configuration is set up for load balancing.")
    else:
        print("The configuration is not set up for load balancing.")
