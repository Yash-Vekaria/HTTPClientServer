import subprocess
import sys

script_name = 'non_persistent_http_client.py'
# script_name = 'persistent_http_client.py'
n_iter = 100

procs = []

for i in range(n_iter):
    print(i)
    # output_file =  './LoadTesting Output 10 Clients/Run_' + str(i) + '.txt'
    output_file =  './LoadTesting Output/Run_' + str(i) + '.txt'
    sys.stdout = open(output_file, 'w')
    proc = subprocess.Popen(['python3', script_name], stdout=sys.stdout, stderr=subprocess.STDOUT)
    procs.append(proc)

for proc in procs:
    proc.wait()