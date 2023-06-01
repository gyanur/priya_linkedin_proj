import argparse
import paramiko
import logging

# Set up logging to write to a file
logging.basicConfig(filename='newrelic_browser_install.log', level=logging.INFO)

# SSH credentials for the remote server

parser = argparse.ArgumentParser()
parser.add_argument('hostname', type=str, help='Remote server hostname')
parser.add_argument('username', type=str, help='Remote server username')
parser.add_argument('privkey', type=str, help='Path to private key file')
parser.add_argument('license_key', type=str, help='New Relic license key')
args = parser.parse_args()

# Assign values to variables
ssh_hostname = args.hostname
ssh_username = args.username
ssh_key = args.privkey

# New Relic license key
newrelic_license_key = args.license_key

# Commands to install New Relic Browser agent
install_commands = [
    "curl https://download.newrelic.com/NR-Apm-Host-Installer/master/linux/newrelic-browser-agent-ubuntu.deb -O",
    "sudo dpkg -i newrelic-browser-agent-ubuntu.deb",
    f"sudo newrelic-install install -a --license_key={newrelic_license_key}"
]

status_command = 'sudo service newrelic-browser-agent status'

# Connect to the remote server over SSH
ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
key= paramiko.RSAKey.from_private_key_file(ssh_key)
ssh_client.connect(hostname=ssh_hostname, username=ssh_username, pkey=key)

# Execute the commands to install New Relic agent and write output to log file
for command in install_commands:
    stdin, stdout, stderr = ssh_client.exec_command(command)
    output = stdout.read().decode('utf-8')
    if output:
        logging.info(output)
    error = stderr.read().decode('utf-8')
    if error:
        logging.error(error)

# Execute the status command and write output to log file
stdin, stdout, stderr = ssh_client.exec_command(status_command)
status_output = stdout.read().decode('utf-8')
if 'running' in status_output:
    logging.info("New Relic Browser agent is running.")
else:
    logging.warning("New Relic Browser agent is not running.")
    logging.warning(f"Cause: {status_output}")

# Close the SSH connection
ssh_client.close()
