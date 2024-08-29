import requests
import json

# Load configuration
from config import *

# Updated GraphQL query to retrieve fields directly from the ProjectV2
query = """
query($owner: String!, $repo: String!, $projectNumber: Int!) {
  repository(owner: $owner, name: $repo) {
    projectV2(number: $projectNumber) {
      id
      title
      fields(first: 100) {
        nodes {
          id
          name
          ... on ProjectV2FieldCommon {
            dataType
          }
          ... on ProjectV2SingleSelectField {
            options {
              id
              name
            }
          }
        }
      }
    }
  }
}
"""

headers = {
    'Authorization': f'token {gh_token}',
    'Content-Type': 'application/json',
}

def fetch_project_fields(owner, repo, project_number):
    variables = {
        "owner": owner,
        "repo": repo,
        "projectNumber": project_number,
    }

    response = requests.post(
        api_endpoint,
        headers=headers,
        json={'query': query, 'variables': variables}
    )

    if response.status_code == 200:
        response_data = response.json()

        # Check if the response contains errors
        if 'errors' in response_data:
            print("GraphQL errors occurred:")
            for error in response_data['errors']:
                print(error['message'])
            return None

        return response_data

    else:
        print(f"Error fetching project fields: {response.status_code} - {response.text}")
        return None

def check_project_fields():
    # Fetch fields for the specific project
    data = fetch_project_fields(repository_owner, repository_name, project_number)

    if data and 'data' in data:
        project = data['data']['repository']['projectV2']
        fields = project['fields']['nodes']

        print(f"Fields for Project '{project['title']}':")
        for field in fields:
            print(f"- {field['name']} (ID: {field['id']}, Type: {field['dataType']})")
            if 'options' in field:
                print("  Options:")
                for option in field['options']:
                    print(f"  - {option['name']} (ID: {option['id']})")
    else:
        print("No data received from the API.")

if __name__ == "__main__":
    check_project_fields()
