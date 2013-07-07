<?
class DeviceType {
	const PowerSwitch = 0;
	const Sensor = 1;
}

class NodeType {
	const PublicIP = 0;
	const Master = 1;
	const Slave = 2;
}

function db_connect() {
	$link = mysql_connect('localhost', 'ceng499', 'ceng499');
	if(!$link) {
		die('Could not connect: ' . mysql_error());
	}
	
	$db_selected = mysql_select_db('pihome', $link);
	if(!$db_selected) {
		die ('Can\'t use pihome: ' . mysql_error());
	}
}

function db_query($query) {
	$result = mysql_query($query);
	
	if(!$result) {
		$message  = 'Invalid query: ' . mysql_error() . "\n";
		$message .= 'Whole query: ' . $query;
		die($message);
	}
	
	return $result;
}

function getCamIPPort($name) {
	$name = mysql_real_escape_string($name);
	$result = db_query("SELECT ipaddress, mjpgport FROM Nodes WHERE name = " . "'$name'");
	$row = mysql_fetch_row($result);
	return $row;
}

function getCamNamesResult() {
	return db_query("SELECT name FROM Nodes WHERE mjpgport IS NOT NULL");
}

function getDevicesResult() {
	return db_query("SELECT * FROM Devices");
}

function addDevice($dserial, $dtype, $dname) {
	$query = sprintf("INSERT INTO Devices VALUES(%s, %s, '%s', 0, 0)",
		mysql_real_escape_string($dserial),
		mysql_real_escape_string($dtype),
		mysql_real_escape_string($dname)
	);
	
	db_query($query);
}
?>