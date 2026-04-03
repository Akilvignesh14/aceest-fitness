from flask import Flask, jsonify

app = Flask(__name__)

# This is a 'route'. When you visit the website, this function runs.
@app.route('/')
def home():
    return "ACEest Fitness & Gym: Server is Running!"

# An example 'endpoint' for gym members
@app.route('/status')
def status():
    return jsonify({"status": "Open", "capacity": "75%"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)