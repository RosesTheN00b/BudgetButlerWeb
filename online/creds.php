<?php

require __DIR__ . '/vendor/autoload.php';
function getPDO(){
	$config_array  = parse_ini_file('db.ini');
	return new PDO('mysql:dbname='.$config_array['db_name'].';host=localhost;charset=utf8mb4', $config_array['db_usr'], $config_array['db_pw']);
}


function getAuth(){
	$config_array  = parse_ini_file('db.ini');


	// $db = new \PDO('mysql:dbname=my-database;host=localhost;charset=utf8mb4', 'my-username', 'my-password');
	// or
	// $db = new \PDO('pgsql:dbname=my-database;host=localhost;port=5432', 'my-username', 'my-password');
	// or
	// $db = new \PDO('sqlite:../Databases/my-database.sqlite');

	// or

	 $db = new \Delight\Db\PdoDsn('mysql:dbname='.$config_array['db_name'].';host=localhost;charset=utf8mb4', $config_array['db_usr'], $config_array['db_pw']);
	// or
	// $db = new \Delight\Db\PdoDsn('pgsql:dbname=my-database;host=localhost;port=5432', 'my-username', 'my-password');
	// or
	// $db = new \Delight\Db\PdoDsn('sqlite:../Databases/my-database.sqlite');

	return new \Delight\Auth\Auth($db);
}


?>