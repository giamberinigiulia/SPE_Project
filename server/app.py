from flask import Flask
import sys

from routes import setup_routes

# Create a new Flask application
app = Flask(__name__)

def setup():

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

    file_path = "./data/csv/request_delays"
    image_path = "./data/images/plot"
    extensionFileName = "_" + str(app.config['MU']).split('.')[0] + "_" + str(app.config['MU']).split('.')[1]
    app.config['csv_path'] = file_path + extensionFileName + ".csv"
    app.config['images_path'] = image_path + extensionFileName + ".png"


    # SetUp the entry points of the application
    setup_routes(app)

if __name__ == '__main__':
    setup();
    app.run(threaded=False)  # Disable multithreading

