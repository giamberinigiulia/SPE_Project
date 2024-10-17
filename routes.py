import csv
from flask import jsonify, render_template, send_file
import os
import numpy as np
from analysis import DelayAnalyzer
from plotting import PlotGenerator
from tasks import CPUBoundTask

file_path = "request_delays.csv"
image_path = "plot.png"

def setup_routes(app):    
    delay_analyzer = DelayAnalyzer(file_path)
    plot_generator = PlotGenerator(image_path)

    @app.route('/<float:mu>', methods=['GET'])
    def process_task(mu):
        delay = np.random.exponential(1.0 / mu)
        CPUBoundTask.run(delay)
        delay_analyzer.log_delay_to_csv(mu, delay)
        return jsonify({"message": "Task completed", "duration": delay})

    @app.route('/plot/<float:mu>', methods=['GET'])
    def plot(mu):
        mean_delay, _ = delay_analyzer.mean_mu_observed(mu)
        values_observed = delay_analyzer.empirical_distribution(mu)
        plot_generator.generate_exponential_plot(mu, mean_delay, values_observed)
        return send_file(image_path, mimetype='image/png')

    @app.route('/reset', methods=['GET'])
    def reset():
        if os.path.isfile(file_path):
            os.remove(file_path)
        return jsonify({"message": "Reset completed"})

    @app.route('/csv', methods=['GET'])
    def delays():
        if os.path.isfile(file_path):
            with open(file_path, 'r') as csvfile:
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

    @app.route('/plots', methods=['GET'])
    def plot_selection():
        mu_values = set()
        if os.path.isfile(file_path):
            with open(file_path, 'r') as csvfile:
                csvreader = csv.reader(csvfile)
                next(csvreader)
                for row in csvreader:
                    mu_values.add(float(row[0]))
        return render_template('plot_selection.html', mu_values=sorted(mu_values))
