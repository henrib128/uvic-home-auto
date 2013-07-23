<!DOCTYPE HTML>
<html>
	<head>
		<title>Devices</title>
	</head>

	<body>
		<h1>Devices</h1>
		<table border="1">
<?
		require_once('DBManager.php');
		db_connect();
		
		if(isset($_REQUEST['dserial']) && isset($_REQUEST['dname']) && isset($_REQUEST['add'])) {
			addDevice($_REQUEST['dserial'], $_REQUEST['dname']);
			setDeviceState($_REQUEST['dserial'], $_REQUEST['add']);
			header('Location: ' . $_SERVER['PHP_SELF']);
		}
		else if(isset($_REQUEST['dserial']) && isset($_REQUEST['toggle'])) {
			setDeviceState($_REQUEST['dserial'], $_REQUEST['toggle']);
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
