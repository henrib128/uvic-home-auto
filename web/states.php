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
			
			if(isset($_REQUEST['dserial']) && isset($_REQUEST['status'])) {
				setDeviceState($_REQUEST['dserial'], !$_REQUEST['status']);
				header('Location: ' . $_SERVER['PHP_SELF']);
			}
			
			$result = getStatesResult();
			
			echo "<tr><th>Name</th><th>State</th><th>Command</th></tr>\n";
			
			while($row = mysql_fetch_object($result)) {
				echo '<tr>';
				
				echo '<td>' . $row->Name . '</td>';
				echo '<td>' . $row->State . '</td>';
				
				echo '<td>';
				if($row->Type == DeviceType::PowerSwitch) { ?>
					<form action="<? echo $_SERVER['PHP_SELF']; ?>" method="post">
						<input type="hidden" name="dserial" value="<? echo $row->Serial; ?>">
						<input type="hidden" name="status" value="<? echo $row->Status; ?>">
						<input type="submit" value="Turn <? echo stateToStr(!$row->Status); ?>">
					</form>
				<? }
				echo '</td>';
				
				echo "</tr>\n";
			}
?>
		</table>
	</body>
</html>
