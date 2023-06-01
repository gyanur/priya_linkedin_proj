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
parser.add_argument('app_name', type=str, help='Name of the application')
parser.add_argument('language', type=str, help='Programming language of the application')
args = parser.parse_args()

# Assign values to variables
ssh_hostname = args.hostname
ssh_username = args.username
ssh_key = args.privkey
#ssh_password = args.password

# New Relic license key and APM settings
newrelic_license_key = args.license_key
app_name = args.app_name
language = args.language.lower()

# Commands to install New Relic APM agent
if language == 'go':
    install_commands = [
        "curl https://download.newrelic.com/go-agent/go-agent-latest.tar.gz | sudo tar zx -C /usr/local",
        f"sudo newrelic-admin set-app-name {app_name}",
        f"sudo newrelic-admin generate-config {newrelic_license_key} /usr/local/newrelic/newrelic.cfg",
        "sudo systemctl restart newrelic-daemon.service"
    ]
elif language == 'java':
    install_commands = [
        "sudo sh -c 'echo deb http://apt.newrelic.com/debian/ newrelic non-free >> /etc/apt/sources.list.d/newrelic.list'",
        "wget -O- https://download.newrelic.com/548C16BF.gpg | sudo apt-key add -",
        "sudo apt-get update",
        "sudo apt-get install -y openjdk-8-jdk",
        f"sudo apt-get install newrelic-java -y -q -o NEWRELIC_LICENSE_KEY={newrelic_license_key}",
        f"sudo newrelic-admin set-app-name {app_name}",
        "sudo systemctl restart newrelic-daemon.service"
    ]
elif language == 'dotnet':
    install_commands = [
        "sudo sh -c 'echo deb http://apt.newrelic.com/debian/ newrelic non-free >> /etc/apt/sources.list.d/newrelic.list'",
        "wget -O- https://download.newrelic.com/548C16BF.gpg | sudo apt-key add -",
        "sudo apt-get update",
        f"sudo apt-get install newrelic-dotnet-agent -y -q -o NEWRELIC_LICENSE_KEY={newrelic_license_key}",
        f"sudo newrelic-admin set-app-name {app_name}",
        "sudo systemctl restart newrelic-daemon.service"
    ]
elif language == 'node':
    install_commands = [
        "curl -sL https://deb.nodesource.com/setup_14.x | sudo -E bash -",
        "sudo apt-get install -y nodejs",
        f"sudo npm install -g newrelic --unsafe-perm=true",
        f"sudo newrelic-admin set-app-name {app_name}",
        f"sudo newrelic-admin generate-config {newrelic_license_key} newrelic.js",
        "sudo systemctl restart newrelic-daemon.service"
    ]
elif language == 'php':
    install_commands = [
        "sudo sh -c 'echo deb http://apt.newrelic.com/debian/ newrelic non-free >> /etc/apt/sources.list.d/newrelic.list'",
        "wget -O- https://download.newrelic.com/548C16BF.gpg | sudo apt-key add -",
        "sudo apt-get update",
        f"sudo apt-get install newrelic-php5 -y -q -o NEWRELIC_LICENSE_KEY={newrelic_license_key}",
        f"sudo newrelic-install install",
        f"sudo newrelic-admin set-app-name {app_name}",
        "sudo systemctl restart newrelic-daemon.service"
    ]
elif language == 'python':
    install_commands = [
        "sudo apt-get install -y python3-pip",
        "sudo pip3 install newrelic",
        f"sudo newrelic-admin generate-config {newrelic_license_key} newrelic.ini",
        f"sudo newrelic-admin run-program python app.py",
    ]
elif language == 'ruby':
    install_commands = [
        "sudo sh -c 'echo deb http://apt.newrelic.com/debian/ newrelic non-free >> /etc/apt/sources.list.d/newrelic.list'",
        "wget -O- https://download.newrelic.com/548C16BF.gpg | sudo apt-key add -",
        "sudo apt-get update",
        f"sudo apt-get install newrelic-sysmond -y -q -o NEWRELIC_LICENSE_KEY={newrelic_license_key}",
        f"sudo nrsysmond-config --set license_key={newrelic_license_key}",
        "sudo systemctl restart newrelic-sysmond.service",
        f"sudo newrelic-admin set-app-name {app_name}",
        "sudo systemctl restart newrelic-daemon.service"
    ]
else:
    logging.error(f"Unsupported language: {language}")
    exit()

status_command = 'sudo systemctl status newrelic-daemon.service'

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