import os
import requests
import json
from config import GRAPHQL_ENDPOINT, GRAPHQL_HEADERS, required_fields

def fetch_closed_issues():
    query = """
    query {
        repository(owner: $owner, name: $repo) {
            issues(first: 100, states: [CLOSED]) {
                nodes {
                    id
                    number
                    title
                    body
                    comments(first: 100) {
                        nodes {
                            body
                        }
                    }
                    projectCards(first: 100) {
                        nodes {
                            id
                            note
                            project {
                                id
                                name
                                columns(first: 100) {
                                    nodes {
                                        id
                                        name
                                        cards(first: 100) {
                                            nodes {
                                                id
                                                note
                                                content {
                                                    ... on Issue {
                                                        id
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    """ % (repository_owner, repository_name)

    response = requests.post(GRAPHQL_ENDPOINT, headers=GRAPHQL_HEADERS, json={'query': query})
    response.raise_for_status()
    data = response.json()
    issues = data.get('data', {}).get('repository', {}).get('issues', {}).get('nodes', [])
    return issues

def get_field_value(issue_id, field_name):
    query = """
    query($issueId: ID!) {
        node(id: $issueId) {
            ... on Issue {
                projectCards(first: 100) {
                    nodes {
                        id
                        note
                        project {
                            id
                            name
                            columns(first: 100) {
                                nodes {
                                    id
                                    name
                                    cards(first: 100) {
                                        nodes {
                                            id
                                            note
                                            content {
                                                ... on Issue {
                                                    id
                                                    fieldValues(first: 100) {
                                                        nodes {
                                                            field {
                                                                ... on ProjectV2Field {
                                                                    name
                                                                    type
                                                                }
                                                            }
                                                            value
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    """
    variables = {'issueId': issue_id}
    response = requests.post(GRAPHQL_ENDPOINT, headers=GRAPHQL_HEADERS, json={'query': query, 'variables': variables})
    response.raise_for_status()
    data = response.json()
    fields = data.get('data', {}).get('node', {}).get('projectCards', {}).get('nodes', [])

    for field in fields:
        for card in field.get('project', {}).get('columns', {}).get('nodes', []):
            for card_item in card.get('cards', {}).get('nodes', []):
                if card_item.get('content', {}).get('id') == issue_id:
                    for field_value in card_item.get('note', {}).get('fieldValues', {}).get('nodes', []):
                        if field_value.get('field', {}).get('name') == field_name:
                            return field_value.get('value')
    return None

def check_missing_fields(issue):
    missing_fields = []
    for field, field_type in required_fields.items():
        field_value = get_field_value(issue['id'], field)
        if field_type == 'single_select':
            if not field_value:
                missing_fields.append(field)
        elif field_type == 'date':
            if not field_value:
                missing_fields.append(field)
        elif field_type == 'text':
            if not field_value or field_value.strip() == '':
                missing_fields.append(field)
        elif field_type == 'iteration':
            if not field_value:
                missing_fields.append(field)
    return missing_fields

def issue_has_existing_comment(issue, comment_text):
    comments = issue.get('comments', {}).get('nodes', [])
    for comment in comments:
        if comment_text in comment.get('body', ''):
            return True
    return False

def add_comment(issue_id, missing_fields):
    comment_text = "The following required fields are missing:\n"
    for field in missing_fields:
        comment_text += f"- {field}\n"
    
    mutation = """
    mutation($issueId: ID!, $body: String!) {
        addComment(input: {subjectId: $issueId, body: $body}) {
            clientMutationId
        }
    }
    """
    variables = {
        'issueId': issue_id,
        'body': comment_text
    }
    response = requests.post(GRAPHQL_ENDPOINT, headers=GRAPHQL_HEADERS, json={'query': mutation, 'variables': variables})
    response.raise_for_status()
    print(f"Comment added to issue {issue_id}")

def main():
    issues = fetch_closed_issues()
    for issue in issues:
        missing_fields = check_missing_fields(issue)
        if missing_fields:
            if not issue_has_existing_comment(issue, "The following required fields are missing:"):
                add_comment(issue['id'], missing_fields)

if __name__ == "__main__":
    main()
