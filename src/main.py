from logger import logger
import requests
import config
import utils
import graphql

def notify_missing_status():
    issues = graphql.get_project_issues_status(
        owner=config.repository_owner,
        owner_type=config.repository_owner_type,
        project_number=config.project_number,
        status_field_name=config.status_field_name,
        filters={'empty_status': True, 'closed_only': True}
    )

    # Check if there are issues available
    if not issues:
        logger.info('No issues has been found')
        return

     # Loop through issues
    for issue in issues:
        # Skip the issues if they are opened
        if issue.get('state') == 'OPEN':
            continue

        # Ensure 'content' is present
        issue_content = issue.get('content', {})
        if not issue_content:
            logger.warning(f'Issue object does not contain "content": {issue}')
            continue
            
         # Ensure 'id' is present in issue content
        issue_id = issue_content.get('id')
        if not issue_id:
            logger.warning(f'Issue content does not contain "id": {issue_content}')
            continue

        # Get the project item from issue
        project_items = issue.get('projectItems', {}).get('nodes', [])
        if not project_items:
            logger.warning(f'No project items found for issue {issue_id}')
            continue

        comment_text = f"Kindly set the missing required fields for the project: Status, Due Date, Time Spent, Release, Estimate, Priority, Size, Week."
        
        # Check if the comment already exists
        if not utils.check_comment_exists(issue_id, comment_text):
            if config.notification_type == 'comment':
                # Prepare the notification content
                comment = utils.prepare_missing_fields_comment(
                    issue=issue_content,
                    assignees=issue_content.get('assignees', {}).get('nodes', []), 
                )
    
                if not config.dry_run:
                    # Add the comment to the issue
                    graphql.add_issue_comment(issue_id, comment)
    
                logger.info(f'Comment added to issue #{issue_content.get("number")} ({issue_id})')
                
def notify_missing_duedate():
    issues = graphql.get_project_issues_duedate(
        owner=config.repository_owner,
        owner_type=config.repository_owner_type,
        project_number=config.project_number,
        duedate_field_name=config.duedate_field_name,
        filters={'empty_duedate': True, 'closed_only': True}
    )

    # Check if there are issues available
    if not issues:
        logger.info('No issues has been found')
        return

    # Loop through issues
    for issue in issues:
        # Skip the issues if they are opened
        if issue.get('state') == 'OPEN':
            continue

        # Ensure 'content' is present
        issue_content = issue.get('content', {})
        if not issue_content:
            logger.warning(f'Issue object does not contain "content": {issue}')
            continue
            
         # Ensure 'id' is present in issue content
        issue_id = issue_content.get('id')
        if not issue_id:
            logger.warning(f'Issue content does not contain "id": {issue_content}')
            continue

        # Get the project item from issue
        project_items = issue.get('projectItems', {}).get('nodes', [])
        if not project_items:
            logger.warning(f'No project items found for issue {issue_id}')
            continue

        comment_text = f"Kindly set the missing required fields for the project: Status, Due Date, Time Spent, Release, Estimate, Priority, Size, Week."
        
        # Check if the comment already exists
        if not utils.check_comment_exists(issue_id, comment_text):

            if config.notification_type == 'comment':
                # Prepare the notification content
                comment = utils.prepare_missing_fields_comment(
                    issue=issue_content,
                    assignees=issue_content.get('assignees', {}).get('nodes', []), 
                )
    
                if not config.dry_run:
                    # Add the comment to the issue
                    graphql.add_issue_comment(issue['id'], comment)
    
                logger.info(f'Comment added to issue #{issue["number"]} ({issue["id"]})')


def notify_missing_timespent():
    issues = graphql.get_project_issues_timespent(
        owner=config.repository_owner,
        owner_type=config.repository_owner_type,
        project_number=config.project_number,
        timespent_field_name=config.timespent_field_name,
        filters={'empty_timespent': True, 'closed_only': True}
    )

    # Check if there are issues available
    if not issues:
        logger.info('No issues has been found')
        return

    # Loop through issues
    for issue in issues:
        # Skip the issues if they are opened
        if issue.get('state') == 'OPEN':
            continue

        # Ensure 'content' is present
        issue_content = issue.get('content', {})
        if not issue_content:
            logger.warning(f'Issue object does not contain "content": {issue}')
            continue
            
         # Ensure 'id' is present in issue content
        issue_id = issue_content.get('id')
        if not issue_id:
            logger.warning(f'Issue content does not contain "id": {issue_content}')
            continue

        # Get the project item from issue
        project_items = issue.get('projectItems', {}).get('nodes', [])
        if not project_items:
            logger.warning(f'No project items found for issue {issue_id}')
            continue

        comment_text = f"Kindly set the missing required fields for the project: Status, Due Date, Time Spent, Release, Estimate, Priority, Size, Week."
        
        # Check if the comment already exists
        if not utils.check_comment_exists(issue_id, comment_text):   
            if config.notification_type == 'comment':
                # Prepare the notification content
                comment = utils.prepare_missing_fields_comment(
                    issue=issue_content,
                    assignees=issue_content.get('assignees', {}).get('nodes', []), 
                )
    
                if not config.dry_run:
                    # Add the comment to the issue
                    graphql.add_issue_comment(issue['id'], comment)
    
                logger.info(f'Comment added to issue #{issue["number"]} ({issue["id"]})')
          
def notify_missing_release():
    issues = graphql.get_project_issues_release(
        owner=config.repository_owner,
        owner_type=config.repository_owner_type,
        project_number=config.project_number,
        release_field_name=config.release_field_name,
        filters={'empty_release': True, 'closed_only': True}
    )

    # Check if there are issues available
    if not issues:
        logger.info('No issues has been found')
        return

    # Loop through issues
    for issue in issues:
        # Skip the issues if they are opened
        if issue.get('state') == 'OPEN':
            continue

        # Ensure 'content' is present
        issue_content = issue.get('content', {})
        if not issue_content:
            logger.warning(f'Issue object does not contain "content": {issue}')
            continue
            
         # Ensure 'id' is present in issue content
        issue_id = issue_content.get('id')
        if not issue_id:
            logger.warning(f'Issue content does not contain "id": {issue_content}')
            continue

        # Get the project item from issue
        project_items = issue.get('projectItems', {}).get('nodes', [])
        if not project_items:
            logger.warning(f'No project items found for issue {issue_id}')
            continue

        comment_text = f"Kindly set the missing required fields for the project: Status, Due Date, Time Spent, Release, Estimate, Priority, Size, Week."
        
        # Check if the comment already exists
        if not utils.check_comment_exists(issue_id, comment_text):   
            if config.notification_type == 'comment':
                # Prepare the notification content
                comment = utils.prepare_missing_fields_comment(
                    issue=issue_content,
                    assignees=issue_content.get('assignees', {}).get('nodes', []), 
                )
    
                if not config.dry_run:
                    # Add the comment to the issue
                    graphql.add_issue_comment(issue['id'], comment)
    
                logger.info(f'Comment added to issue #{issue["number"]} ({issue["id"]})')
          
      
def notify_missing_estimate():
    issues = graphql.get_project_issues_estimate(
        owner=config.repository_owner,
        owner_type=config.repository_owner_type,
        project_number=config.project_number,
        estimate_field_name=config.estimate_field_name,
        filters={'empty_estimate': True, 'closed_only': True}
    )

    # Check if there are issues available
    if not issues:
        logger.info('No issues has been found')
        return

    # Loop through issues
    for issue in issues:
        # Skip the issues if they are opened
        if issue.get('state') == 'OPEN':
            continue

        # Ensure 'content' is present
        issue_content = issue.get('content', {})
        if not issue_content:
            logger.warning(f'Issue object does not contain "content": {issue}')
            continue
            
         # Ensure 'id' is present in issue content
        issue_id = issue_content.get('id')
        if not issue_id:
            logger.warning(f'Issue content does not contain "id": {issue_content}')
            continue

        # Get the project item from issue
        project_items = issue.get('projectItems', {}).get('nodes', [])
        if not project_items:
            logger.warning(f'No project items found for issue {issue_id}')
            continue

        comment_text = f"Kindly set the missing required fields for the project: Status, Due Date, Time Spent, Release, Estimate, Priority, Size, Week."
        
        # Check if the comment already exists
        if not utils.check_comment_exists(issue_id, comment_text):   
            if config.notification_type == 'comment':
                # Prepare the notification content
                comment = utils.prepare_missing_fields_comment(
                    issue=issue_content,
                    assignees=issue_content.get('assignees', {}).get('nodes', []), 
                )
    
                if not config.dry_run:
                    # Add the comment to the issue
                    graphql.add_issue_comment(issue['id'], comment)
    
                logger.info(f'Comment added to issue #{issue["number"]} ({issue["id"]})')
          
def notify_missing_priority():
    issues = graphql.get_project_issues_priority(
        owner=config.repository_owner,
        owner_type=config.repository_owner_type,
        project_number=config.project_number,
        priority_field_name=config.priority_field_name,
        filters={'empty_priority': True, 'closed_only': True}
    )

    # Check if there are issues available
    if not issues:
        logger.info('No issues has been found')
        return

    # Loop through issues
    for issue in issues:
        # Skip the issues if they are opened
        if issue.get('state') == 'OPEN':
            continue

        # Ensure 'content' is present
        issue_content = issue.get('content', {})
        if not issue_content:
            logger.warning(f'Issue object does not contain "content": {issue}')
            continue
            
         # Ensure 'id' is present in issue content
        issue_id = issue_content.get('id')
        if not issue_id:
            logger.warning(f'Issue content does not contain "id": {issue_content}')
            continue

        # Get the project item from issue
        project_items = issue.get('projectItems', {}).get('nodes', [])
        if not project_items:
            logger.warning(f'No project items found for issue {issue_id}')
            continue

        comment_text = f"Kindly set the missing required fields for the project: Status, Due Date, Time Spent, Release, Estimate, Priority, Size, Week."
        
        # Check if the comment already exists
        if not utils.check_comment_exists(issue_id, comment_text):   
            if config.notification_type == 'comment':
                # Prepare the notification content
                comment = utils.prepare_missing_fields_comment(
                    issue=issue_content,
                    assignees=issue_content.get('assignees', {}).get('nodes', []), 
                )
    
                if not config.dry_run:
                    # Add the comment to the issue
                    graphql.add_issue_comment(issue['id'], comment)
    
                logger.info(f'Comment added to issue #{issue["number"]} ({issue["id"]})')
          
      
def notify_missing_size():
    issues = graphql.get_project_issues_size(
        owner=config.repository_owner,
        owner_type=config.repository_owner_type,
        project_number=config.project_number,
        size_field_name=config.size_field_name,
        filters={'empty_size': True, 'closed_only': True}
    )

    # Check if there are issues available
    if not issues:
        logger.info('No issues has been found')
        return

    # Loop through issues
    for issue in issues:
        # Skip the issues if they are opened
        if issue.get('state') == 'OPEN':
            continue

        # Ensure 'content' is present
        issue_content = issue.get('content', {})
        if not issue_content:
            logger.warning(f'Issue object does not contain "content": {issue}')
            continue
            
         # Ensure 'id' is present in issue content
        issue_id = issue_content.get('id')
        if not issue_id:
            logger.warning(f'Issue content does not contain "id": {issue_content}')
            continue

        # Get the project item from issue
        project_items = issue.get('projectItems', {}).get('nodes', [])
        if not project_items:
            logger.warning(f'No project items found for issue {issue_id}')
            continue
        comment_text = f"Kindly set the missing required fields for the project: Status, Due Date, Time Spent, Release, Estimate, Priority, Size, Week."
        
        # Check if the comment already exists
        if not utils.check_comment_exists(issue_id, comment_text):   
            if config.notification_type == 'comment':
                # Prepare the notification content
                comment = utils.prepare_missing_fields_comment(
                    issue=issue_content,
                    assignees=issue_content.get('assignees', {}).get('nodes', []), 
                )
    
                if not config.dry_run:
                    # Add the comment to the issue
                    graphql.add_issue_comment(issue['id'], comment)
    
                logger.info(f'Comment added to issue #{issue["number"]} ({issue["id"]})')
          
      
def notify_missing_week():
    issues = graphql.get_project_issues_week(
        owner=config.repository_owner,
        owner_type=config.repository_owner_type,
        project_number=config.project_number,
        week_field_name=config.week_field_name,
        filters={'empty_week': True, 'closed_only': True}
    )

    # Check if there are issues available
    if not issues:
        logger.info('No issues has been found')
        return

    # Loop through issues
    for issue in issues:
        # Skip the issues if they are opened
        if issue.get('state') == 'OPEN':
            continue

        # Ensure 'content' is present
        issue_content = issue.get('content', {})
        if not issue_content:
            logger.warning(f'Issue object does not contain "content": {issue}')
            continue
            
         # Ensure 'id' is present in issue content
        issue_id = issue_content.get('id')
        if not issue_id:
            logger.warning(f'Issue content does not contain "id": {issue_content}')
            continue

        # Get the project item from issue
        project_items = issue.get('projectItems', {}).get('nodes', [])
        if not project_items:
            logger.warning(f'No project items found for issue {issue_id}')
            continue

        comment_text = f"Kindly set the missing required fields for the project: Status, Due Date, Time Spent, Release, Estimate, Priority, Size, Week."
        
        # Check if the comment already exists
        if not utils.check_comment_exists(issue_id, comment_text):   
            if config.notification_type == 'comment':
                # Prepare the notification content
                comment = utils.prepare_missing_fields_comment(
                    issue=issue_content,
                    assignees=issue_content.get('assignees', {}).get('nodes', []), 
                )
    
                if not config.dry_run:
                    # Add the comment to the issue
                    graphql.add_issue_comment(issue['id'], comment)
    
                logger.info(f'Comment added to issue #{issue["number"]} ({issue["id"]})')
          
def main():
    logger.info('Process started...')
    if config.dry_run:
        logger.info('DRY RUN MODE ON!')

    notify_missing_status()
    notify_missing_duedate()
    notify_missing_timespent()
    notify_missing_release()
    notify_missing_estimate()
    notify_missing_priority()
    notify_missing_size()
    notify_missing_week()
  

if __name__ == "__main__":
    main()
