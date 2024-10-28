import subprocess
import sys
import time


if __name__ == '__main__':
    # retrieve from command line n_client, lambda, maxtime, mu
    print(sys.argv)
    mu = sys.argv[1]
    lambda_val = sys.argv[2]
    maxtime = sys.argv[3]
    n_client = sys.argv[4]
    help_message = f"Usage: python main.py <mu> <lambda> <maxtime> <n_client>"
    
    subprocess.Popen(['start','cmd','/k', f'py server/app.py {str(mu)}'], shell=True)
    time.sleep(2)
    subprocess.Popen(['start','cmd','/k', "py load_generator/test_generator.py"], shell=True)

    #subprocess.run([sys.executable, './server/app.py', str(mu)])