import requests
from requests.auth import HTTPBasicAuth

def createTicket(jira_username, jira_password, title, description, type, priority):

# Jira API endpoint for creating an issue
    jira_api_url = "https://ws-lambda.atlassian.net/rest/api/2/issue/"

    # Replace these variables with your Jira credentials and project information
    project_key = "COACHBOT"
    issue_type = type  # You can replace it with the appropriate issue type for your project

    # Issue data

    # Create a dictionary with the issue data
    issue_data = {
        "fields": {
            "project": {"key": project_key},
            "summary": title,
            "description": description,
            "issuetype": {"name": issue_type},
            "priority": {"name": priority},
            #"product": {"name": "GT School: CoachBot - TeachTap"},
        }
    }

    # Convert the issue data to JSON
    json_data = {
        "fields": issue_data["fields"]
    }

    # Set up authentication
    auth = HTTPBasicAuth(jira_username, jira_password)

    # Make the request to create the issue
    response = requests.post(
        jira_api_url,
        json=json_data,
        auth=auth,
        headers={"Content-Type": "application/json"}
    )

    # Check the response
    if response.status_code == 201:
        print("Jira issue created successfully!")
        print("Issue Key:", response.json()["key"])
        print("Issue URL:", "https://ws-lambda.atlassian.net/browse/" + response.json()["key"])
    else:
        print("Failed to create Jira issue.")
        print("Status Code:", response.status_code)
        print("Response:", response.text)