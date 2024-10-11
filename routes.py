import csv
from flask import jsonify, send_file
import numpy as np
from tasks import cpu_bound_task, log_delay_to_csv
from analysis import analyze_csv
from plotting import generate_exponential_plot
import os


image_path = "plot.png"  # Path for saving the plot image
file_path = "request_delays.csv"

def setup_routes(app):    
    @app.route('/<float:mu>', methods=['GET'])
    def process_task(mu):
        # mu = float(request.args.get('mu', 1.0))  # Default mu value
        
        # Generate a delay based on the exponential distribution with rate 'mu'
        delay = np.random.exponential(1.0 / mu)
        
        # Simulate the CPU-bound task for the duration of the 'delay'
        cpu_bound_task(delay)
        
        # Log the delay to the CSV file
        log_delay_to_csv(mu, delay, file_path)

        # Return a JSON response indicating the task was completed
        return jsonify({"message": "Task completed", "duration": delay})

# # Route to display a list of buttons for each distinct 'mu' value in the CSV file
    # @app.route('/plot', methods=['GET'])
    # def plotSelection():
    #     mu_values = set()
        
    #     # Check if the file exists
    #     if os.path.isfile(file_path):
    #         with open(file_path, 'r') as csvfile:
    #             csvreader = csv.reader(csvfile)
    #             next(csvreader)  # Skip headers
    #             for row in csvreader:
    #                 mu_values.add(float(row[0]))

    #     # Render the template with the list of mu values
    #     return render_template('plot_selection.html', mu_values=sorted(mu_values))  # Pass sorted values for clarity

    @app.route('/plot/<float:mu>', methods=['GET'])
    def plot(mu):
        # mu = float(request.args.get('mu', 1.0))  # Default mu value
        mean_delay = analyze_csv(file_path, mu)  # Get the mean delay
        generate_exponential_plot(mu, mean_delay, image_path)  # Generate the plot
        return send_file(image_path, mimetype='image/png')  # Return the image plot       

    @app.route('/reset', methods=['GET'])
    def reset():
        # Remove the CSV file if it exists
        if os.path.isfile(file_path):
            os.remove(file_path)
        
        # Return an HTTP response
        return jsonify({"message": "Reset completed"})

    @app.route('/csv', methods=['GET'])
    def delays():
        """Display the CSV file contents as an interactive HTML table with DataTables."""
        if os.path.isfile(file_path):
            with open(file_path, 'r') as csvfile:
                csvreader = csv.reader(csvfile)
                headers = next(csvreader)

                # Building the HTML page with DataTables
                table_data = '''
                <html>
                <head>
                    <title>Request Delays Table</title>
                    <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.11.5/css/jquery.dataTables.css">
                    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
                    <script type="text/javascript" charset="utf8" src="https://cdn.datatables.net/1.11.5/js/jquery.dataTables.js"></script>
                    <script>
                        $(document).ready(function() {{
                            $('#delayTable').DataTable();
                        }});
                    </script>
                </head>
                <body>
                    <h1>Request Delays Table</h1>
                    <table id="delayTable" class="display" style="width:100%">
                    <thead><tr>{}</tr></thead><tbody>
                '''.format(''.join(['<th>{}</th>'.format(h) for h in headers]))

                # Adding table rows for each entry
                for row in csvreader:
                    table_data += '<tr>{}</tr>'.format(''.join(['<td>{}</td>'.format(r) for r in row]))
                
                table_data += '''
                    </tbody></table>
                </body>
                </html>
                '''

                return table_data
        else:
            return "No data found"
