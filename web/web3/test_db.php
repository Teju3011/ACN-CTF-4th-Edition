<?php
// Simple database connection test
$db_host = 'localhost';
$db_username = 'webapp';
$db_password = 'webapp123';
$db_name = 'blind_sqli';

echo "<h1>Database Connection Test</h1>";

// Create connection
$conn = new mysqli($db_host, $db_username, $db_password, $db_name);

// Check connection
if ($conn->connect_error) {
    echo "<p style='color: red;'>Connection failed: " . $conn->connect_error . "</p>";
} else {
    echo "<p style='color: green;'>Connected successfully to database: $db_name</p>";
    
    // Test query
    $result = $conn->query("SELECT COUNT(*) as count FROM agents");
    if ($result) {
        $row = $result->fetch_assoc();
        echo "<p>Agents table has " . $row['count'] . " records</p>";
    }
    
    // Test flag table
    $result = $conn->query("SELECT COUNT(*) as count FROM flags");
    if ($result) {
        $row = $result->fetch_assoc();
        echo "<p>Flags table has " . $row['count'] . " records</p>";
    }
}

$conn->close();
?>
