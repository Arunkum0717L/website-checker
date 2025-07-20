<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Website Checker</title>
    <link rel="stylesheet" href="static/style.css">
</head>
<body>
    <div class="container">
        <h1>Website Safety Checker</h1>
        <form action="check.php" method="post">
            <input type="text" name="url" placeholder="Enter website URL" required>
            <button type="submit">Check</button>
        </form>

        <?php if (isset($_GET['result'])): ?>
        <div class="results">
            <h2>Analysis Result</h2>
            <?php
                $result = json_decode(file_get_contents("results/output.json"), true);
                echo "<p><strong>URL:</strong> " . $result['url'] . "</p>";
                echo "<p><strong>Status:</strong> " . $result['status'] . "</p>";
                echo "<ul>";
                foreach ($result['reasons'] as $reason) {
                    echo "<li>" . htmlspecialchars($reason) . "</li>";
                }
                echo "</ul>";
            ?>
        </div>
        <?php endif; ?>
    </div>
</body>
</html>




