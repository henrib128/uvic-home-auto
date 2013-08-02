<!DOCTYPE HTML>
<html>
	<head>
		<title>Pimation Homepage</title>
		<? include("meta.php"); ?>
	</head>

	<body>
		<? include("header.php"); ?>
		
		<h1>Welcome to Pimation Home Page!</h1>
		
		<? if($isAdmin) { ?>
		<p>You are the administrator. You have full control of your Pimation system, including:</p><br>
			<li>Devices Tab: You can add new devices such as camera, door sensor, power switch via this page. You can also turn on and off your switch and see your door status in this page.</li>
			<li>Triggers Tab: You can turn on a power switch when a door opens. You can also schedule to turn on/off your power switch at certain time daily.</li>
			<li>Live Cams Tab: You can view all of your cameras live here! You can also record actions live and see it later if you want to.</li>
			<li>Playbacks Tab: You can view all of your recordings here.</li>
		</p>
		<? } ?>
			
		<h2>Users</h2>
	
		<table border="1">
			<tr><th>Username</th><th>Administrator</th><th>New Password</th><th>Submit</th></tr>
<?
		if(isset($_REQUEST['username']) && isset($_REQUEST['pass'])) {
			if($isAdmin) changePass($_REQUEST['username'], $_REQUEST['pass']);
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
		
		<? include("footer.php"); ?>
	</body>
</html>
