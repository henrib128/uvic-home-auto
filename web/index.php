<!DOCTYPE HTML>
<html>
	<head>
		<title>Pimation Homepage</title>
		<? include("meta.php"); ?>
	</head>

	<body>
		<? include("header.php"); ?>
		
		<h1>Welcome to Pimation Home Page!</h1>
		
		<? if(isAdmin()) { ?>
		
		<h2>Users</h2>
		
		<table border="1">
<?
		if(isset($_REQUEST['username']) && isset($_REQUEST['pass'])) {
			changePass($_REQUEST['username'], $_REQUEST['pass']);
			header('Location: ' . $_SERVER['PHP_SELF']);
		}
		
		$result = getUsers();
		
		echo '<tr>';
		
		for($i = 0; $i < mysql_num_fields($result); $i++) {
			$meta = mysql_fetch_field($result, $i);
			echo '<th>' . $meta->name . '</th>';
		}
		
		echo "<th>New Password</th><th>Submit</th></tr>\n";
		
		while($row = mysql_fetch_row($result)) {
			echo '<tr>';
			
			for($i = 0; $i < mysql_num_fields($result); $i++) {
				echo '<td>' . $row[$i] . '</td>';
			}
?>
			<form action="<? echo $_SERVER['PHP_SELF']; ?>" method="post">
					<input type="hidden" name="username" value="<? echo $row[0]; ?>">
					<td><input type="text" name="pass"></td>
					<td><input type="submit" value="Change"></td>
			</form>
<?
			echo "</tr>\n";
		}
?>
		</table>
		
		<? } ?>
		
		<? include("footer.php"); ?>
	</body>
</html>
