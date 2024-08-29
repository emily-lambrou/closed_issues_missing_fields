import requests
import json

# Load configuration
from config import *

# Define the GraphQL query with variables
query = """
query($owner: String!, $repo: String!) {
  repository(owner: $owner, name: $repo) {
    issues(states: CLOSED, first: 100) {
      nodes {
        id
        title
        projectCards(first: 100) {
          nodes {
            project {
              fields {
                name
              }
              items {
                fieldValues {
                  field {
                    name
                  }
                  value
                }
              }
            }
          }
        }
        comments(first: 100) {
          nodes {
            body
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

def fetch_issues(owner, repo):
    variables = {
        "owner": owner,
        "repo": repo
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
        print(f"Error fetching issues: {response.status_code} - {response.text}")
        return None

def check_issues():
    # Call fetch_issues with your repository owner and name
    data = fetch_issues(repository_owner, repository_name)

    if data and 'data' in data:  # Ensure 'data' key is present
        for issue in data['data']['repository']['issues']['nodes']:
            comments = issue['comments']['nodes']
            if not comment_exists(comments):
                missing_fields = []
                project_fields = [field['name'] for field in issue['projectCards']['nodes'][0]['project']['fields']]
                field_values = [value['field']['name'] for value in issue['projectCards']['nodes'][0]['project']['items'][0]['fieldValues']]
                
                required_fields = [status_field_name, duedate_field_name, timespent_field_name,
                                   release_field_name, estimate_field_name, priority_field_name,
                                   size_field_name, week_field_name]
                
                for field in required_fields:
                    if field not in field_values:
                        missing_fields.append(field)
                
                if missing_fields:
                    print(f"Issue ID: {issue['id']} has missing fields: {missing_fields}")
                    add_comment(issue['id'])
    else:
        print("No data received from the API.")

if __name__ == "__main__":
    check_issues()
