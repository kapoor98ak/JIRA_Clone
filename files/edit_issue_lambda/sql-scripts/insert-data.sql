-- Database to use
USE JIRA;

-- Sample Data Insertion in User Table
INSERT INTO User (name, email) VALUES
('Abhishek Kapoor', 'kapoor98.ak@gmail.com'),
('Abhishek Latawa', 'kapoor28204@gmail.com'),
('Yash Walia', 'kapoor98.ak2@gmail.com');

-- Sample Data Insertion in the Issue Table
INSERT INTO Issue (assignee, assigner, status, date, title) VALUES
('kapoor98.ak@gmail.com', 'kapoor98.ak@gmail.com', 'In Progress', '2024-04-03', 'Fix bug on homepage'),
('kapoor28204@gmail.com', 'kapoor98.ak@gmail.com', 'Open', '2024-04-01', 'Implement new feature'),
('kapoor98.ak2@gmail.com', 'kapoor98.ak@gmail.com', 'Open', '2024-04-02', 'Update documentation');

