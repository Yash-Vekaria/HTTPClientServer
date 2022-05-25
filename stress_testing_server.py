import subprocess
import sys

n_clients = 100
processes = []
script_name = 'non_persistent_http_client.py'
# script_name = 'persistent_http_client.py'

for i in range(n_clients):
    print(i)
    output_file =  './Load Testing Output/Client_' + str(i) + '.txt'
    sys.stdout = open(output_file, 'w')
    proc = subprocess.Popen(['python3', script_name], stdout=sys.stdout, stderr=subprocess.STDOUT)
    processes.append(proc)

for proc in processes:
    proc.wait()
