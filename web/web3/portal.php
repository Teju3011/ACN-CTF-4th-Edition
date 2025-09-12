<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Agent Verification Portal</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <h1>🔒 Agent Verification Portal</h1>
        
        <div class="story-text">
            <p>Welcome to the classified recruitment system.</p>
            <p>Please enter your Agent ID for verification.</p>
        </div>
        
        <div class="form-section">
            <form method="POST" action="check.php">
                <div class="form-group">
                    <label for="agent_id">Agent ID:</label>
                    <input type="text" id="agent_id" name="id" placeholder="Enter your Agent ID" required>
                </div>
                <button type="submit" class="submit-btn">Verify Access</button>
            </form>
        </div>
        
        <div class="back-link">
            <a href="index.php">← Back to Main Portal</a>
        </div>
    </div>
</body>
</html>
