<!DOCTYPE HTML>
<html>
	<head>
		<title>Pimation Camera Manager</title>
		<? include("meta.php"); ?>
		
		<script type="text/javascript">
		var frameNr = 0;
		var loadCnt = 0;
		var counts = new Array();
		
		var size = document.getElementsByTagName('img').length;
		for(i = 0; i < 2; i++) counts[i] = 0;
		
		function refresh(cam, countsIndex) {
			var img = document.getElementById(cam);
			
			counts[countsIndex]++;
			
			img.src = "/webcamproxy.php?cam=" + escape(cam) + "&port=8080" + "&n=" + counts[countsIndex];
		}
		
		</script>
	</head>
	<body>
		<? include("header.php"); ?>
		
		<h1>Welcome to Pimation Camera Manager!</h1>
<?
		require_once('DBManager.php');
		db_connect();
		
		if(isset($_REQUEST['action']) && isset($_REQUEST['cam']) && isset($_REQUEST['path'])) {
			$act = $_REQUEST['action'];
			$cam_rec = $_REQUEST['cam'];
			$path = $_REQUEST['path'];
			$loc = 'Location: ' . $_SERVER['PHP_SELF'];
			
			if($act == 'Record') {
				startRecord($cam_rec, $path);
				header($loc . '?cam_rec=' . urlencode($cam_rec));
			}
			else if($act == 'Stop') {
				camReset($cam_rec);
				header($loc);
			}
			else die('invalid action 2');
		}

		$result = getCamNamesResult();
		$i = 0;
		while($cam = mysql_fetch_array($result)) {
			$cam = $cam[0];
			echo "<h1>" . $cam . "</h1><br>\n";
?>
			<form action="<? echo $_SERVER['PHP_SELF']; ?>" method="post">
				Record Folder: <input type="text" name="path"><br>
				<input type="hidden" name="cam" value="<? echo $cam; ?>" />
				<input type="submit" name="action" value="Record" />
				<input type="submit" name="action" value="Stop" />
			</form>
		
<?
			echo "<img id='" . $cam . "' src='/blank.jpg' onload=\"refresh('" . $cam . "', " . $i . ");\"/>";
			$i++;
		}
?>

		<?php include("/footer.php"); ?>
	</body>
</html>
