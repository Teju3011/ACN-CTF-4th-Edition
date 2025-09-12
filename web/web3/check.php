<?php
require_once 'config.php';

$message = '';
$message_type = '';

if ($_POST && isset($_POST['id'])) {
    $id = $_POST['id'];
    
    // VULNERABLE SQL QUERY - Direct concatenation without sanitization
    $query = "SELECT * FROM agents WHERE id='$id'";
    
    // Execute query
    $result = $conn->query($query);
    
    if ($result && $result->num_rows > 0) {
        $message = "Access Granted: Welcome Agent.";
        $message_type = "success";
    } else {
        $message = "Access Denied.";
        $message_type = "error";
    }
    
    // Add a small delay to make time-based blind SQLi possible
    usleep(100000); // 0.1 second delay
    
    $conn->close();
} else {
    header('Location: portal.php');
    exit();
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Verification Result</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <h1>🔍 Verification Result</h1>
        
        <?php if ($message): ?>
            <div class="message <?php echo $message_type; ?>">
                <?php echo htmlspecialchars($message); ?>
            </div>
        <?php endif; ?>
        
        <div class="back-link">
            <a href="portal.php">← Try Another Agent ID</a>
        </div>
        
        <div class="back-link">
            <a href="index.php">← Back to Main Portal</a>
        </div>
    </div>
</body>
</html>
