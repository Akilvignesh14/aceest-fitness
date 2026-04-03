import os
from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

# SRE Best Practice: Use environment variables to handle different environments
# This allows the test suite to override the database name.
DB_NAME = os.getenv("DB_NAME", "aceest_fitness.db")

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS clients (id INTEGER PRIMARY KEY, name TEXT, program TEXT, membership TEXT)")
    # 'INSERT OR IGNORE' prevents duplicate errors on re-runs
    cur.execute("INSERT OR IGNORE INTO clients (id, name, program, membership) VALUES (1, 'Admin User', 'General', 'Active')")
    conn.commit()
    conn.close()

@app.route('/')
def home():
    """Phase 1: Foundational service endpoint"""
    return jsonify({"status": "ACEest Fitness System Online", "version": "3.2.4"})

@app.route('/client/<name>')
def get_client(name):
    """Phase 1: Modular service endpoint for client retrieval"""
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT * FROM clients WHERE name=?", (name,))
    row = cur.fetchone()
    conn.close()
    
    if row:
        return jsonify({
            "id": row[0],
            "name": row[1],
            "program": row[2],
            "membership": row[3]
        })
    return jsonify({"error": "Client not found"}), 404

if __name__ == "__main__":
    init_db()
    app.run(host='0.0.0.0', port=5000)