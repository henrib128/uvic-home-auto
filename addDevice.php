<!DOCTYPE HTML>
<html>
	<head>
		<title>Add Device Page</title>
	</head>

	<body>
		<h1>Add new device</h1>
		<form action="listDevices.php" method="post">
			Serial Number: <input type="text" name="dserial">
			Name: <input type="text" name="dname">
			<input type="hidden" name="add" value="3">
			<input type="submit" value="Add">
		</form>
	</body>
</html>
