-- Create database
CREATE DATABASE IF NOT EXISTS blind_sqli;
USE blind_sqli;

-- Create agents table
CREATE TABLE IF NOT EXISTS agents (
    id INT AUTO_INCREMENT PRIMARY KEY,
    codename VARCHAR(50) NOT NULL
);

-- Insert sample agents
INSERT INTO agents (codename) VALUES 
('EagleEye'),
('ShadowFox'),
('NightHawk'),
('PhantomWolf'),
('CyberGhost');

-- Create flags table (the target for extraction)
CREATE TABLE IF NOT EXISTS flags (
    id INT AUTO_INCREMENT PRIMARY KEY,
    flag_value VARCHAR(100) NOT NULL
);

-- Insert the flag that players need to extract
INSERT INTO flags (flag_value) VALUES ('ACNCTF{0u7_0f_b4nd_sql1_m4st3r}');

-- Grant FILE privileges to webapp user for OOB extraction
GRANT FILE ON *.* TO 'webapp'@'%';
FLUSH PRIVILEGES;

-- Create an admin table for additional challenge complexity
CREATE TABLE IF NOT EXISTS admin_users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(100) NOT NULL,
    secret_note TEXT
);

-- Insert admin data
INSERT INTO admin_users (username, password, secret_note) VALUES 
('admin', 'sup3r_s3cr3t_p4ss', 'The real treasure lies in the flags table'),
('operator', 'op3r4t0r_k3y', 'System maintenance access only');

-- Show tables for verification
SHOW TABLES;

-- Show sample data
SELECT 'Agents Table:' as Info;
SELECT * FROM agents;

SELECT 'Flags Table:' as Info;
SELECT * FROM flags;

SELECT 'Admin Users Table:' as Info;
SELECT username, secret_note FROM admin_users;
