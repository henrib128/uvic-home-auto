<!DOCTYPE HTML>
<html>
	<head>
		<title>Pimation Trigger Manager</title>
		<? include("meta.php"); ?>
	</head>

	<body>
		<? include("header.php"); ?>
		
		<h1>Welcome to Pimation Trigger Manager!</h1>

<?
		# Pre action to take care of self-direct requests
		if(isset($_REQUEST['command']) && isset($_REQUEST['dserial'])) {
			if($_REQUEST['command'] == "addtrigger" && $_REQUEST['dtype'] == 1){
				# First add new entry to Door Trigger table
				if($isAdmin) addDoorTrigger('0x'.$_REQUEST['dserial']);
			}
			else if($_REQUEST['command'] == "addtrigger" && $_REQUEST['dtype'] == 0){
				# First add new entry to Door Trigger table
				if($isAdmin) addSwitchTrigger('0x'.$_REQUEST['dserial']);
			}			
			else if($_REQUEST['command'] == "updateswitch"){
				# Upadate trigger table
				if($isAdmin) updateDoorSwitch('0x'.$_REQUEST['dserial'],'0x'.$_REQUEST['sserial']);
			}
			else if($_REQUEST['command'] == "updatedooraction" && isset($_REQUEST['dooraction'])){
				# Upadate trigger table
				if($isAdmin) updateDoorAction('0x'.$_REQUEST['dserial'],$_REQUEST['dooraction']);
			}
			else if($_REQUEST['command'] == "updateontime"){
				# Upadate trigger table
				if($isAdmin) updateOnTime('0x'.$_REQUEST['dserial'],$_REQUEST['ondailytime']);
			}	
			else if($_REQUEST['command'] == "updateofftime"){
				# Upadate trigger table
				if($isAdmin) updateOffTime('0x'.$_REQUEST['dserial'],$_REQUEST['offdailytime']);
			}						
			else if($_REQUEST['command'] == "removedoortrigger"){
				# Upadate trigger table
				if($isAdmin) removeDoorTrigger('0x'.$_REQUEST['dserial']);
			}
			else if($_REQUEST['command'] == "removeswitchtrigger"){
				# Upadate trigger table
				if($isAdmin) removeSwitchTrigger('0x'.$_REQUEST['dserial']);
			}

			# Return to self rendering
			header('Location: ' . $_SERVER['PHP_SELF']);
		}
		else if(isset($_REQUEST['command']) && isset($_REQUEST['oldrecordtime']) && isset($_REQUEST['newrecordtime'])) {									
			$command = $_REQUEST['command'];
			$oldrecordtime = $_REQUEST['oldrecordtime'];
			$newrecordtime = $_REQUEST['newrecordtime'];
						
			if($command == "updaterecordtime"){
				# Update record time table
				if($isAdmin) updateRecordTime($newrecordtime, $oldrecordtime);
			}		
			# Return to self rendering
			header('Location: ' . $_SERVER['PHP_SELF']);
		}
?>
		<h2>Cameras Recording Time</h2>
		<p>Specify how long you want to record on all cameras when a door is opened (door must be activated).</p>
		
		<table border="1">
<?
		# Getting list of record time
		$result = getRecordTime();
		
		# Header row
		echo '<tr>';
		# Populate all collumns
		for($i = 0; $i < mysql_num_fields($result); $i++) {
			# Get collumn header
			$meta = mysql_fetch_field($result, $i);
			echo '<th>' . $meta->name . '</th>';
		}
		echo "</tr>\n";
		
		# Start populating rows
		while($row = mysql_fetch_row($result)) {
			echo '<tr>';
			# Populate rest of collumns
			for($i = 0; $i < mysql_num_fields($result); $i++){
				# Get collumn header
				$meta = mysql_fetch_field($result, $i);
				
				# Add change name button for Name collumn
				if($meta->name == 'recordtime') {
				    echo '<td>';
					?><form action="<? echo $_SERVER['PHP_SELF']; ?>" method="post">
						<input type="text" name="newrecordtime" value="<? echo $row[0]; ?>"> seconds
						<input type="hidden" name="oldrecordtime" value="<? echo $row[0]; ?>">						
						<input type="hidden" name="command" value="updaterecordtime">
						<input type="submit" value="Update">
					</form><?
				    echo '</td>';
				}
				else echo '<td>' . $row[$i] . '</td>';
			}
			echo "</tr>\n";
		}		
?>		
		</table>
		
		<h2>Door Sensor Triggers</h2>
		<p>Associate your door to a power switch to have it turned on or off everytime the door is opened and closed (door must be activated). Open On means the switch will be turned on when door opens (and turned off when door closes). Open Off means the opposite. None to disable it.</p>
		
		<table border="1">		
<?
		$result = getDoorTriggers();

		echo '<tr>';
		# Extra command collumn at the front
		echo '<th>Command</th>';
		for($i = 0; $i < mysql_num_fields($result); $i++) {
			# Get collumn header
			$meta = mysql_fetch_field($result, $i);
			echo '<th>' . $meta->name . '</th>';
		}
		echo "</tr>\n";
		
		while($row = mysql_fetch_row($result)) {
			echo '<tr>';
			# Extra collumn for removing device
			echo '<td>';
?>
			<form action="triggers.php" method="post">
				<input type="hidden" name="dserial" value="<? echo $row[0]; ?>">
				<input type="hidden" name="command" value="removedoortrigger">
				<input type="submit" value="Remove">
			</form>
<?
			echo '</td>';
			
			for($i = 0; $i < mysql_num_fields($result); $i++){
				# Get collumn header
				$meta = mysql_fetch_field($result, $i);
				
				# Allow changing SwitchSerial field
				if($meta->name == 'switchserial') {
				    echo '<td>';

					?><form action="triggers.php" method="post">
						<input type="hidden" name="dserial" value="<? echo $row[0]; ?>">
						<input type="text" name="sserial" value="<? echo $row[1]; ?>">
						<input type="hidden" name="command" value="updateswitch">
						<input type="submit" value="Change switch">
					</form><?
				    echo '</td>';
				}
				else if($meta->name == 'action') {
				    echo '<td>';

					?><form action="triggers.php" method="post">
						<input type="hidden" name="dserial" value="<? echo $row[0]; ?>">
						<input type="radio" name="dooraction" value=0 <? if($row[2]==0) echo 'checked="True"'?>>None
						<input type="radio" name="dooraction" value=1 <? if($row[2]==1) echo 'checked="True"'?>>OpenOn
						<input type="radio" name="dooraction" value=2 <? if($row[2]==2) echo 'checked="True"'?>>OpenOff
						<input type="hidden" name="command" value="updatedooraction">
						<input type="submit" value="Save">
					</form><?
				    echo '</td>';
				}							
				else echo '<td>' . $row[$i] . '</td>';
			}
			
			echo "</tr>\n";
		}
?>
		</table>

		<h2>Power Switch Triggers</h2>
		<p>You can schedule your power switch to automatically turn on and off at a specific time of the day every day. i.e. 1430 for 2:30 pm.</p>
		
		<table border="1">		
<?
		$result = getSwitchTriggers();

		echo '<tr>';
		# Extra command collumn at the front
		echo '<th>Command</th>';
		for($i = 0; $i < mysql_num_fields($result); $i++) {
			# Get collumn header
			$meta = mysql_fetch_field($result, $i);
			echo '<th>' . $meta->name . '</th>';
		}
		echo "</tr>\n";
		
		while($row = mysql_fetch_row($result)) {
			echo '<tr>';
			# Extra collumn for removing device
			echo '<td>';
?>
			<form action="triggers.php" method="post">
				<input type="hidden" name="dserial" value="<? echo $row[0]; ?>">
				<input type="hidden" name="command" value="removeswitchtrigger">
				<input type="submit" value="Remove">
			</form>
<?
			echo '</td>';
			
			for($i = 0; $i < mysql_num_fields($result); $i++){
				# Get collumn header
				$meta = mysql_fetch_field($result, $i);
				
				# Allow changing ondailytime field
				if($meta->name == 'ondailytime') {
				    echo '<td>';

					?><form action="triggers.php" method="post">
						<input type="hidden" name="dserial" value="<? echo $row[0]; ?>">
						<input type="text" name="ondailytime" value="<? echo $row[1]; ?>">
						<input type="hidden" name="command" value="updateontime">
						<input type="submit" value="Change time">
					</form><?
				    echo '</td>';
				}
				# Allow changing offdailytime field
				else if($meta->name == 'offdailytime') {
				    echo '<td>';

					?><form action="triggers.php" method="post">
						<input type="hidden" name="dserial" value="<? echo $row[0]; ?>">
						<input type="text" name="offdailytime" value="<? echo $row[2]; ?>">
						<input type="hidden" name="command" value="updateofftime">
						<input type="submit" value="Change time">
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
