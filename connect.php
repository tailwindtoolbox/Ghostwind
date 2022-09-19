<?php
$email = $_POST['email'];

$conn = new mysqli('localhost','root','','test');
if($conn->connect_error){
    die('Connection Faild : '.$conn->connect_error);
}else{
    $stmt =  $conn0->prepaare("insert into registration(email)
    values(?)");
    $stmt->bind_param("sssssi",$email);
    $stmt->execute();
    echo "regristration succesfully...";
    $stmt->close();
    $conn->close();
}
?>