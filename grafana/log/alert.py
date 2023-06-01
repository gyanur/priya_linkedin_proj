import requests
import csv
import datetime
import base64

# Set the Grafana API URL and query parameters
grafana_url = "https://grafana-m1.core.tirabeauty.com/alerting/list?state=alerting"
query_params = {
    "from": int((datetime.datetime.utcnow() - datetime.timedelta(days=7)).timestamp()),
    "to": int(datetime.datetime.utcnow().timestamp())
}

# Set the authentication credentials
username = "admin"
password = "Password"

# Encode the credentials using base64
credentials = base64.b64encode(f"{username}:{password}".encode()).decode()

# Send the GET request to the Grafana API endpoint with the query parameters and authentication headers
headers = {
    "Authorization": f"Basic {credentials}"
}
response = requests.get(grafana_url, headers=headers, params=query_params)

# If the request was successful, write the alerts to a CSV file
if response.status_code == 200:
    alerts = response.json()
    # with open("alerts.csv", "w", newline="") as csvfile:
    #     writer = csv.writer(csvfile)
    #     writer.writerow(["Dashboard", "Panel", "Time", "State", "Message"])
    #     for alert in alerts:
    #         writer.writerow([alert["dashboardTitle"], alert["panelTitle"],
    #                         datetime.datetime.fromtimestamp(alert["time"]).isoformat(),
    #                         alert["state"], alert["message"]])
    print(alerts)
    print("Alerts written to alerts.csv")
else:
    print("Error: Failed to retrieve alerts from Grafana API.")
