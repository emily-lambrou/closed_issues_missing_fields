from pprint import pprint
import requests
import logging
import config
import utils

def query_graphql(query, variables):
    try:
        response = requests.post(
            config.api_endpoint,
            json={"query": query, "variables": variables},
            headers={"Authorization": f"Bearer {config.gh_token}"}
        )
        response.raise_for_status()
        data = response.json()
        if 'errors' in data:
            logging.error(f"GraphQL query errors: {data['errors']}")
            return None
        return data.get('data')
    except requests.RequestException as e:
        logging.error(f"Request error: {e}")
        return None

def fetch_issues(owner, owner_type, project_number, field_name, field_type, filters=None, after=None, issues=None):
    query = f"""
    query GetProjectIssues($owner: String!, $projectNumber: Int!, $field: String!, $after: String) {{
          {owner_type}(login: $owner) {{
            projectV2(number: $projectNumber) {{
              id
              title
              number
              items(first: 100, after: $after) {{
                nodes {{
                  id
                  fieldValueByName(name: $field) {{
                    ... on {field_type} {{
                      id
                      name
                    }}
                  }}
                  content {{
                    ... on Issue {{
                      id
                      title
                      number
                      state
                      url
                      assignees(first: 20) {{
                        nodes {{
                          name
                          email
                          login
                        }}
                      }}
                    }}
                  }}
                }}
                pageInfo {{
                  endCursor
                  hasNextPage
                  hasPreviousPage
                }}
                totalCount
              }}
            }}
          }}
        }}
    """

    variables = {
        'owner': owner,
        'projectNumber': project_number,
        'field': field_name,
        'after': after
    }

    data = query_graphql(query, variables)
    if not data:
        return []

    owner_data = data.get(owner_type, {})
    project_data = owner_data.get('projectV2', {})
    items_data = project_data.get('items', {})
    pageinfo = items_data.get('pageInfo', {})
    nodes = items_data.get('nodes', [])

    if issues is None:
        issues = []

    if filters:
        filtered_issues = []
        for node in nodes:
            if filters.get('closed_only') and node['content'].get('state') != 'CLOSED':
                continue
            if filters.get(f'empty_{field_name.lower()}') and node['fieldValueByName']:
                continue
            filtered_issues.append(node)
        nodes = filtered_issues

    issues += nodes

    if pageinfo.get('hasNextPage'):
        return fetch_issues(
            owner=owner,
            owner_type=owner_type,
            project_number=project_number,
            field_name=field_name,
            field_type=field_type,
            filters=filters,
            after=pageinfo.get('endCursor'),
            issues=issues
        )

    return issues

def get_project_issues_status(owner, owner_type, project_number, status_field_name, filters=None, after=None, issues=None):
    return fetch_issues(owner, owner_type, project_number, status_field_name, 'ProjectV2ItemFieldSingleSelectValue', filters, after, issues)

def get_project_issues_duedate(owner, owner_type, project_number, duedate_field_name, filters=None, after=None, issues=None):
    return fetch_issues(owner, owner_type, project_number, duedate_field_name, 'ProjectV2ItemFieldDateValue', filters, after, issues)

def get_project_issues_timespent(owner, owner_type, project_number, timespent_field_name, filters=None, after=None, issues=None):
    return fetch_issues(owner, owner_type, project_number, timespent_field_name, 'ProjectV2ItemFieldTextValue', filters, after, issues)

def get_project_issues_release(owner, owner_type, project_number, release_field_name, filters=None, after=None, issues=None):
    return fetch_issues(owner, owner_type, project_number, release_field_name, 'ProjectV2ItemFieldSingleSelectValue', filters, after, issues)

def get_project_issues_estimate(owner, owner_type, project_number, estimate_field_name, filters=None, after=None, issues=None):
    return fetch_issues(owner, owner_type, project_number, estimate_field_name, 'ProjectV2ItemFieldTextValue', filters, after, issues)

def get_project_issues_priority(owner, owner_type, project_number, priority_field_name, filters=None, after=None, issues=None):
    return fetch_issues(owner, owner_type, project_number, priority_field_name, 'ProjectV2ItemFieldSingleSelectValue', filters, after, issues)

def get_project_issues_size(owner, owner_type, project_number, size_field_name, filters=None, after=None, issues=None):
    return fetch_issues(owner, owner_type, project_number, size_field_name, 'ProjectV2ItemFieldSingleSelectValue', filters, after, issues)

def get_project_issues_week(owner, owner_type, project_number, week_field_name, filters=None, after=None, issues=None):
    return fetch_issues(owner, owner_type, project_number, week_field_name, 'ProjectV2ItemFieldIterationValue', filters, after, issues)

def add_issue_comment(issueId, comment):
    mutation = """
    mutation AddIssueComment($issueId: ID!, $comment: String!) {
        addComment(input: {subjectId: $issueId, body: $comment}) {
            clientMutationId
        }
    }
    """

    variables = {
        'issueId': issueId,
        'comment': comment
    }

    try:
        response = requests.post(
            config.api_endpoint,
            json={"query": mutation, "variables": variables},
            headers={"Authorization": f"Bearer {config.gh_token}"}
        )
        data = response.json()

        if 'errors' in data:
            logging.error(f"GraphQL mutation errors: {data['errors']}")

        return data.get('data')

    except requests.RequestException as e:
        logging.error(f"Request error: {e}")
        return {}

def get_issue_comments(issue_id):
    query = """
    query GetIssueComments($issueId: ID!) {
        node(id: $issueId) {
            ... on Issue {
                comments(first: 100) {
                    nodes {
                        body
                        createdAt
                        author {
                            login
                        }
                    }
                    pageInfo {
                        endCursor
                        hasNextPage
                    }
                }
            }
        }
    }
    """

    variables = {
        'issueId': issue_id
    }

    try:
        response = requests.post(
            config.api_endpoint,
            json={"query": query, "variables": variables},
            headers={"Authorization": f"Bearer {config.gh_token}"}
        )
        
        data = response.json()

        if 'errors' in data:
            logging.error(f"GraphQL query errors: {data['errors']}")
            return []

        comments_data = data.get('data', {}).get('node', {}).get('comments', {})
        comments = comments_data.get('nodes', [])

        # Handle pagination if there are more comments
        pageinfo = comments_data.get('pageInfo', {})
        if pageinfo.get('hasNextPage'):
            next_page_comments = get_issue_comments(issue_id, after=pageinfo.get('endCursor'))
            comments.extend(next_page_comments)

        return comments

    except requests.RequestException as e:
        logging.error(f"Request error: {e}")
        return []
