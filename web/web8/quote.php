<?php
require_once 'vendor/autoload.php';

use Dompdf\Dompdf;
use Dompdf\Options;

// Validate inputs
function validateInput($input, $type) {
    switch($type) {
        case 'email':
            return filter_var($input, FILTER_VALIDATE_EMAIL);
        case 'number':
            return is_numeric($input) && $input >= 0 && $input <= 100;
        case 'text':
            return !empty($input) && strlen($input) <= 200;
        default:
            return false;
    }
}

// Get and validate parameters
$organisation = $_GET['organisation'] ?? '';
$email = $_GET['email'] ?? '';
$small = $_GET['small'] ?? 0;
$medium = $_GET['medium'] ?? 0;
$large = $_GET['large'] ?? 0;

// Basic validation
if (!validateInput($organisation, 'text')) {
    die('Invalid student name');
}
if (!validateInput($email, 'email')) {
    die('Invalid school email address');
}
if (!validateInput($small, 'number') || !validateInput($medium, 'number') || !validateInput($large, 'number')) {
    die('Invalid grades');
}

// Calculate grades and GPA
$mathGrade = $small;
$scienceGrade = $medium;
$englishGrade = $large;
$totalGrade = $mathGrade + $scienceGrade + $englishGrade;
$averageGrade = round($totalGrade / 3, 1);

// Determine grade letter
function getGradeLetter($grade) {
    if ($grade >= 90) return 'A';
    if ($grade >= 80) return 'B';
    if ($grade >= 70) return 'C';
    if ($grade >= 60) return 'D';
    return 'F';
}

// Create HTML for PDF
$html = "
<!DOCTYPE html>
<html>
<head>
    <meta charset='UTF-8'>
    <title>Student Report Card</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .header { text-align: center; color: #2c5aa0; margin-bottom: 30px; border-bottom: 3px solid #2c5aa0; padding-bottom: 20px; }
        .school-info { text-align: center; margin-bottom: 30px; color: #666; }
        .student-details { margin: 20px 0; }
        .grades-table { width: 100%; border-collapse: collapse; margin: 20px 0; }
        .grades-table th, .grades-table td { padding: 12px; border: 1px solid #ddd; text-align: center; }
        .grades-table th { background-color: #2c5aa0; color: white; }
        .summary { margin: 30px 0; padding: 20px; background-color: #f0f8ff; border-radius: 5px; }
        .footer { margin-top: 40px; font-size: 12px; color: #666; text-align: center; }
        .grade-a { color: #27ae60; font-weight: bold; }
        .grade-b { color: #3498db; font-weight: bold; }
        .grade-c { color: #f39c12; font-weight: bold; }
        .grade-d { color: #e67e22; font-weight: bold; }
        .grade-f { color: #e74c3c; font-weight: bold; }
    </style>
</head>
<body>
    <div class='header'>
        <h1>📚 ACADEMIC REPORT CARD 📚</h1>
    </div>
    
    <div class='school-info'>
        <h3>EduCard Pro Digital School System</h3>
        <p>Academic Excellence • Character Development • Future Leaders</p>
    </div>
    
    <div class='student-details'>
        <p><strong>Student Name:</strong> " . $organisation . "</p>
        <p><strong>School Contact:</strong> " . htmlspecialchars($email) . "</p>
        <p><strong>Report Date:</strong> " . date('Y-m-d H:i:s') . "</p>
        <p><strong>Academic Year:</strong> 2024-2025</p>
    </div>
    
    <table class='grades-table'>
        <thead>
            <tr>
                <th>Subject</th>
                <th>Grade (%)</th>
                <th>Letter Grade</th>
                <th>Performance</th>
            </tr>
        </thead>
        <tbody>";

if ($mathGrade > 0) {
    $letterGrade = getGradeLetter($mathGrade);
    $performance = $mathGrade >= 80 ? 'Excellent' : ($mathGrade >= 70 ? 'Good' : ($mathGrade >= 60 ? 'Satisfactory' : 'Needs Improvement'));
    $gradeClass = 'grade-' . strtolower($letterGrade);
    $html .= "<tr><td>Mathematics</td><td>{$mathGrade}%</td><td class='{$gradeClass}'>{$letterGrade}</td><td>{$performance}</td></tr>";
}
if ($scienceGrade > 0) {
    $letterGrade = getGradeLetter($scienceGrade);
    $performance = $scienceGrade >= 80 ? 'Excellent' : ($scienceGrade >= 70 ? 'Good' : ($scienceGrade >= 60 ? 'Satisfactory' : 'Needs Improvement'));
    $gradeClass = 'grade-' . strtolower($letterGrade);
    $html .= "<tr><td>Science</td><td>{$scienceGrade}%</td><td class='{$gradeClass}'>{$letterGrade}</td><td>{$performance}</td></tr>";
}
if ($englishGrade > 0) {
    $letterGrade = getGradeLetter($englishGrade);
    $performance = $englishGrade >= 80 ? 'Excellent' : ($englishGrade >= 70 ? 'Good' : ($englishGrade >= 60 ? 'Satisfactory' : 'Needs Improvement'));
    $gradeClass = 'grade-' . strtolower($letterGrade);
    $html .= "<tr><td>English</td><td>{$englishGrade}%</td><td class='{$gradeClass}'>{$letterGrade}</td><td>{$performance}</td></tr>";
}

$overallLetter = getGradeLetter($averageGrade);
$overallClass = 'grade-' . strtolower($overallLetter);

$html .= "
        </tbody>
    </table>
    
    <div class='summary'>
        <h3>Academic Summary</h3>
        <p><strong>Overall Average:</strong> <span class='{$overallClass}'>{$averageGrade}% ({$overallLetter})</span></p>
        <p><strong>Total Points:</strong> {$totalGrade}/300</p>
        <p><strong>Academic Standing:</strong> " . ($averageGrade >= 80 ? 'Honor Roll' : ($averageGrade >= 70 ? 'Good Standing' : 'Needs Academic Support')) . "</p>
    </div>
    
    <div class='footer'>
        <p>This report card is generated digitally by EduCard Pro</p>
        <p>For questions regarding this report, contact the school administration</p>
        <p>Generated on " . date('F j, Y \a\t g:i A') . "</p>
    </div>
</body>
</html>";

// Configure DomPDF
$options = new Options();
$options->set('defaultFont', 'Arial');
$options->set('isRemoteEnabled', true); // This is the vulnerable setting!
$options->set('isHtml5ParserEnabled', true);

$dompdf = new Dompdf($options);
$dompdf->loadHtml($html);
$dompdf->setPaper('A4', 'portrait');
$dompdf->render();

// Output PDF
$dompdf->stream('student_report_card.pdf', array('Attachment' => false));
?>
