-- Select the Database to use
USE JIRA;

-- Update Query
UPDATE Issue
SET assignee = 'bob@example.com', status = 'Closed'
WHERE issue_id = 8
