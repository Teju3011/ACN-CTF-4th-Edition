<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>EduCard Pro - Digital Report Cards</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f0f8ff;
        }
        .container {
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #2c5aa0;
            text-align: center;
            margin-bottom: 30px;
        }
        .form-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
            color: #333;
        }
        input[type="text"], input[type="email"], input[type="number"], select {
            width: 100%;
            padding: 10px;
            border: 2px solid #ddd;
            border-radius: 5px;
            font-size: 16px;
            box-sizing: border-box;
        }
        input[type="number"] {
            width: 80px;
        }
        .grades-group {
            display: grid;
            grid-template-columns: 1fr 100px;
            gap: 15px;
            align-items: center;
        }
        .subject-row {
            display: contents;
        }
        button {
            background-color: #2c5aa0;
            color: white;
            padding: 12px 30px;
            border: none;
            border-radius: 5px;
            font-size: 16px;
            cursor: pointer;
            width: 100%;
            margin-top: 20px;
        }
        button:hover {
            background-color: #1e3d6f;
        }
        .academic-emoji {
            font-size: 2em;
            margin: 0 10px;
        }
        .banner {
            text-align: center;
            margin-bottom: 20px;
            color: #666;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>📚 EduCard Pro - Digital Report Cards 📚</h1>
        <div class="banner">
            <p><strong>Create Professional Digital Report Cards Instantly!</strong></p>
            <p>Generate beautiful PDF report cards for your students</p>
            <span class="academic-emoji">�</span>
            <span class="academic-emoji">�</span>
            <span class="academic-emoji">🏆</span>
            <span class="academic-emoji">�</span>
        </div>
        
        <form action="quote.php" method="GET">
            <div class="form-group">
                <label for="organisation">Student Name:</label>
                <input type="text" id="organisation" name="organisation" required 
                       placeholder="Enter student's full name">
            </div>
            
            <div class="form-group">
                <label for="email">School Email:</label>
                <input type="email" id="email" name="email" required 
                       placeholder="school@example.com">
            </div>
            
            <div class="form-group">
                <label>Subject Grades:</label>
                <div class="grades-group">
                    <div class="subject-row">
                        <label for="small">Mathematics:</label>
                        <input type="number" id="small" name="small" min="0" max="100" value="85" placeholder="Grade">
                    </div>
                    <div class="subject-row">
                        <label for="medium">Science:</label>
                        <input type="number" id="medium" name="medium" min="0" max="100" value="90" placeholder="Grade">
                    </div>
                    <div class="subject-row">
                        <label for="large">English:</label>
                        <input type="number" id="large" name="large" min="0" max="100" value="88" placeholder="Grade">
                    </div>
                </div>
            </div>
            
            <button type="submit">Generate Report Card 📄</button>
        </form>
    </div>
</body>
</html>
