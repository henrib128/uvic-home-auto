<!DOCTYPE HTML>
<html>
	<head>
		<title>Pimation Homepage</title>
		<? include("meta.php"); ?>
	</head>

	<body>
		<? include("header.php"); ?>
		
		<h1>Welcome to Pimation Home Page!</h1>
<?
		# Path to local PiMation working directory
		$pimation_dir = '/home/pi/uvic-home-auto/';
		#$pimation_dir="/home/tri/ceng499/uvic-home-auto/";

		# Pre action to take care of self-direct requests
		if(isset($_REQUEST['command'])) {
			if($_REQUEST['command'] == "startcentral"){
				# First kill all PiHome and PiCam instance
				exec("killall -9 PiHome.py");
				exec("killall -9 PiCam.py");
			
				# Then start PiHome and PiCam in the background
				exec($pimation_dir . "PiCam.py &");
				exec($pimation_dir . "PiHome.py &");
			}
			else if($_REQUEST['command'] == "startremote"){
				# First kill all PiHome and PiCam instance
				exec("killall -9 PiHome.py");
				exec("killall -9 PiCam.py");
	
				# Then start PiCam in the background
				exec($pimation_dir . "PiCam.py &");
			}			
						
			# Return to self rendering
			header('Location: ' . $_SERVER['PHP_SELF']);
		}
?>
		<p>Click below to restart your central Pi</p>
		<form action="<? echo $_SERVER['PHP_SELF']; ?>" method="post">
			<input type="hidden" name="command" value="startcentral">
			<input type="submit" value="Restart Central Pi">
		</form>

		<p>Click below to restart your remote Pi</p>
		<form action="<? echo $_SERVER['PHP_SELF']; ?>" method="post">
			<input type="hidden" name="command" value="startremote">
			<input type="submit" value="Restart Remote Pi">
		</form>
		
		<? include("footer.php"); ?>
	</body>
</html>
