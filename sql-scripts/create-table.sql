-- Database
USE JIRA;

DROP TABLE IF EXISTS Issue_History;
DROP TABLE IF EXISTS Issue;
DROP TABLE IF EXISTS User;

-- Create User table
CREATE TABLE IF NOT EXISTS User (
    name VARCHAR(255),
    email VARCHAR(255) PRIMARY KEY
);

-- Create Issue table
CREATE TABLE IF NOT EXISTS Issue (
    issue_id INT PRIMARY KEY AUTO_INCREMENT,
    assignee VARCHAR(50),
    assigner VARCHAR(50),
    status  ENUM('Open', 'Closed', 'Done', 'In Progress'),
    date DATE,
    title VARCHAR(255),
    FOREIGN KEY (assignee) REFERENCES User(email),
    FOREIGN KEY (assigner) REFERENCES User(email)
);

-- Create Issue_History table
CREATE TABLE IF NOT EXISTS Issue_History (
    change_id INT PRIMARY KEY AUTO_INCREMENT,
    issue_id INT,
    assignee VARCHAR(50),
    assigner VARCHAR(50),
    status VARCHAR(50),
    date DATE,
    title VARCHAR(255),
    change_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (issue_id) REFERENCES Issue(issue_id),
    FOREIGN KEY (assignee) REFERENCES User(email),
    FOREIGN KEY (assigner) REFERENCES User(email)
);
