import argparse
import paramiko
import logging

# Set up logging to write to a file
logging.basicConfig(filename='newrelic_logs_install.log', level=logging.INFO)

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

# Commands to install New Relic Logs agent
install_commands = [
    "curl -Ls https://download.newrelic.com/nrlinux/infra/agent/newrelic-infra.gpg | sudo apt-key add -",
    "echo \"deb [arch=amd64] https://download.newrelic.com/nrlinux/infra/agent/$(lsb_release -i -s | awk '{print tolower($0)}')/$(lsb_release -cs) binary/\" | sudo tee /etc/apt/sources.list.d/newrelic-infra.list",
    "sudo apt-get update",
    "sudo apt-get install newrelic-infra -y",
    f"sudo sh -c 'echo license_key: {newrelic_license_key} >> /etc/newrelic-infra.yml'",
    "sudo systemctl restart newrelic-infra"
]

status_command = 'sudo newrelic-infra nrl-lookback 5m'

# Connect to the remote server over SSH
ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
key= paramiko.RSAKey.from_private_key_file(ssh_key)
ssh_client.connect(hostname=ssh_hostname, username=ssh_username, pkey=key)

# Execute the commands to install New Relic Logs agent and write output to log file
for command in install_commands:
    stdin, stdout, stderr = ssh_client.exec_command(command)
    logging.info(stdout.read().decode('utf-8'))

# Execute the status command and write output to log file
stdin, stdout, stderr = ssh_client.exec_command(status_command)
status_output = stdout.read().decode('utf-8')
if 'No logs found' not in status_output:
    logging.info("New Relic Logs agent is running.")
else:
    logging.warning("New Relic Logs agent is not running.")
    logging.warning(f"Cause: {status_output}")

# Close the SSH connection
ssh_client.close()
