from .templatepersister import TemplatePersister
import os, subprocess, shutil, tempfile


# Evaluate whether it's worth updating this Class to use GitPython in the future
class GithubPersistence(TemplatePersister):
    def __init__(self):
        gh_token = os.environ.get('GITHUB_TOKEN')
        if gh_token is not None:
            subprocess.run(["gh", "auth", "login", "--with-token"], input=gh_token.encode())

    def persist(self, output_path, destination):
        # persistence logic goes here
        print("persisting template to github repo")
        self.create_github_repo(destination, "private")
        with tempfile.TemporaryDirectory() as temp_dir:
            self.clone_repo(repo_name=destination, clone_path=temp_dir)
            self.copy_output_to_repo(output_path=output_path, repo_path=temp_dir)
            self.commit_and_push(temp_dir)

    @staticmethod
    def create_github_repo(repo_name, repo_type):
        try:
            subprocess.run(["gh", "repo", "create", repo_name, f"--{repo_type}"], check=True)
            print(f"Repository: {repo_name} has been created successfully")
        except subprocess.CalledProcessError as e:
            print(f"Failed to create repository: {e}")

    @staticmethod
    def clone_repo(repo_name, clone_path):
        try:
            subprocess.run(["gh", "repo", "clone", repo_name, clone_path], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Failed to clone repository: {e}")

    @staticmethod
    def copy_output_to_repo(output_path, repo_path):
        if not os.path.exists(output_path):
            print("Output path does not exist")
            exit(1)
        try:
            single_directory = next((os.path.join(output_path, item) for item in os.listdir(output_path) if os.path.isdir(os.path.join(output_path, item))), None)
            print(f"single directory: {single_directory}")
            if single_directory is None:
                print(f"Output path: {output_folder_name} does not contain a folder")
                exit(1)

            for item in os.listdir(single_directory):
                src = os.path.join(single_directory, item)
                dst = os.path.join(repo_path, item)
                print(f"copying {src} to {dst}")
                if os.path.isdir(src):
                    shutil.copytree(src, dst, dirs_exist_ok=True)
                else:
                    shutil.copy2(src, dst)
            print("Templates copied successfully")
        except Exception as e:
            print(f"Failed to copy templates to destination repo: {e}")

    @staticmethod
    def commit_and_push(repo_path):
        try:
            subprocess.run(["git", "add", "."], cwd=repo_path)
            subprocess.run(["git", "commit", "-m", f"Pushing files in {repo_path}"], cwd=repo_path)
            subprocess.run(["git", "push"], cwd=repo_path)
        except subprocess.CalledProcessError as e:
            print(f"Failed to commit and push to new repo: {e}")
