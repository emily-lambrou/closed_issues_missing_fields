# Missing required information for the project when it is closed

GitHub doesn't provide a built-in way to send notifications if the fields of the project are missing after it is closed. This
GitHub Action aims to address this by allowing you to identify the missing information within a central GitHub project.

## Introduction

This GitHub Action allows you to identify missing fields in a central GitHub project on closed issues. If at least one of the fields are missing,
then the assignees of the issue will be informed via comment to fill all the required fields for the project. 


### Prerequisites

Before you can start using this GitHub Action, you'll need to ensure you have the following:

1. A GitHub repository where you want to enable this action.
2. A GitHub project board with custom "Status" field, "Due Date", "Time Spent", "Release", "Estimate", "Priority", "Size", and "Week" added.
3. Status field, Release field, Priority field and Size fields should be "Single select" types, "Due Date" field should be "Date" type, "Time Spent" and "Estimate" should be "Text" type
   and "Week" should be "Iteration" type.
5. A Token (Classic) with permissions to repo:*, read:user, user:email, read:project

### Inputs

| Input                                | Description                                                                                      |
|--------------------------------------|--------------------------------------------------------------------------------------------------|
| `gh_token`                           | The GitHub Token                                                                                 |
| `project_number`                     | The project number                                                                               |                                                          
| `status_field_name` _(optional)_     | The status field name. The default is `Status`                                                   |
| `due_date_field_name` _(optional)_   | The due date field name. The default is `Due Date`                                               |
| `timespent_field_name` _(optional)_  | The time spent field name. The default is `Time Spent`                                           |
| `release_field_name` _(optional)_    | The release field name. The default is `Release`                                                 |
| `estimate_field_name` _(optional)_   | The estimate field name. The default is `Estimate`                                               |
| `priority_field_name` _(optional)_   | The priority field name. The default is `Priority`                                               |
| `size_field_name` _(optional)_       | The size field name. The default is `Size`                                                       |
| `week_field_name` _(optional)_       | The week field name. The default is `Week`                                                       |
| `notification_type` _(optional)_     | The notification type. Default is `comment`                                                      |
| `enterprise_github` _(optional)_     | `True` if you are using enterprise github and false if not. Default is `False`                   |
| `repository_owner_type` _(optional)_ | The type of the repository owner (oragnization or user). Default is `user`                       |
| `dry_run` _(optional)_               | `True` if you want to enable dry-run mode. Default is `False`                                    |


### Examples

#### Notify for missing fields with comment
To set up missing fields comment notifications, you'll need to create or update a GitHub Actions workflow in your repository. Below is
an example of a workflow YAML file:

```yaml
name: Notify for missing fields

# Runs every minute
on:
  schedule:
    - cron: '* * * * *'
  workflow_dispatch:

jobs:
  notify_for_missing_fields:
    runs-on: self-hosted

    steps:
      # Checkout the code to be used by runner
      - name: Checkout code
        uses: actions/checkout@v3


      # Check for missing fields
      - name: Check for missing fields
        uses: emily-lambrou/closed_issues_without_required_info@v1.3
        with:
          dry_run: ${{ vars.DRY_RUN }}           
          gh_token: ${{ secrets.GH_TOKEN }}      
          project_number: ${{ vars.PROJECT_NUMBER }} 
          enterprise_github: 'True'
          repository_owner_type: organization
        
```

