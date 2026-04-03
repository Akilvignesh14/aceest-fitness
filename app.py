from flask import Flask, jsonify

app = Flask(__name__)

# This is your "self.programs" dictionary, moved from the desktop app to the web app
GYM_PROGRAMS = {
    "Fat Loss (FL)": {
        "workout": "Mon: 5x5 Back Squat + AMRAP; Tue: EMOM 20min Assault Bike",
        "diet": "B: 3 Egg Whites + Oats Idli; L: Grilled Chicken + Brown Rice",
        "color": "#e74c3c"
    },
    "Muscle Gain (MG)": {
        "workout": "Mon: Squat 5x5; Tue: Bench 5x5; Wed: Deadlift 4x6",
        "diet": "B: 4 Eggs + PB Oats; L: Chicken Biryani",
        "color": "#2ecc71"
    }
}

@app.route('/')
def home():
    return "<h1>Welcome to ACEest Fitness & Gym Portal</h1><p>Check /programs to see our plans.</p>"

@app.route('/programs')
def get_programs():
    # This sends the dictionary data to the web browser
    return jsonify(GYM_PROGRAMS)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)