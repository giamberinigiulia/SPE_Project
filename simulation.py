import subprocess
import itertools

# s_a_pairs = [((10, 5), (5, 10), (10, 10)) ]
# k_values = [1, 2, 4]

s_a_pairs = [(10, 10)]
k_values = [3,5,7]

for (s, a), k in itertools.product(s_a_pairs, k_values):
    command = f"python main.py run -s {str(s)} -a {str(a)} -u 1 15 -t 300 -k {str(k)}"

    print(f"Running: {(command)}")

    try:
        result = subprocess.run(command,  shell=True, check=True)
        print(f"Finished: {(command)}\n")
        # wait enough time to let the gunicorn processes to be shutted down
        subprocess.run("sleep 20", shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running: {(command)}")
        print(f"Error message: {e}")
        print(e.stderr)  # Print error output for more details