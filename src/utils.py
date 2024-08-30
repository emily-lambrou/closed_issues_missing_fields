import smtplib
import html2text
import config

def prepare_missing_duedate_comment(issue: dict, assignees: dict):
    """
    Prepare the comment from the given arguments and return it
    """

    comment = ''
    if assignees:
        for assignee in assignees:
            comment += f'@{assignee["login"]} '
    else:
        logger.info(f'No assignees found for issue #{issue["number"]}')

    comment += f'Kindly set the `Due Date` for this issue.'
    logger.info(f'Issue {issue["title"]} | {comment}')

    return comment




