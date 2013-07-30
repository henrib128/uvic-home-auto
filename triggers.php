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
		require_once('DBManager.php');
		db_connect();
		
		# Pre action to take care of self-direct requests
		if(isset($_REQUEST['command']) && isset($_REQUEST['dserial'])) {
			if($_REQUEST['command'] == "addtrigger" && $_REQUEST['dtype'] == 1){
				# First add new entry to Door Trigger table
				addDoorTrigger('0x'.$_REQUEST['dserial']);
			}
			else if($_REQUEST['command'] == "addtrigger" && $_REQUEST['dtype'] == 0){
				# First add new entry to Door Trigger table
				addSwitchTrigger('0x'.$_REQUEST['dserial']);
			}			
			else if($_REQUEST['command'] == "updateswitch"){
				# Upadate trigger table
				updateDoorSwitch('0x'.$_REQUEST['dserial'],'0x'.$_REQUEST['sserial']);
			}
			else if($_REQUEST['command'] == "updatedooraction" && isset($_REQUEST['dooraction'])){
				# Upadate trigger table
				updateDoorAction('0x'.$_REQUEST['dserial'],$_REQUEST['dooraction']);
			}
			else if($_REQUEST['command'] == "updateontime"){
				# Upadate trigger table
				updateOnTime('0x'.$_REQUEST['dserial'],$_REQUEST['ondailytime']);
			}	
			else if($_REQUEST['command'] == "updateofftime"){
				# Upadate trigger table
				updateOffTime('0x'.$_REQUEST['dserial'],$_REQUEST['offdailytime']);
			}						
			else if($_REQUEST['command'] == "removedoortrigger"){
				# Upadate trigger table
				removeDoorTrigger('0x'.$_REQUEST['dserial']);
			}
			else if($_REQUEST['command'] == "removeswitchtrigger"){
				# Upadate trigger table
				removeSwitchTrigger('0x'.$_REQUEST['dserial']);
			}
									
			# Return to self rendering
			header('Location: ' . $_SERVER['PHP_SELF']);
		}
?>
		
		<h2>Door Trigger Manager</h2>
		<table border="1">		
<?
		require_once('DBManager.php');
		db_connect();
		
		$result = getDoorTriggers();

		echo '<tr>';
		# Extra command collumn at the front
		echo '<td>Command</td>';
		for($i = 0; $i < mysql_num_fields($result); $i++) {
			# Get collumn header
			$meta = mysql_fetch_field($result, $i);
			echo '<td>' . $meta->name . '</td>';
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

		<h2>Switch Trigger Manager</h2>
		<table border="1">		
<?
		require_once('DBManager.php');
		db_connect();
		
		$result = getSwitchTriggers();

		echo '<tr>';
		# Extra command collumn at the front
		echo '<td>Command</td>';
		for($i = 0; $i < mysql_num_fields($result); $i++) {
			# Get collumn header
			$meta = mysql_fetch_field($result, $i);
			echo '<td>' . $meta->name . '</td>';
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
