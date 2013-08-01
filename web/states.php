<!DOCTYPE HTML>
<html>
	<head>
		<meta http-equiv="refresh" content="1">
	</head>
	
	<body>
		<table border="1">
<?
			require_once('DBManager.php');
			
			$result = getStatesResult();
			
			echo '<tr>';
			
			for($i = 0; $i < mysql_num_fields($result); $i++) {
				$meta = mysql_fetch_field($result, $i);
				echo '<th>' . $meta->name . '</th>';
			}
			
			echo "</tr>\n";
			
			while($row = mysql_fetch_row($result)) {
				echo '<tr>';
				
				for($i = 0; $i < mysql_num_fields($result); $i++) {
					echo "<td>" . $row[$i] . "</td>";
				}
				
				echo "</tr>\n";
			}
?>
		</table>
	</body>
</html>
