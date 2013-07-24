<!DOCTYPE HTML>
<html>
	<head>
		<title>Pimation Device Manager</title>
	</head>

	<body>
		<h1>Welcome to Pimation Device Manager!</h1>
		<ul><a href="/pimation.php">Back to Home page</a></ul>

<?
		require_once('DBManager.php');
		db_connect();
		
		# Pre action to take care of self-direct requests
		if(isset($_REQUEST['command']) && isset($_REQUEST['dserial']) && isset($_REQUEST['dname'])) {
			if($_REQUEST['command'] == "adddevice"){
				addDevice('0x'.$_REQUEST['dserial'], $_REQUEST['dname']);
			}
			else if($_REQUEST['command'] == "removedevice"){
				removeDevice('0x'.$_REQUEST['dserial'], $_REQUEST['dname']);
			}
			else if($_REQUEST['command'] == "toggleactive"){
				toggleDeviceActive('0x'.$_REQUEST['dserial'], $_REQUEST['dname'], $_REQUEST['dactive']);
			}
			else if($_REQUEST['command'] == "changedevicename"){
				changeDeviceName('0x'.$_REQUEST['dserial'], $_REQUEST['dname']);
			}
			
			sendCommandToPiHome($_REQUEST['command'], $_REQUEST['dserial']);
			header('Location: ' . $_SERVER['PHP_SELF']);
		}
		else if(isset($_REQUEST['dserial']) && isset($_REQUEST['toggle'])) {
			setDeviceState($_REQUEST['dserial'], $_REQUEST['toggle']);
			header('Location: ' . $_SERVER['PHP_SELF']);
		}
		else if(isset($_REQUEST['command']) && isset($_REQUEST['nodename']) && isset($_REQUEST['nodeaddress'])) {
			if($_REQUEST['command'] == "addnode"){
				addNode($_REQUEST['nodename'], $_REQUEST['nodeaddress']);
			}
			else if($_REQUEST['command'] == "delnode"){
				removeNode($_REQUEST['nodename'], $_REQUEST['nodeaddress']);
			}
			
			sendCommandToPiHome($_REQUEST['command'], $_REQUEST['nodename'] . ',' . $_REQUEST['nodeaddress']);
			header('Location: ' . $_SERVER['PHP_SELF']);
		}
?>
		<h2>Add new camera node</h2>
		<form action="listDevices.php" method="post">
			Camera Name: <input type="text" name="nodename">
			Pi address: <input type="text" name="nodeaddress">
			<input type="hidden" name="command" value="addnode">
			<input type="submit" value="Add">
		</form>

		<table border="1">		
<?
		$result = getNodes();

		echo '<tr>';
		for($i = 0; $i < mysql_num_fields($result); $i++) {
			$meta = mysql_fetch_field($result, $i);
			echo '<td>' . $meta->name . '</td>';
		}
		echo '<td>Action</td>';
		echo "</tr>\n";
		
		while($row = mysql_fetch_row($result)) {
			echo '<tr>';
			for($i = 0; $i < mysql_num_fields($result); $i++) echo '<td>' . $row[$i] . '</td>';
			echo '<td>';
?>
			<form action="listDevices.php" method="post">
					<input type="hidden" name="nodename" value="<? echo $row[0]; ?>">
					<input type="hidden" name="nodeaddress" value="<? echo $row[1]; ?>">
					<input type="hidden" name="command" value="delnode">
					<input type="submit" value="Remove">
			</form>
<?
			echo '</td>';
			echo "</tr>\n";
		}
?>
		</table>
		
		<h2>Device Manager Table</h2>
		<form action="listDevices.php" method="post">
			Serial Number: <input type="text" name="dserial">
			Name: <input type="text" name="dname">
			<input type="hidden" name="command" value="adddevice">
			<input type="submit" value="Add">
		</form>
		<table border="1">		
<?
		require_once('DBManager.php');
		db_connect();
		
		$result = getDevicesResult();

		echo '<tr>';
		echo '<td>Command</td>';
		for($i = 0; $i < mysql_num_fields($result); $i++) {
			$meta = mysql_fetch_field($result, $i);
			echo '<td>' . $meta->name . '</td>';
		}

		echo "</tr>\n";
		
		while($row = mysql_fetch_row($result)) {
			echo '<tr>';
			
			# Extra collume for removing device
			echo '<td>';
?>
			<form action="listDevices.php" method="post">
				<input type="hidden" name="dserial" value="<? echo $row[0]; ?>">
				<input type="hidden" name="dname" value="<? echo $row[2]; ?>">
				<input type="hidden" name="command" value="removedevice">
				<input type="submit" value="Remove">
			</form>
<?
			echo '</td>';
			
			for($i = 0; $i < mysql_num_fields($result); $i++){
				$meta = mysql_fetch_field($result, $i);
				
				if($row[1] == DeviceType::PowerSwitch and $meta->name == 'Status') {
					$t_str = 'On';
					$t_m = 1;
				
					if($row[3] == 1) {
						$t_str = 'Off';
						$t_m = 0;
					}
				    echo '<td>' . $row[$i];

					?><form action="listDevices.php" method="post">
						<input type="hidden" name="dserial" value="<? echo $row[0]; ?>">
						<input type="hidden" name="toggle" value="<? echo $t_m; ?>">
						<input type="submit" value="Turn <? echo $t_str; ?>">
					</form><?
				    echo '</td>';
				}
				else if($meta->name == 'Active') {
				    echo '<td>' . $row[$i];

					if($row[5] == 1) {
						$t_str = 'Deactive';
						$t_m = 0;
					}
					else if($row[5] == 0) {
						$t_str = 'Activate';
						$t_m = 1;
					}
					
					?><form action="listDevices.php" method="post">
						<input type="hidden" name="dserial" value="<? echo $row[0]; ?>">
						<input type="hidden" name="dname" value="<? echo $row[2]; ?>">
						<input type="hidden" name="dactive" value="<? echo $t_m; ?>">
						<input type="hidden" name="command" value="toggleactive">
						<input type="submit" value="<? echo $t_str; ?>">
					</form><?
				    echo '</td>';
				}
				else if($meta->name == 'Name') {
				    echo '<td>';

					?><form action="listDevices.php" method="post">
						<input type="hidden" name="dserial" value="<? echo $row[0]; ?>">
						<input type="text" name="dname" value="<? echo $row[2]; ?>">
						<input type="hidden" name="command" value="changedevicename">
						<input type="submit" value="New name">
					</form><?
				    echo '</td>';
				}
				else echo '<td>' . $row[$i] . '</td>';
			}
			echo "</tr>\n";
		}
?>
		</table>
	</body>
</html>
