<?php
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $url = $_POST['url'];
    $command = escapeshellcmd("python3 check.py " . escapeshellarg($url));
    shell_exec($command);
    header("Location: index.html?result=1");
    exit();
}
?>
