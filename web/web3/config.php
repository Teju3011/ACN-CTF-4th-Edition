<?php
// Database configuration for Docker
$db_host = $_ENV['DB_HOST'] ?? 'mysql';
$db_username = $_ENV['DB_USER'] ?? 'webapp';
$db_password = $_ENV['DB_PASS'] ?? 'webapp123';
$db_name = $_ENV['DB_NAME'] ?? 'blind_sqli';

// Create connection (for auth_socket, we need to connect as the web server user)
$conn = new mysqli($db_host, $db_username, $db_password, $db_name);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Set charset to prevent encoding issues
$conn->set_charset("utf8");
?>
