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
				if($isAdmin) addDevice('0x'.$_REQUEST['dserial'], $_REQUEST['dname']);
				if($isAdmin) sendCommandToPiHome($_REQUEST['command'], $_REQUEST['dserial']);
			}
			else if($_REQUEST['command'] == "removedevice"){
				if($isAdmin) removeDevice('0x'.$_REQUEST['dserial'], $_REQUEST['dname']);
			}
			else if($_REQUEST['command'] == "toggleactive"){
				if($isAdmin) toggleDeviceActive('0x'.$_REQUEST['dserial'], $_REQUEST['dname'], $_REQUEST['dactive']);
			}
			else if($_REQUEST['command'] == "changedevicename"){
				if($isAdmin) changeDeviceName('0x'.$_REQUEST['dserial'], $_REQUEST['dname']);
			}
			
			header('Location: ' . $_SERVER['PHP_SELF']);
		}
		else if(isset($_REQUEST['dserial']) && isset($_REQUEST['toggle'])) {
			if($isAdmin) setDeviceState($_REQUEST['dserial'], $_REQUEST['toggle']);
			if($isAdmin) sleep(1);
			header('Location: ' . $_SERVER['PHP_SELF']);
		}
		else if(isset($_REQUEST['command']) && isset($_REQUEST['nodename']) && isset($_REQUEST['nodeaddress'])) {
			if($_REQUEST['command'] == "addnode"){
				if($isAdmin) addNode($_REQUEST['nodename'], $_REQUEST['nodeaddress']);
			}
			else if($_REQUEST['command'] == "delnode"){
				if($isAdmin) removeNode($_REQUEST['nodename'], $_REQUEST['nodeaddress']);
			}
			else if($_REQUEST['command'] == "changenodename"){
				if($isAdmin) changeNodeName($_REQUEST['nodename'], $_REQUEST['nodenewname']);
			}
			
			header('Location: ' . $_SERVER['PHP_SELF']);
		}
?>
		<h2>Camera Manager</h2>
		<p>Add new camera by giving it a unique name and ipaddress (check your network). You can also change name or remove it later.</p>
		
		<form action="<? echo $_SERVER['PHP_SELF']; ?>" method="post">
			Camera Name: <input type="text" name="nodename">
			Pi address: <input type="text" name="nodeaddress">
			<input type="hidden" name="command" value="addnode">
			<input type="submit" value="Add">
		</form>

		<table border="1">
			<tr><th>Action</th><th>Name</th><th>IP Address</th></tr>
<?
			$result = getNodes();
		
			while($row = mysql_fetch_object($result)) {
?>
			<tr>
				<td>
					<form action="<? echo $_SERVER['PHP_SELF']; ?>" method="post">
							<input type="hidden" name="nodename" value="<? echo $row->nodename; ?>">
							<input type="hidden" name="nodeaddress" value="<? echo $row->ipaddress; ?>">
							<input type="hidden" name="command" value="delnode">
							<input type="submit" value="Remove">
					</form>
				</td>
				<td>
					<form action="<? echo $_SERVER['PHP_SELF']; ?>" method="post">
						<input type="text" name="nodenewname" value="<? echo $row->nodename; ?>">
						<input type="hidden" name="nodename" value="<? echo $row->nodename; ?>">						
						<input type="hidden" name="nodeaddress" value="<? echo $row->ipaddress; ?>">
						<input type="hidden" name="command" value="changenodename">
						<input type="submit" value="Change name">
					</form>
				</td>
				<td><? echo $row->ipaddress; ?></td>
			</tr>
<?
		}
?>
		</table>
		
		<h2>Device Manager</h2>
		<p>Add new power switch and door sensor to your network by giving it a name and serial number (the 16 digit code on your device). You can activate door sensor to enable email notification and camera recording when door opens. You can also add custome trigger to it (see Triggers tab).</p>
		
		<form action="<? echo $_SERVER['PHP_SELF']; ?>" method="post">
			Serial Number: <input type="text" name="dserial">
			Name: <input type="text" name="dname">
			<input type="hidden" name="command" value="adddevice">
			<input type="submit" value="Add">
		</form>
		
		<table border="1">		
			<tr><th>Command</th><th>Name</th><th>Serial</th><th>Type</th><th>Active</th><th>Trigger</th></tr>
<?
			$result = getDevicesResult();

			while($row = mysql_fetch_object($result)) {
?>
			<tr>
				<td>
					<form action="<? echo $_SERVER['PHP_SELF']; ?>" method="post">
						<input type="hidden" name="dserial" value="<? echo $row->Serial; ?>">
						<input type="hidden" name="dname" value="<? echo $row->Name; ?>">
						<input type="hidden" name="command" value="removedevice">
						<input type="submit" value="Remove">
					</form>
				</td>
				<td>
					<form action="<? echo $_SERVER['PHP_SELF']; ?>" method="post">
						<input type="hidden" name="dserial" value="<? echo $row->Serial; ?>">
						<input type="text" name="dname" value="<? echo $row->Name; ?>">
						<input type="hidden" name="command" value="changedevicename">
						<input type="submit" value="Change name">
					</form>
				</td>
				<td><? echo $row->Serial; ?></td>
				<td><? echo typeToStr($row->Type); ?></td>
<?
				if($row->Active == 1) {
					$t_str = 'Deactive';
					$t_m = 0;
				} else {
					$t_str = 'Activate';
					$t_m = 1;
				}
?>
				<td>
					<form action="<? echo $_SERVER['PHP_SELF']; ?>" method="post">
						<input type="hidden" name="dserial" value="<? echo  $row->Serial; ?>">
						<input type="hidden" name="dname" value="<? echo $row->Name; ?>">
						<input type="hidden" name="dactive" value="<? echo $t_m; ?>">
						<input type="hidden" name="command" value="toggleactive">
						<input type="submit" value="<? echo $t_str; ?>">
					</form>
				</td>
				<td>
					<form action="triggers.php" method="post">
						<input type="hidden" name="dserial" value="<? echo  $row->Serial; ?>">
						<input type="hidden" name="dtype" value="<? echo $row->Type; ?>">
						<input type="hidden" name="dname" value="<? echo $row->Name; ?>">
						<input type="hidden" name="command" value="addtrigger">
						<input type="submit" value="Add trigger">
					</form>
				</td>
			</tr>
<?
			}
?>
		</table>
		
		<h2>Device Live Status</h2>
		<p>This table is automatically refreshed every second for latest updates on your devices.</p>
		
		<iframe src="/states.php" style="border:0;width:100%;height:100%;scrolling:no"></iframe> 

		<?php include("footer.php"); ?>
	</body>
</html>
