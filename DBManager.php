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


###################################### Camera node related functions
# Function to get a list of all nodes
function getNodes() {
	return db_query("SELECT nodename,ipaddress FROM Nodes");
}

# Function to get all node names from Nodes
function getCamNamesResult() {
	return db_query("SELECT nodename FROM Nodes");
}

# Function to get ipaddress of a node
function getCamIP($name) {
	$query = sprintf("SELECT ipaddress FROM Nodes WHERE nodename ='%s'",
		mysql_real_escape_string($name));
	$result = db_query($query);
	$row = mysql_fetch_row($result);
	return $row[0];
}

# Function to add new node to database
function addNode($nodename, $nodeaddress) {
	$query = sprintf("INSERT INTO Nodes VALUES('%s','%s')",
		mysql_real_escape_string($nodename),
		mysql_real_escape_string($nodeaddress)
	);
	
	db_query($query);
}

# Function to change camera node name
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

# Function to remove node
function removeNode($nodename, $nodeaddress) {
	# Remove Node from Nodes table
	$query = sprintf("DELETE FROM Nodes WHERE nodename='%s' AND ipaddress='%s'",
		mysql_real_escape_string($nodename),
		mysql_real_escape_string($nodeaddress)
	);
	
	db_query($query);
}

################################### Device related functions
# Function to get list of devices
function getDevicesResult() {
	return db_query("SELECT lpad(hex(serial),16,'0') as Serial, type as Type, name as Name, status as Status, message as Message, active as Active FROM Devices");
}

# Function to add new device to database
function addDevice($dserial, $dname) {
	$query = sprintf("INSERT INTO Devices VALUES(%s, 5, '%s', 0, 0,'New')",
		mysql_real_escape_string($dserial),
		mysql_real_escape_string($dname)
	);
	
	db_query($query);
}

# Function to change device name
function changeDeviceName($dserial, $dname) {
	# Change device name in Devices table
	$query = sprintf("UPDATE Devices SET name='%s' WHERE serial=%s",
		mysql_real_escape_string($dname),
		mysql_real_escape_string($dserial)
	);
	
	db_query($query);
}

# Function to remove device
function removeDevice($dserial, $dname) {
	$query = sprintf("DELETE FROM Devices WHERE serial=%s AND name='%s'",
		mysql_real_escape_string($dserial),
		mysql_real_escape_string($dname)
	);
	
	db_query($query);
}

# Function to update device active state
function toggleDeviceActive($dserial, $dname, $dactive) {
	$query = sprintf("UPDATE Devices SET active=%s WHERE serial=%s AND name='%s'",
		mysql_real_escape_string($dactive),
		mysql_real_escape_string($dserial),
		mysql_real_escape_string($dname)
	);
	
	db_query($query);
}

############################ Email related functions
# Function to get all emails
function getEmails() {
	return db_query("SELECT email FROM Emails");
}

# Function to add new email
function addEmail($email) {
	$query = sprintf("INSERT INTO Emails VALUES('%s')",
		mysql_real_escape_string($email)
	);
	
	db_query($query);
}

# Function to remove email
function removeEmail($email) {
	$query = sprintf("DELETE FROM Emails WHERE email='%s'",
		mysql_real_escape_string($email)
	);
	
	db_query($query);
}

# Function to change email
function changeEmail($newemail, $oldemail) {
	# Change device name in Devices table
	$query = sprintf("UPDATE Emails SET email='%s' WHERE email='%s'",
		mysql_real_escape_string($newemail),
		mysql_real_escape_string($oldemail)
	);
	
	db_query($query);
}


############################################## Playback related functions
# Function to return list of nodename and playback folders
function getCamPlaybacksResult() {
	return db_query("SELECT nodename, recordfolder FROM Playbacks");
}

############### Function to send command to remore Pi via socket
function sendPiCam($cam, $msg) {
	$ip = getCamIP($cam);
	if($ip == '') die("cam not found: " . $cam);
	
	$sock = socket_create(AF_INET, SOCK_STREAM, SOL_TCP);
	if(!$sock) die('socket_create');
	
	if(!socket_connect($sock, $ip, 44444)) {
		socket_close($sock);
		die('socket_connect: ' . $ip . ', ' . $msg);
	}
	
	socket_send($sock, $msg, strlen($msg), 0);
	
	socket_close($sock);
}

# Function to send STARTPLAYBACK command
function startPlayback($cam, $path) {
	sendPiCam($cam, 'STARTPLAYBACK,' . $path);
}

# Function to send INIT command
function camReset($cam) {
	sendPiCam($cam, 'INIT');
}

# Function to send DELPLAYBACK
function deletePlayback($cam, $path) {
	$query = sprintf("DELETE FROM Playbacks WHERE nodename='%s' AND recordfolder='%s'",
		mysql_real_escape_string($cam),
		mysql_real_escape_string($path)
	);
	db_query($query);
	
	sendPiCam($cam, 'DELPLAYBACK,' . $path);	
}

# Function to send STARTRECORD command
function startRecord($cam, $path) {
	sendPiCam($cam, 'STARTRECORD,' . $path);
	
	$query = sprintf("INSERT INTO Playbacks VALUES('%s', '%s')",
		mysql_real_escape_string($cam),
		mysql_real_escape_string($path)
	);
	
	db_query($query);
}


################################################# Function to send command to central PiHome
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

# Function to set switch state through PiHome, should use sendCommandToPiHome function
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
