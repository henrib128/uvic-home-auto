<!DOCTYPE HTML>
<html>
	<head>
		<title>Pimation Trigger Manager</title>
	</head>

	<body>
		<h1>Welcome to Pimation Trigger Manager!</h1>
		<ul><a href="/pimation.php">Back to Home page</a></ul>

<?
		require_once('DBManager.php');
		db_connect();
		
		# Pre action to take care of self-direct requests
		if(isset($_REQUEST['command']) && isset($_REQUEST['dserial'])) {
			if($_REQUEST['command'] == "addtrigger" && $_REQUEST['dtype'] == 1){
				# First add new entry to Door Trigger table
				addDoorTrigger('0x'.$_REQUEST['dserial']);
			}
			else if($_REQUEST['command'] == "updateswitch"){
				# Upadate trigger table
				updateDoorSwitch('0x'.$_REQUEST['dserial'],'0x'.$_REQUEST['sserial']);
			}
			else if($_REQUEST['command'] == "updateopenon"){
				if(isset($_REQUEST['openon'])) $openon = 1;
				else $openon = 0; 
				# Upadate trigger table
				updateOpenOn('0x'.$_REQUEST['dserial'],$openon);
			}
			else if($_REQUEST['command'] == "removetrigger"){
				# Upadate trigger table
				removeDoorTrigger('0x'.$_REQUEST['dserial']);
			}
						
			# Return to self rendering
			header('Location: ' . $_SERVER['PHP_SELF']);
		}
?>
		
		<h2>Trigger Manager</h2>
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
				<input type="hidden" name="command" value="removetrigger">
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
				else if($meta->name == 'openon') {
				    echo '<td>';

					?><form action="triggers.php" method="post">
						<input type="hidden" name="dserial" value="<? echo $row[0]; ?>">
						<input type="checkbox" name="openon" value=1 <? if($row[2]==1) echo 'checked="True"'?>>
						<input type="hidden" name="command" value="updateopenon">
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
	</body>
</html>
