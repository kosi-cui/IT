from flask import Flask, send_from_directory, request
import os
import subprocess
import unittest
import argparse
import requests
import webbrowser
from dotenv import load_dotenv
from server import api_page as api
from server import settings

app = Flask(__name__)

@app.route('/')
def base():
    return send_from_directory('client/public', 'index.html')

@app.route('/check_credentials')
def check_credentials():
    if not os.path.exists('.env') or not validCredentials():
        return 'Invalid credentials', 401
    return 'Valid credentials'

# Credential Check
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        api_key = data.get('api_key')
        url = data.get('url')

        with open('.env', 'w') as f:
            f.write(f'API_KEY="{api_key}"\n')
            f.write(f'HELPDESK_URL="{url}"\n')

        return 'Credentials saved.'
    else:
        return send_from_directory('client/public', 'index.html')

# Path for all static files (Compiled JS, CSS, images, etc.)
@app.route('/<path:path>')
def home(path):
    return send_from_directory('client/public', path)

# API Routes
@app.route('/api/ticket/<int:ticket_id>')
def api_req(ticket_id):
    return api.ticket_get(ticket_id)

@app.route('/api/reimage_tickets')
def reimage_tickets():
    return api.get_all_reimage_tickets()


# Main
def validCredentials():
    """
    Checks if the .env file exists and if the credentials are valid.
    """
    if not os.path.exists('.env'):
        return False

    load_dotenv()  # take environment variables from .env.
    api_key = os.getenv('API_KEY')
    helpdesk_url = os.getenv('HELPDESK_URL')
    url = helpdesk_url + '/api/v2/tickets.json'
    response = requests.get(url, auth=(api_key, "X"))
    return response.status_code == 200    


def run():
    # Check if the script is running inside a Docker container
    if not os.path.exists('/.dockerenv'):
        build_client()
        webbrowser.open('http://localhost:5000')
    app.run(host='0.0.0.0', port=5000, debug=True)

def test():
    # Discover and run tests
    loader = unittest.TestLoader()
    start_dir = 'server/tests'
    suite = loader.discover(start_dir)

    runner = unittest.TextTestRunner()
    runner.run(suite)

def build_client():
    # Update the styling in the Svelte files
    settings.replace_to_color()
    # If not, navigate to the client directory and run "npm run build"
    os.chdir('client')
    subprocess.run('npm run build', shell=True, check=True)
    # Navigate back to the previous directory
    os.chdir('..')
    settings.return_to_original()

def full_build():
    # Build the client
    build_client()
    # Build the server
    os.system('docker-compose -f docker/docker-compose.yml up --build -d')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--test', action='store_true', help='Run unit tests')
    parser.add_argument('-b', '--build', action='store_true', help='Build & Run the Docker container')
    parser.add_argument('-s', '--stop', action='store_true', help='Stop the Docker container')
    args = parser.parse_args()

    if args.test:
        test()
    elif  args.build:
        full_build()
        # Open the browser at localhost:5000
        webbrowser.open('http://localhost:5000')
    elif args.stop:
        # Stop the Docker container
        os.system('docker-compose -f docker/docker-compose.yml down')
    else:
        # Build the client and run the server locally without Docker
        run()
