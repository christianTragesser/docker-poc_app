<body style='background-color:white'>
<?php
$IP = $_SERVER['SERVER_ADDR']; // Get IP
$NAME = php_uname('n');
echo nl2br("Server hostname is: <strong>$NAME</strong>\nServer LAN IP address is: <strong>$IP</strong>");
?>
