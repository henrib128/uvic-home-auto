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
		
		if(isset($_REQUEST['dserial']) && isset($_REQUEST['dtype']) && isset($_REQUEST['dname']))
			addDevice($_REQUEST['dserial'], $_REQUEST['dtype'], $_REQUEST['dname']);
		
		$result = getDevicesResult();
		
		for($i = 0; $i < mysql_num_fields($result); $i++) {
			$meta = mysql_fetch_field($result, $i);
			echo '<td>' . $meta->name . '</td>';
		}
		
		while($row = mysql_fetch_row($result)) {
			echo '<tr>';
			for($i = 0; $i < mysql_num_fields($result); $i++) echo '<td>' . $row[$i] . '</td>';
			echo "</tr>\n";
		}
?>
		</table>
	</body>
</html>
