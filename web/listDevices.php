<!DOCTYPE HTML>
<html>
	<head>
		<title>Pimation Device Manager</title>
		<? include("meta.php"); ?>
	</head>

	<body>
		<? include("header.php"); ?>
		
		<h1>Welcome to Pimation Device Manager!</h1>
<?
		# Pre action to take care of self-direct requests
		if(isset($_REQUEST['command']) && isset($_REQUEST['dserial']) && isset($_REQUEST['dname'])) {
			if($_REQUEST['command'] == "adddevice"){
				addDevice('0x'.$_REQUEST['dserial'], $_REQUEST['dname']);
				sendCommandToPiHome($_REQUEST['command'], $_REQUEST['dserial']);
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
			
			header('Location: ' . $_SERVER['PHP_SELF']);
		}
		else if(isset($_REQUEST['dserial']) && isset($_REQUEST['toggle'])) {
			setDeviceState($_REQUEST['dserial'], $_REQUEST['toggle']);
			sleep(1);
			header('Location: ' . $_SERVER['PHP_SELF']);
		}
		else if(isset($_REQUEST['command']) && isset($_REQUEST['email'])) {
			if($_REQUEST['command'] == "addemail"){
				addEmail($_REQUEST['email']);
			}
			else if($_REQUEST['command'] == "removeemail"){
				removeEmail($_REQUEST['email']);
			}
			else if($_REQUEST['command'] == "changeemail"){
				changeEmail($_REQUEST['newemail'],$_REQUEST['email']);
			}
			header('Location: ' . $_SERVER['PHP_SELF']);
		}
		else if(isset($_REQUEST['command']) && isset($_REQUEST['nodename']) && isset($_REQUEST['nodeaddress'])) {
			if($_REQUEST['command'] == "addnode"){
				addNode($_REQUEST['nodename'], $_REQUEST['nodeaddress']);
			}
			else if($_REQUEST['command'] == "delnode"){
				removeNode($_REQUEST['nodename'], $_REQUEST['nodeaddress']);
			}
			else if($_REQUEST['command'] == "changenodename"){
				changeNodeName($_REQUEST['nodename'], $_REQUEST['nodenewname']);
			}
			
			header('Location: ' . $_SERVER['PHP_SELF']);
		}
?>
		<h2>Camera Manager</h2>
		<form action="<? echo $_SERVER['PHP_SELF']; ?>" method="post">
			Camera Name: <input type="text" name="nodename">
			Pi address: <input type="text" name="nodeaddress">
			<input type="hidden" name="command" value="addnode">
			<input type="submit" value="Add">
		</form>

		<table border="1">		
<?
		$result = getNodes();
		
		# Header row
		echo '<tr>';
		# Extra collumn for Action
		echo '<td>Action</td>';
		# Populate all collumns
		for($i = 0; $i < mysql_num_fields($result); $i++) {
			# Get collumn header
			$meta = mysql_fetch_field($result, $i);
			echo '<td>' . $meta->name . '</td>';
		}
		echo "</tr>\n";
		
		# Start populating rows
		while($row = mysql_fetch_row($result)) {
			echo '<tr>';
			# First collumn is Action button
			echo '<td>';
?>
			<form action="<? echo $_SERVER['PHP_SELF']; ?>" method="post">
					<input type="hidden" name="nodename" value="<? echo $row[0]; ?>">
					<input type="hidden" name="nodeaddress" value="<? echo $row[1]; ?>">
					<input type="hidden" name="command" value="delnode">
					<input type="submit" value="Remove">
			</form>
<?
			echo '</td>';
			# Populate rest of collumns
			for($i = 0; $i < mysql_num_fields($result); $i++){
				# Get collumn header
				$meta = mysql_fetch_field($result, $i);
				
				# Add change name button for Name collumn
				if($meta->name == 'nodename') {
				    echo '<td>';

					?><form action="<? echo $_SERVER['PHP_SELF']; ?>" method="post">
						<input type="text" name="nodenewname" value="<? echo $row[0]; ?>">
						<input type="hidden" name="nodename" value="<? echo $row[0]; ?>">						
						<input type="hidden" name="nodeaddress" value="<? echo $row[1]; ?>">
						<input type="hidden" name="command" value="changenodename">
						<input type="submit" value="Change name">
					</form><?
				    echo '</td>';
				}
				else echo '<td>' . $row[$i] . '</td>';
			}
			echo "</tr>\n";
		}
?>
		</table>
		
		<h2>Device Manager</h2>
		<form action="<? echo $_SERVER['PHP_SELF']; ?>" method="post">
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
		# Extra command collumn at the front
		echo '<td>Command</td>';
		for($i = 0; $i < mysql_num_fields($result); $i++) {
			# Get collumn header
			$meta = mysql_fetch_field($result, $i);
			echo '<td>' . $meta->name . '</td>';
		}
		# Extra trigger collumn at the end
		echo '<td>Trigger</td>';

		echo "</tr>\n";
		
		while($row = mysql_fetch_row($result)) {
			echo '<tr>';
			# Extra collumn for removing device
			echo '<td>';
?>
			<form action="<? echo $_SERVER['PHP_SELF']; ?>" method="post">
				<input type="hidden" name="dserial" value="<? echo $row[0]; ?>">
				<input type="hidden" name="dname" value="<? echo $row[2]; ?>">
				<input type="hidden" name="command" value="removedevice">
				<input type="submit" value="Remove">
			</form>
<?
			echo '</td>';
			
			for($i = 0; $i < mysql_num_fields($result); $i++){
				# Get collumn header
				$meta = mysql_fetch_field($result, $i);
				
				if($row[1] == DeviceType::PowerSwitch and $meta->name == 'Status') {
					$t_str = 'On';
					$t_m = 1;
				
					if($row[3] == 1) {
						$t_str = 'Off';
						$t_m = 0;
					}
				    echo '<td>' . $row[$i];

					?><form action="<? echo $_SERVER['PHP_SELF']; ?>" method="post">
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
					
					?><form action="<? echo $_SERVER['PHP_SELF']; ?>" method="post">
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

					?><form action="<? echo $_SERVER['PHP_SELF']; ?>" method="post">
						<input type="hidden" name="dserial" value="<? echo $row[0]; ?>">
						<input type="text" name="dname" value="<? echo $row[2]; ?>">
						<input type="hidden" name="command" value="changedevicename">
						<input type="submit" value="Change name">
					</form><?
				    echo '</td>';
				}
				else echo '<td>' . $row[$i] . '</td>';
			}
			
			# Extra collumn at the end for adding trigger
			echo '<td>';
?>
			<form action="triggers.php" method="post">
				<input type="hidden" name="dserial" value="<? echo $row[0]; ?>">
				<input type="hidden" name="dtype" value="<? echo $row[1]; ?>">
				<input type="hidden" name="dname" value="<? echo $row[2]; ?>">
				<input type="hidden" name="command" value="addtrigger">
				<input type="submit" value="Add trigger">
			</form>
<?
			echo '</td>';
			echo "</tr>\n";
		}
?>
		</table>

		<h2>Email Manager</h2>
		<form action="<? echo $_SERVER['PHP_SELF']; ?>" method="post">
			Email: <input type="text" name="email">
			<input type="hidden" name="command" value="addemail">
			<input type="submit" value="Add">
		</form>

		<table border="1">		
<?
		$result = getEmails();
		
		# Header row
		echo '<tr>';
		# Extra collumn for Action
		echo '<td>Action</td>';
		# Populate all collumns
		for($i = 0; $i < mysql_num_fields($result); $i++) {
			# Get collumn header
			$meta = mysql_fetch_field($result, $i);
			echo '<td>' . $meta->name . '</td>';
		}
		echo "</tr>\n";
		
		# Start populating rows
		while($row = mysql_fetch_row($result)) {
			echo '<tr>';
			# First collumn is Action button
			echo '<td>';
?>
			<form action="<? echo $_SERVER['PHP_SELF']; ?>" method="post">
					<input type="hidden" name="email" value="<? echo $row[0]; ?>">
					<input type="hidden" name="command" value="removeemail">
					<input type="submit" value="Remove">
			</form>
<?
			echo '</td>';
			# Populate rest of collumns
			for($i = 0; $i < mysql_num_fields($result); $i++){
				# Get collumn header
				$meta = mysql_fetch_field($result, $i);
				
				# Add change name button for Name collumn
				if($meta->name == 'email') {
				    echo '<td>';

					?><form action="<? echo $_SERVER['PHP_SELF']; ?>" method="post">
						<input type="text" name="newemail" value="<? echo $row[0]; ?>">
						<input type="hidden" name="email" value="<? echo $row[0]; ?>">						
						<input type="hidden" name="command" value="changeemail">
						<input type="submit" value="Change name">
					</form><?
				    echo '</td>';
				}
				else echo '<td>' . $row[$i] . '</td>';
			}
			echo "</tr>\n";
		}
?>
		</table>
		
		<?php include("footer.php"); ?>
	</body>
</html>
