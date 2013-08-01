<!DOCTYPE HTML>
<html>
	<head>
		<meta http-equiv="refresh" content="1">
		<? include("meta.php"); ?>
	</head>
	
	<body style="background:none;margin:0;">
		<table border="1">
<?
			require_once('DBManager.php');
			
			if(isset($_REQUEST['dserial']) && isset($_REQUEST['toggle'])) {
				setDeviceState($_REQUEST['dserial'], $_REQUEST['toggle']);
				header('Location: ' . $_SERVER['PHP_SELF']);
			}
			
			$result = getStatesResult();
			
			echo '<tr>';
			
			for($i = 0; $i < mysql_num_fields($result); $i++) {
				$meta = mysql_fetch_field($result, $i);
				echo '<th>' . $meta->name . '</th>';
			}
			
			echo '<th>Command</th>';
			
			echo "</tr>\n";
			
			while($row = mysql_fetch_row($result)) {
				echo '<tr>';
				
				for($i = 0; $i < mysql_num_fields($result); $i++) {
					echo "<td>";
					if($i == 3) echo stateToStr($row[3]);
					else echo $row[$i];
					echo "</td>";
				}
				
				echo '<td>';
				
				if($row[2] == DeviceType::PowerSwitch) { ?>
					<form action="<? echo $_SERVER['PHP_SELF']; ?>" method="post">
						<input type="hidden" name="dserial" value="<? echo $row[0]; ?>">
						<input type="hidden" name="toggle" value="<? echo !$row[3]; ?>">
						<input type="submit" value="Turn <? echo stateToStr(!$row[3]); ?>">
					</form>
				<? }
				
				echo '</td>';
				echo "</tr>\n";
			}
?>
		</table>
	</body>
</html>
