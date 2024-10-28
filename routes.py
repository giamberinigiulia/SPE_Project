import csv
import random
import time
from flask import jsonify, send_file
import os
import numpy as np
from analysis import DelayAnalyzer
from plotting import PlotGenerator
from tasks import CPUBoundTask

def setup_routes(app):
    # retrieve mu value from configuration attributes of the app
    mu = app.config.get('MU')
    
    # inizialize the delay_analyzer and the plot_generator with file names
    delay_analyzer = DelayAnalyzer(app.config['csv_path'])
    plot_generator = PlotGenerator(app.config['images_path'])

    @app.route('/', methods=['GET'])
    def process_task():
        random.seed(42)
        #start_time = time.time()
        # Sample the delay time and perform a CPU bound operation, then log the delay in the csv file
        delay = np.random.exponential(1.0 / mu)
        CPUBoundTask.run(delay)
        # end_time = time.time()
        # delay_analyzer.log_delay_to_csv(mu, end_time-start_time)
        delay_analyzer.log_delay_to_csv(mu, delay)
        return jsonify({"message": "Task completed", "duration": delay})

    @app.route('/plot/', methods=['GET'])
    def plot():
        # Evaluate the mean mu observed in the csv and generate the empirical distribution plot
        mean_delay, n = delay_analyzer.mean_mu_observed(mu)
        values_observed = delay_analyzer.empirical_distribution(mu)
        plot_generator.generate_exponential_plot(mu, mean_delay, values_observed, n)
        return send_file(app.config['images_path'], mimetype='image/png')

    @app.route('/reset', methods=['GET'])
    def reset():
        # delete the csv file related to this server (launched with that mu)
        if os.path.isfile(app.config['csv_path']):
            os.remove(app.config['csv_path'])
        return jsonify({"message": "Reset completed"})

    @app.route('/csv', methods=['GET'])
    def delays():
        # return the html table with the content of the csv file related to this server (launched with that mu)
        if os.path.isfile(app.config['csv_path']):
            with open(app.config['csv_path'], 'r') as csvfile:
                csvreader = csv.reader(csvfile)
                headers = next(csvreader)
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