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

function getNodes() {
	return db_query("SELECT nodename,ipaddress FROM Nodes");
}

function removeDevice($dserial, $dname) {
	$query = sprintf("DELETE FROM Devices WHERE serial=%s AND name='%s'",
		mysql_real_escape_string($dserial),
		mysql_real_escape_string($dname)
	);
	
	db_query($query);
}

function toggleDeviceActive($dserial, $dname, $dactive) {
	$query = sprintf("UPDATE Devices SET active=%s WHERE serial=%s AND name='%s'",
		mysql_real_escape_string($dactive),
		mysql_real_escape_string($dserial),
		mysql_real_escape_string($dname)
	);
	
	db_query($query);
}

function changeEmail($newemail, $oldemail) {
	# Change device name in Devices table
	$query = sprintf("UPDATE Emails SET email='%s' WHERE email='%s'",
		mysql_real_escape_string($newemail),
		mysql_real_escape_string($oldemail)
	);
	
	db_query($query);
}

function changeDeviceName($dserial, $dname) {
	# Change device name in Devices table
	$query = sprintf("UPDATE Devices SET name='%s' WHERE serial=%s",
		mysql_real_escape_string($dname),
		mysql_real_escape_string($dserial)
	);
	
	db_query($query);
}

function changeNodeName($dname, $dnewname) {
	# Change Node name in Nodes table
	$query = sprintf("UPDATE Nodes SET nodename='%s' WHERE nodename='%s'",
		mysql_real_escape_string($dnewname),
		mysql_real_escape_string($dname)
	);
	
	db_query($query);

	# Change Node name in Playbacks table
	$query = sprintf("UPDATE Playbacks SET nodename='%s' WHERE nodename='%s'",
		mysql_real_escape_string($dnewname),
		mysql_real_escape_string($dname)
	);
	
	db_query($query);
}

function removeNode($nodename, $nodeaddress) {
	$query = sprintf("DELETE FROM Nodes WHERE nodename='%s' AND ipaddress='%s'",
		mysql_real_escape_string($nodename),
		mysql_real_escape_string($nodeaddress)
	);
	
	db_query($query);
}

function removePlayback($nodename, $playbackfolder) {
	$query = sprintf("DELETE FROM Playbacks WHERE nodename='%s' AND recordfolder='%s'",
		mysql_real_escape_string($nodename),
		mysql_real_escape_string($playbackfolder)
	);
	
	db_query($query);
}

function removeEmail($email) {
	$query = sprintf("DELETE FROM Emails WHERE email='%s'",
		mysql_real_escape_string($email)
	);
	
	db_query($query);
}

function getEmails() {
	return db_query("SELECT email FROM Emails");
}

function getCamPlaybacksResult() {
	return db_query("SELECT nodename, recordfolder FROM Playbacks");
}

function getDevicesResult() {
	return db_query("SELECT lpad(hex(serial),16,'0') as Serial, type as Type, name as Name, status as Status, message as Message, active as Active FROM Devices");
}

# Test function to add fake playbacks
function addPlayback($nodename, $playbackfolder) {
	$query = sprintf("INSERT INTO Playbacks VALUES('%s','%s')",
		mysql_real_escape_string($nodename),
		mysql_real_escape_string($playbackfolder)
	);
	
	db_query($query);
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
	$message = $command. '/pi/' . $param;
	
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
	
	$msg .= '/pi/' . $dserial;
	
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
