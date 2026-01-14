from flask import Flask, render_template, jsonify
import os

app = Flask(__name__)

@app.route("/")
def index():
    # Force rendering the HTML file
    return render_template('index.html')

@app.route("/health")
def health():
    return "OK", 200

if __name__ == "__main__":
    # Ensure port 8080 for OpenShift
    app.run(host="0.0.0.0", port=8080)
