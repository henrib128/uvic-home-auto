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
		
		$result = getCamNamesResult();
		
		$i = 0;
		while($cam = mysql_fetch_array($result)) {
			$cam = $cam[0];
			echo "<h1>" . $cam . "</h1><br>\n";
			echo "<img id='" . $cam . "' src='/blank.jpg' onload=\"refresh('" . $cam . "', " . $i . ");\"/>";
			$i++;
		}
?>

		<?php include("/footer.php"); ?>
	</body>
</html>
