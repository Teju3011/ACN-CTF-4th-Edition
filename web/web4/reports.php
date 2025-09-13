<?php
$error_message = '';
$file_content = '';
$current_file = '';
$available_reports = ['mission_001.txt', 'agent_status.txt', 'daily_briefing.txt'];

if (isset($_GET['file'])) {
    $file = $_GET['file'];
    $current_file = $file;
    
    // VULNERABLE: Direct file inclusion without proper validation
    // This allows path traversal attacks
    $base_path = '/var/www/html/reports/';
    $full_path = $base_path . $file;
    
    if (file_exists($full_path)) {
        $file_content = file_get_contents($full_path);
    } else {
        $error_message = "Report not found: " . htmlspecialchars($file);
    }
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mission Reports Archive</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <div class="header-section">
            <h1>📁 Mission Reports Archive</h1>
            <p>Access classified mission reports and operational documents</p>
            <a href="index.php" class="back-link">← Back to Portal</a>
        </div>

        <div class="reports-section">
            <div class="file-browser">
                <h3>Available Reports</h3>
                <div class="file-list">
                    <?php foreach ($available_reports as $report): ?>
                        <a href="?file=<?php echo urlencode($report); ?>" 
                           class="file-item <?php echo ($current_file === $report) ? 'active' : ''; ?>">
                            📄 <?php echo htmlspecialchars($report); ?>
                        </a>
                    <?php endforeach; ?>
                </div>
                
                <div class="manual-access">
                    <h4>Direct File Access</h4>
                    <!-- <p>For authorized personnel: Enter filename directly</p> -->
                    <form method="GET" class="file-form">
                        <input type="text" name="file" placeholder="Enter filename..." 
                               value="<?php echo htmlspecialchars($current_file); ?>" class="file-input">
                        <button type="submit" class="load-btn">Load Report</button>
                    </form>
                </div>
            </div>

            <div class="file-content">
                <?php if ($error_message): ?>
                    <div class="error-message">
                        <?php echo $error_message; ?>
                    </div>
                <?php elseif ($file_content): ?>
                    <div class="content-header">
                        <h3>📄 <?php echo htmlspecialchars($current_file); ?></h3>
                    </div>
                    <div class="content-body">
                        <pre><?php echo htmlspecialchars($file_content); ?></pre>
                    </div>
                <?php else: ?>
                    <div class="no-content">
                        <p>Select a report from the archive to view its contents.</p>
                        <p><em>Authorized personnel can access additional files directly by filename.</em></p>
                    </div>
                <?php endif; ?>
            </div>
        </div>
    </div>
</body>
</html>
