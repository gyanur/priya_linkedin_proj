import argparse
import paramiko
import logging

# Set up logging to write to a file
logging.basicConfig(filename='newrelic_install.log', level=logging.INFO)

# SSH credentials for the remote server

parser = argparse.ArgumentParser()
parser.add_argument('hostname', type=str, help='Remote server hostname')
parser.add_argument('username', type=str, help='Remote server username')
#parser.add_argument('password', type=str, help='Remote server password')
parser.add_argument('privkey', type=str, help='Path to private key file')
parser.add_argument('license_key', type=str, help='New Relic license key')
args = parser.parse_args()

# Assign values to variables
ssh_hostname = args.hostname
ssh_username = args.username
ssh_key = args.privkey
#ssh_password = args.password

# New Relic license key
newrelic_license_key = args.license_key

print (ssh_hostname)
print (ssh_username)
print (ssh_key)
print (newrelic_license_key)

# Commands to install New Relic Infrastructure agent
install_commands = [
    "sudo sh -c 'echo deb http://apt.newrelic.com/debian/ newrelic non-free >> /etc/apt/sources.list.d/newrelic.list'",
    "wget -O- https://download.newrelic.com/548C16BF.gpg | sudo apt-key add -",
    "sudo apt-get update",
    f"sudo apt-get install newrelic-sysmond -y -q -o NEWRELIC_LICENSE_KEY={newrelic_license_key}"
]

status_command = 'service newrelic-sysmond status'

# Connect to the remote server over SSH
ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
key= paramiko.RSAKey.from_private_key_file(ssh_key)
ssh_client.connect(hostname=ssh_hostname, username=ssh_username, pkey=key)
#ssh_client.connect(hostname=ssh_hostname, username=ssh_username, password= ssh_password)

# Execute the commands to install New Relic agent and write output to log file
for command in install_commands:
    stdin, stdout, stderr = ssh_client.exec_command(command)


# Execute the status command and write output to log file
stdin, stdout, stderr = ssh_client.exec_command(status_command)
status_output = stdout.read().decode('utf-8')
if 'running' in status_output:
    logging.info("New Relic agent is running.")
else:
    logging.warning("New Relic agent is not running.")
    logging.warning(f"Cause: {status_output}")


# Close the SSH connection
ssh_client.close()
