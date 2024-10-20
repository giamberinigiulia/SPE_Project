from flask import Flask
import sys

from routes import setup_routes

# Create a new Flask application
app = Flask(__name__)

# Check if the correct number of arguments is provided
if len(sys.argv) != 2:
    print("Usage: python app.py <mu_value>")
    sys.exit(1)

# Retrieve and convert the mu parameter
try:
    mu_value = float(sys.argv[1])
except ValueError:
    print("Error: The mu parameter must be a float.")
    sys.exit(1)

# Store the mu parameter in the Flask app configuration
app.config['MU'] = mu_value

print(f"Starting Flask app with mu = {app.config['MU']}")

# SetUp the entry points of the application
setup_routes(app)

if __name__ == '__main__':
    app.run(threaded=False)  # Disable multithreading

