<?php
require_once 'config.php';

$message = '';
$message_type = '';

if ($_POST && isset($_POST['id'])) {
    $id = $_POST['id'];
    
    // VULNERABLE SQL QUERY - Still injectable but no feedback
    $query = "SELECT * FROM agents WHERE id='$id'";
    
    // Execute query but suppress all feedback
    mysqli_report(MYSQLI_REPORT_OFF); // Disable error reporting
    @$conn->query($query); // Execute but ignore results/errors
    
    // ALWAYS return the same neutral response
    // This breaks boolean-based and error-based blind SQLi
    $message = "Request processed. System administrator will review your credentials.";
    $message_type = "neutral";
    
    // NO timing delays - breaks time-based blind SQLi
    
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
        <h1>🔍 Request Submitted</h1>
        
        <?php if ($message): ?>
            <div class="message <?php echo $message_type; ?>">
                <?php echo htmlspecialchars($message); ?>
            </div>
        <?php endif; ?>
        
        <div class="story-text">
            <p>Your verification request has been logged.</p>
            <p>Due to enhanced security protocols, no immediate feedback is provided.</p>
            <p>Please wait for manual review by our security team.</p>
        </div>
        
        <div class="back-link">
            <a href="portal.php">← Submit Another Request</a>
        </div>
        
        <div class="back-link">
            <a href="index.php">← Back to Main Portal</a>
        </div>
    </div>
</body>
</html>
