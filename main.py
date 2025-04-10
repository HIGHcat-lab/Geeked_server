from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json

app = Flask(__name__)
CORS(app)

LINKS_FILE = os.path.join('/tmp', 'links.json')

# Ensure file exists
if not os.path.exists(LINKS_FILE):
    with open(LINKS_FILE, 'w') as f:
        json.dump([], f)

@app.route('/submit-link', methods=['POST'])
def submit_link():
    data = request.get_json()
    name = data.get('name')
    url = data.get('url')

    if not name or not url:
        return jsonify({'error': 'Missing name or URL'}), 400

    with open(LINKS_FILE, 'r+') as f:
        links = json.load(f)
        if any(link['name'] == name for link in links):
            return jsonify({'error': 'Name already exists'}), 409

        links.append({'name': name, 'url': url})
        f.seek(0)
        json.dump(links, f, indent=2)

    return jsonify({'message': 'Link saved'}), 200

@app.route('/get-links', methods=['GET'])
def get_links():
    with open(LINKS_FILE, 'r') as f:
        links = json.load(f)
    return jsonify(links)

if __name__ == '__main__':
    app.run(debug=True)
