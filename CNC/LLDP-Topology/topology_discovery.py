import paramiko, time
import os

try:
    os.mkdir('devices')
except:
    print("already_created")

with open('sw_addresses.conf', 'r') as address_file:
    addresses=address_file.read().split('\n')
    print(addresses, type(addresses))

for ip in addresses:
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, username='soc-e', password='soc-e')
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('sudo lldpcli show neighbors')
    time.sleep(1)
    data = ssh_stdout.readlines()
    with open('devices/topology_'+ ip + '.txt', 'a') as f:
        for line in data:
            f.write(str(line) + '\n')