import os
from flask import Flask, render_template, request, jsonify
import requests
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

app1 = Flask(__name__)


@app1.route('/')
def index():
    return render_template('form.html')


# Define the URL of the external microservice
EXTERNAL_MICROSERVICE_URL = os.getenv('EXTERNAL_MICROSERVICE_URL')


@app1.route('/process', methods=['POST'])
def process_form():
    # Specify the path to your file
    file_path = os.getenv('FILE_PATH')

    # Initialize an empty string to store the file content
    file_content = ""

    try:
        with open(file_path, 'r') as file:
            file_content = file.read()
        print('File Content is------------>', file_content)

        # Send data to an external microservice with content type "application/json"
        headers = {'Content-Type': 'application/json',
                   'X-user': request.form.get('user')}

        data = file_content.replace("$region", request.form.get('region')).replace("$endpoint_type", request.form.get(
            'endpoint_type')).replace("$tags", request.form.get('tags')).replace("$user", request.form.get('user'))

        # Add custom headers to the response
        response = requests.post(EXTERNAL_MICROSERVICE_URL, json=data, headers=headers)
        return jsonify(response.json())

    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
    except PermissionError:
        print(f"Permission denied for '{file_path}'.")
    except Exception as e:
        print(f"An error occurred while fetching content for MFT Self service Interface: {str(e)}")


if __name__ == '__main__':
    app1.run(debug=True, host='0.0.0.0', port=4000)