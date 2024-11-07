import graphql
import config
from logger import logger

# List of essential fields we want to check for
ESSENTIAL_FIELDS = [
    "Status", "Due Date", "Time Spent", "Release",
    "Estimate", "Priority", "Size", "Week"
]

# Fields we need to ignore (marked as "OLD" or "DO NOT SET")
IGNORE_FIELDS = [
    "Time Spend OLD(DO NOT SET)", 
    "Estimate OLD(DO NOT SET)"
]

def prepare_missing_fields_comment(issue: dict, assignees: dict):
    """
    Prepare a comment for an issue with missing required fields and return it.
    Only consider essential fields, and ignore fields marked as old, such as
    "Time Spend OLD(DO NOT SET)" and "Estimate OLD(DO NOT SET)".
    """
    # Collect any missing essential fields, ignoring "OLD" fields
    missing_fields = [
        field for field in ESSENTIAL_FIELDS
        if field not in issue or not issue[field]
    ]
    
    # Exclude any "OLD" or "DO NOT SET" fields explicitly
    filtered_missing_fields = [field for field in missing_fields if field not in IGNORE_FIELDS]

    # If no essential fields are missing, do not generate a comment
    if not filtered_missing_fields:
        logger.info(f'Issue #{issue["number"]} has no missing essential fields.')
        return None
    
    # Prepare the comment string
    comment = ''
    if assignees:
        for assignee in assignees:
            comment += f'@{assignee["login"]} '
    else:
        logger.info(f'No assignees found for issue #{issue["number"]}')
    
    # Append message about missing fields
    missing_fields_str = ', '.join(filtered_missing_fields)
    comment += f'Kindly set the missing required fields for the project: {missing_fields_str}.'
    logger.info(f'Issue {issue["title"]} | {comment}')
    
    return comment

def check_comment_exists(issue_id, comment_text):
    """Check if the comment already exists on the issue."""
    comments = graphql.get_issue_comments(issue_id)
    for comment in comments:
        if comment_text in comment.get('body', ''):
            return True
    return False
