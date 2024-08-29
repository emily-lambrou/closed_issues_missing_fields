import requests
import json

# Load configuration
from config import *

# Updated GraphQL query with the correct fields for retrieving project card information
query = """
query($owner: String!, $repo: String!, $after: String) {
  repository(owner: $owner, name: $repo) {
    issues(states: CLOSED, first: 100, after: $after) {
      nodes {
        id
        title
        projectCards(first: 100) {
          nodes {
            id
            note
            project {
              id
              name
            }
            column {
              id
              name
            }
            fieldValues(first: 100) {
              nodes {
                field {
                  name
                }
                value
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
      pageInfo {
        endCursor
        hasNextPage
      }
    }
  }
}
"""

headers = {
    'Authorization': f'token {gh_token}',
    'Content-Type': 'application/json',
}

def fetch_issues(owner, repo, after=None):
    variables = {
        "owner": owner,
        "repo": repo,
        "after": after
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
    # Initialize pagination variables
    after_cursor = None
    all_issues = []

    while True:
        # Call fetch_issues with your repository owner, name, and pagination cursor
        data = fetch_issues(repository_owner, repository_name, after_cursor)

        if data and 'data' in data:
            issues = data['data']['repository']['issues']['nodes']
            all_issues.extend(issues)

            # Check if there are more pages
            page_info = data['data']['repository']['issues']['pageInfo']
            if page_info['hasNextPage']:
                after_cursor = page_info['endCursor']
            else:
                break  # No more pages

        else:
            print("No data received from the API.")
            break

    for issue in all_issues:
        comments = issue['comments']['nodes']
        if not comment_exists(comments):
            missing_fields = []
            project_cards = issue['projectCards']['nodes']
            
            for card in project_cards:
                field_values = [fv['field']['name'] for fv in card['fieldValues']['nodes']]
                
                required_fields = [status_field_name, duedate_field_name, timespent_field_name,
                                   release_field_name, estimate_field_name, priority_field_name,
                                   size_field_name, week_field_name]

                for field in required_fields:
                    if field not in field_values:
                        missing_fields.append(field)
                
                if missing_fields:
                    print(f"Issue ID: {issue['id']} has missing fields: {missing_fields}")
                    add_comment(issue['id'])

if __name__ == "__main__":
    check_issues()
