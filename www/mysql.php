<?php
// Create connection
$conn = new mysqli('localhost', 'root', 'hpdb2019', 'hpdb');
// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

$sid = '28a6bd943a7da403a29d0466761c2b208d83bf3716a4db2afdb2442bdce498de';
$sql = "select * from sessions where sid='" . $sid . "'";
$result = $conn->query($sql);

if ($result->num_rows > 0) {
    $row = mysqli_fetch_assoc($result);
    echo "ID: " . $row["userid"] . " - Username: " . $row["username"];
} else {
    echo "0 results";
}
$conn->close();
?>