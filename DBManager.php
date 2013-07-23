<?
class DeviceType {
	const PowerSwitch = 0;
	const Sensor = 1;
}

class DeviceState {
	const Off = 0;
	const On = 1;
}

class NodeType {
	const PublicIP = 0;
	const Master = 1;
	const Slave = 2;
}

define('SCRIPT_IP', '142.104.165.35');
define('SCRIPT_PORT', 50000);

function db_connect() {
	$link = mysql_connect('localhost', 'ceng499', 'ceng499');
	if(!$link) {
		die('Could not connect: 50000' . mysql_error());
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

function getCamIP($name) {
	$name = mysql_real_escape_string($name);
	$result = db_query("SELECT ipaddress FROM Nodes WHERE nodename = " . "'$name'");
	$row = mysql_fetch_row($result);
	return $row;
}

function getCamNamesResult() {
	return db_query("SELECT nodename FROM Nodes");
}

function getCamPlaybacksResult() {
	return db_query("SELECT nodename, recordfolder FROM Playbacks");
}

function getDevicesResult() {
	return db_query("SELECT lpad(hex(serial),16,'0') as Serial, type as Type, name as Name, status as Status, message as Message, active as Active FROM Devices");
}

function addDevice($dserial, $dname) {
	$query = sprintf("INSERT INTO Devices VALUES(%s, 5, '%s', 0, 0,'New')",
		mysql_real_escape_string($dserial),
		mysql_real_escape_string($dname)
	);
	
	db_query($query);
}

function addNode($nodename, $nodeaddress) {
	$query = sprintf("INSERT INTO Nodes VALUES('%s','%s')",
		mysql_real_escape_string($nodename),
		mysql_real_escape_string($nodeaddress)
	);
	
	db_query($query);
}

# temporary
/*function setDeviceState($dserial, $state) {
	$query = sprintf("UPDATE Devices SET status=%s WHERE serial=%s",
		mysql_real_escape_string($state),
		mysql_real_escape_string($dserial)
	);
	
	db_query($query);
}*/

/*function setDeviceState($dserial, $state) {
	$non_num_pattern = "/[^0-9]/";
	if(preg_match($non_num_pattern, $dserial) || preg_match($non_num_pattern, $state)) {
		die('Invalid input');
	}
	exec(SENDER_PATH . ' ' . $dserial . ' ' . $state);
}*/

function sendCommandToPiHome($command, $param) {
	# Check for non-empty command and parameter
	if(strlen($command) == 0 or strlen($param) == 0) die('Command and Parameter are empty' . $command . $param);
	
	# Build command message consists of "command param"
	$message = $command. ' ' . $param;
	
	# Create one-time socket to local PiHome.py to send command to it
	$sock = socket_create(AF_INET, SOCK_STREAM, SOL_TCP);
	if(!$sock) die('Cannot create socket');
	
	if(!socket_connect($sock, SCRIPT_IP, SCRIPT_PORT)) {
		socket_close($sock);
		die('Cannot connect to PiHome.py ip and port');
	}
	
	# Send command through socket
	socket_send($sock, $message, strlen($message), 0);
	
	# Do not wait for socket response, close right away.
	# This may need to change if we want to wait for confirmation from PiHome.py
	socket_close($sock);
}

function setDeviceState($dserial, $state) {
	#$non_num_pattern = "/[^0-9A-Z]/";
	
	#if(preg_match($non_num_pattern, $dserial) || preg_match($non_num_pattern, $state)) {
	#	die('Non decimal character detected');
	#}
	
	$state = intval($state, 10);
	
	if($state == DeviceState::Off) $msg = 'off';
	else if($state == DeviceState::On) $msg = 'on';
	else die('Invalid state' . $state);
	
	$msg .= ' ' . $dserial;
	
	$sock = socket_create(AF_INET, SOCK_STREAM, SOL_TCP);
	if(!$sock) die('1');
	
	if(!socket_connect($sock, SCRIPT_IP, SCRIPT_PORT)) {
		socket_close($sock);
		die('2');
	}
	
	socket_send($sock, $msg, strlen($msg), 0);
	
	socket_close($sock);
}
?>
