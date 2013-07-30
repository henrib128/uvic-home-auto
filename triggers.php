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
			else if($_REQUEST['command'] == "updatetrigger"){
				# Upadate trigger table
				updateDoorTrigger('0x'.$_REQUEST['dserial'],'0x'.$_REQUEST['sserial'],$_REQUEST['openon']);
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
			
				echo '<td>' . $row[$i] . '</td>';
			}
			
			echo "</tr>\n";
		}
?>
		</table>
	</body>
</html>
