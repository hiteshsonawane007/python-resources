from dotenv import load_dotenv
from github import Github, GithubException
from github.Repository import Repository
from flask import Flask, request, jsonify
import os
import logging
import traceback
import json
import random

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Configure logging to print logs to Docker container stdout
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# GitHub Enterprise credentials
github_token = os.getenv('GITHUB_TOKEN')
github_organization = os.getenv('GITHUB_ORGANIZATION')
github_repository = os.getenv('GITHUB_REPOSITORY')
github_base_url = os.getenv('GITHUB_BASE_URL')


def create_terraform_file(terraform_code):
    with open('terraform.tf', 'w') as f:
        f.write(terraform_code)


@app.route('/upload-terraform', methods=['POST'])
def upload_terraform():
    global path
    try:
        # Receive JSON data from the request
        #json_data = request.json
        json_data = request.get_data(as_text=True)

        # Get extra value from Header:
        user = request.headers.get('X-user')
        app.logger.info(f'User Here--->{user}')

        terraform_code = json.loads(json_data)
        app.logger.info(f'terraform_code--->{terraform_code}')

        if not terraform_code:
            return jsonify({"message": "Terraform code is missing from JSON data"}), 400

        # Create a GitHub instance using a personal access token
        g = Github(github_token, base_url=github_base_url, verify=False)

        # Get the organization
        organization = g.get_organization(github_organization)
        #app.logger.info('Here---------44')

        # Get the repository
        repo: Repository = organization.get_repo(github_repository)

        # Generate a random integer between 1 and 100 (inclusive)
        random_integer = random.randint(1, 100000)
        print("Random Integer:", random_integer)
        string_value = str(random_integer)

        # Create a new branch
        base_branch = "master"  # Change to your default branch name
        new_branch = repo.create_git_ref(f"refs/heads/{user}", repo.get_branch(base_branch).commit.sha)

        # Upload a file to the new branch
        path = 'mft_microservice/' + user + '_' + string_value + '.tf'
        branch=user
        repo.create_file(path, 'Initial commit', bytes(json_data, 'utf-8'), branch=branch)

        # Create a pull request
        pull_request_title = "Feature Request: Creating Pull Reuqest for User "+user
        pull_request_body = "This pull request adds a new file to the repository."

        pull_request = repo.create_pull(title=pull_request_title, body=pull_request_body, base=base_branch,
                                        head=branch)

        return jsonify({"message": "Terraform code uploaded successfully"}), 200

        '''# Check if the Terraform file exists in the repository
        try:
            path = 'mft_microservice/' + user+'_'+string_value+'.tf'
            contents = repo.get_contents(path, ref=os.getenv('BRANCH_NAME'))
            existing_content = contents.decoded_content.decode('utf-8')
        except GithubException as e:
            # If the file does not exist, create it
            if e.status == 404:
                repo.create_file(path, 'Initial commit', terraform_code, branch=os.getenv('BRANCH_NAME'))
                return jsonify({"message": "Terraform code uploaded successfully"}), 200
            else:
                raise

        # Compare the existing content with the new content
        if existing_content == terraform_code:
            return jsonify({"message": "Terraform code is identical; no update needed"}), 200

        # Update the Terraform file
        repo.update_file(contents.path, 'Update Terraform code', terraform_code, contents.sha, branch=os.getenv('BRANCH_NAME'))

        return jsonify({"message": "Terraform code uploaded successfully"}), 200 '''

    except GithubException as e:
        raise
    except Exception as e:
        traceback.print_exc()
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)