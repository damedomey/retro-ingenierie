import gc
import re
import shutil
import time

from git import Repo
import os


def clone_repo(repo_url, target_dir):
    """
    Clones a public GitHub repository to a specified directory using GitPython.

    :param repo_url: URL of the GitHub repository to clone.
    :param target_dir: Directory where the repository will be cloned.
    """
    try:
        # Remove existing content in the target directory
        if os.path.exists(target_dir):
            shutil.rmtree(target_dir)

        # Create the directory
        os.makedirs(target_dir)

        Repo.clone_from(repo_url, target_dir)
        print(f"Repository cloned successfully into {target_dir}")
    except Exception as e:
        print(f"An error occurred while cloning the repository: {e}")


def remove_repo(target_dir):
    """
    Tries to remove the cloned Git repository directory with retries.

    :param target_dir: Directory where the repository was cloned.
    """
    """
        Tries to remove the cloned Git repository directory with retries.

        :param target_dir: Directory where the repository was cloned.
        """
    max_attempts = 3
    for attempt in range(max_attempts):
        try:
            if os.path.exists(target_dir):
                shutil.rmtree(target_dir)
                print(f"Repository at '{target_dir}' has been removed.")
                break
        except PermissionError as e:
            print(f"Attempt {attempt + 1}/{max_attempts}: Unable to remove repository due to permission error: {e}")
            time.sleep(2)  # Wait for 2 seconds before retrying
            gc.collect()
    else:
        print(f"Failed to remove the repository at '{target_dir}' after {max_attempts} attempts.")


def is_load_balancing_configured(file_path):
    try:
        with open(file_path, 'r') as file:
            print("Analysing ", file_path, "...")
            content = file.read()

            # Find all upstream blocks
            upstream_blocks = re.findall(r'(?<!#.\*)(upstream\s+(?!server)[\w-]+\s*{[^}]*})', content, re.DOTALL)

            for block in upstream_blocks:
                # Count the number of uncommented server entries in each upstream block
                server_lines = block.split('\n')
                server_count = sum('server' in line and not line.strip().startswith('#') for line in server_lines)

                # If any upstream block has more than one server, it's load balancing
                if server_count > 1:
                    return True

            return False

    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return False
