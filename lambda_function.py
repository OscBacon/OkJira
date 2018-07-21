import os
import requests
import json

JIRA_URL = os.environ["JIRA_URL"]
JIRA_USERNAME = os.environ["JIRA_USERNAME"]
JIRA_TOKEN = os.environ["JIRA_TOKEN"]
PROJECT_KEY = os.environ["PROJECT_KEY"]
JIRA_IMAGE_URL = "https://atlassianblog.wpengine.com/wp-content/uploads/2017/11/featureimage.png"

def lambda_handler(event, context):
    parameters = event["queryResult"]["parameters"]

    title = parameters.get("title")
    issue_type = parameters.get("issue-type")
    description = parameters.get("description")

    print(title, issue_type, description)
    if not title or not issue_type or not description:
        return json.dumps({"fulfillmentText":
                           "Hm... Something went wrong. \n Try again!"})

    fields = {
        "project": {"key": PROJECT_KEY},
        "summary": title.capitalize(),
        "issuetype": {"name": issue_type.capitalize()},
        "description": description.capitalize()
    }

    components = parameters.get("components")
    print(components)
    if components:
        fields["components"] = [{"name": component}
                                for component in components]

    rv = requests.post(JIRA_URL + "/rest/api/2/issue/",
                        json={"fields": fields},
                        headers={"Content-Type": "application/json"},
                        auth=(JIRA_USERNAME, JIRA_TOKEN))
    if rv.status_code == 201:
        response_data = rv.json()
        ticket_key = "SQR-1234"
        return {
            "fulfillmentText": "Ticket created with key {}".format(ticket_key),
            "fulfillmentMessages":  [{
                "card": {
                    "title": title.capitalize(),
                    "subtitle": description.capitalize(),
                    "formattedText": "Created ticket {}".format(ticket_key),
                    "imageUri": JIRA_IMAGE_URL,
                    "buttons": [{
                        "text": "View ticket",
                        "postback": "{}/browse/{}".format(JIRA_URL, ticket_key)
                    }]
                }
            }]
        }

    return {"fulfillmentText": "Hm... Something went wrong. \n Try again!"}
