-- Database to use
USE JIRA;

-- Sample Data Insertion in User Table
INSERT INTO User (name, email) VALUES
('John Doe', 'john@example.com'),
('Jane Smith', 'jane@example.com'),
('Bob Johnson', 'bob@example.com');

-- Sample Data Insertion in the Issue Table
INSERT INTO Issue (assignee, assigner, status, date, title) VALUES
('john@example.com', 'john@example.com', 'In Progress', '2024-04-03', 'Fix bug on homepage'),
('jane@example.com', 'john@example.com', 'Open', '2024-04-01', 'Implement new feature'),
('jane@example.com', 'john@example.com', 'Open', '2024-04-02', 'Update documentation');

