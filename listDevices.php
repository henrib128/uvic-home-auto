<!DOCTYPE HTML>
<html>
	<head>
		<title>Devices</title>
	</head>

	<body>
		<h1>Welcome to Pimation Device Manager!</h1>
		<ul><a href="/index.php">Back to Home page</a></ul>

		<h2>Add new camera node</h2>
		<form action="listDevices.php" method="post">
			Camera Name: <input type="text" name="nodename">
			Pi address: <input type="text" name="nodeaddress">
			<input type="hidden" name="command" value="addcam">
			<input type="submit" value="Add">
		</form>
		
		<h2>Device Manager Table</h2>
		<form action="listDevices.php" method="post">
			Serial Number: <input type="text" name="dserial">
			Name: <input type="text" name="dname">
			<input type="hidden" name="command" value="add">
			<input type="submit" value="Add">
		</form>
		<table border="1">		
<?
		require_once('DBManager.php');
		db_connect();
		
		if(isset($_REQUEST['dserial']) && isset($_REQUEST['dname']) && isset($_REQUEST['command'])) {
			addDevice('0x'.$_REQUEST['dserial'], $_REQUEST['dname']);
			sendCommandToPiHome($_REQUEST['command'], $_REQUEST['dserial']);
			header('Location: ' . $_SERVER['PHP_SELF']);
		}
		else if(isset($_REQUEST['dserial']) && isset($_REQUEST['toggle'])) {
			setDeviceState($_REQUEST['dserial'], $_REQUEST['toggle']);
			header('Location: ' . $_SERVER['PHP_SELF']);
		}
		else if(isset($_REQUEST['nodename']) && isset($_REQUEST['nodeaddress']) && isset($_REQUEST['command'])) {
			addNode($_REQUEST['nodename'], $_REQUEST['nodeaddress']);
			sendCommandToPiHome($_REQUEST['command'], $_REQUEST['nodeaddress']);
			header('Location: ' . $_SERVER['PHP_SELF']);
		}
		
		$result = getDevicesResult();

		echo '<tr>';
		for($i = 0; $i < mysql_num_fields($result); $i++) {
			$meta = mysql_fetch_field($result, $i);
			echo '<td>' . $meta->name . '</td>';
		}
		echo '<td>Send</td>';
		echo "</tr>\n";
		
		while($row = mysql_fetch_row($result)) {
			echo '<tr>';
			for($i = 0; $i < mysql_num_fields($result); $i++) echo '<td>' . $row[$i] . '</td>';
			echo '<td>';
			if($row[1] == DeviceType::PowerSwitch) {
				$t_str = 'On';
				$t_m = 1;
				
				if($row[3] == 1) {
					$t_str = 'Off';
					$t_m = 0;
				}
				
				?><form action="listDevices.php" method="post">
					<input type="hidden" name="dserial" value="<? echo $row[0]; ?>">
					<input type="hidden" name="toggle" value="<? echo $t_m; ?>">
					<input type="submit" value="Turn <? echo $t_str; ?>">
				</form><?
			}
			echo '</td>';
			echo "</tr>\n";
		}
?>
		</table>
	</body>
</html>
