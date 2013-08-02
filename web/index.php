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
			<tr><th>Username</th><th>Administrator</th><th>New Password</th><th>Submit</th></tr>
<?
		if(isset($_REQUEST['username']) && isset($_REQUEST['pass'])) {
			changePass($_REQUEST['username'], $_REQUEST['pass']);
			header('Location: ' . $_SERVER['PHP_SELF']);
		}
		
		$result = getUsers();
		
		while($row = mysql_fetch_object($result)) {
			echo '<tr><td>' . $row->username . '</td><td>' . yesNo($row->is_admin) . '</td>';
?>
				<form action="<? echo $_SERVER['PHP_SELF']; ?>" method="post">
					<input type="hidden" name="username" value="<? echo $row->username; ?>">
					<td><input type="password" name="pass"></td>
					<td><input type="submit" value="Change"></td>
				</form>
			</tr>
<?
		}
?>
		</table>
		
		<? } ?>
		
		<? include("footer.php"); ?>
	</body>
</html>
