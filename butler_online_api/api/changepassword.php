<?php
require_once(__DIR__.'/util/creds.php');
require_once(__DIR__.'/model.php');

authenticated(function($auth){
	$dbh = getPDO();

	$jsondata = file_get_contents('php://input');
	$data = json_decode($jsondata, true);

	$oldPassword = strval($data['oldPassword']);
	$newPassword = strval($data['newPassword']);

	$auth->changePassword($oldPassword, $newPassword);
	$result = new Result();
	$result->message = "Passwort erfolgreich geändert";
	echo json_encode($result);
});
?>
