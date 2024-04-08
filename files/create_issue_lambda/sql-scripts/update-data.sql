-- Select the Database to use
SELECT TABLE_NAME
FROM information_schema.tables
WHERE TABLE_SCHEMA = 'JIRA' AND TABLE_TYPE = 'BASE TABLE';


# -- Update Query
# USE JIRA
# UPDATE Issue
# SET assignee = 'bob@example.com', status = 'Closed'
# WHERE issue_id = 8
