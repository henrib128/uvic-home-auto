<!DOCTYPE HTML>
<html>
	<head>
		<title>Pimation Playback Manager</title>
	</head>

	<script type="text/javascript">

	/* Copyright (C) 2007 Richard Atterer, richardÂ©atterer.net
	   This program is free software; you can redistribute it and/or modify it
	   under the terms of the GNU General Public License, version 2. See the file
	   COPYING for details. */

	var imageNr = 0; // Serial number of current image
	var finished = new Array(); // References to img objects which have finished downloading
	var paused = false;

	function createImageLayer() {
	  var img = new Image();
	  img.style.position = "absolute";
	  img.style.zIndex = -1;
	  img.onload = imageOnload;
	  img.onclick = imageOnclick;
	  var a = document.getElementById("cam_id").value;
	  a = a.split(':');
	  img.src = "/webcamproxy.php?action=snapshot&n=" + (++imageNr) + "&cam=" + escape(a[0]) + "&port=8081";
	  var webcam = document.getElementById("webcam");
	  webcam.insertBefore(img, webcam.firstChild);
	}

	// Two layers are always present (except at the very beginning), to avoid flicker
	function imageOnload() {
	  this.style.zIndex = imageNr; // Image finished, bring to front!
	  while (1 < finished.length) {
		var del = finished.shift(); // Delete old image(s) from document
		del.parentNode.removeChild(del);
	  }
	  finished.push(this);
	  if (!paused) createImageLayer();
	}

	function imageOnclick() { // Clicking on the image will pause the stream
	  paused = !paused;
	  if (!paused) createImageLayer();
	}

	</script>

	<body onload="createImageLayer();">
		<h1>Welcome to Pimation Playback Manager!</h1>
		<ul><a href="/pimation.php">Back to Home page</a></ul>
		
		<h2>Playback Manager Table</h2>
		<form action="playbacks.php" method="post">
			Camera Name: <input type="text" name="nodename">
			Folder Name: <input type="text" name="playbackfolder">
			<input type="submit" value="Add">
		</form>

		<table border="1">
<?
		require_once('DBManager.php');
		db_connect();
		
		if(!isset($_REQUEST['command']) && isset($_REQUEST['nodename']) && isset($_REQUEST['playbackfolder'])) {
			addPlayback($_REQUEST['nodename'], $_REQUEST['playbackfolder']);
			header('Location: ' . $_SERVER['PHP_SELF']);
		}
		else if(isset($_REQUEST['command']) && isset($_REQUEST['nodename']) && isset($_REQUEST['playbackfolder'])) {
			if($_REQUEST['command'] == "delplayback"){
				removePlayback($_REQUEST['nodename'], $_REQUEST['playbackfolder']);
			}
			
			# Send command to PiHome
			sendCommandToPiHome($_REQUEST['command'], $_REQUEST['nodename'] . ',' . $_REQUEST['playbackfolder']);
			header('Location: ' . $_SERVER['PHP_SELF']);
		}
		
		# Populate playback list
		$result = getCamPlaybacksResult();

		echo '<tr>';
		for($i = 0; $i < mysql_num_fields($result); $i++) {
			$meta = mysql_fetch_field($result, $i);
			echo '<td>' . $meta->name . '</td>';
		}
		# Extra collums for Playback, Remove, and Download action
		echo '<td>Play</td>';
		echo '<td>Delete</td>';
		echo '<td>Download</td>';
		echo "</tr>\n";
		
		while($row = mysql_fetch_row($result)) {
			echo '<tr>';
			for($i = 0; $i < mysql_num_fields($result); $i++) echo '<td>' . $row[$i] . '</td>';

			# Extra Play collumn
			echo '<td>';
?>			
			<form action="playbacks.php" method="post">
				<input type="hidden" name="nodename" value="<? echo $row[0]; ?>">
				<input type="hidden" name="playbackfolder" value="<? echo $row[1]; ?>">
				<input type="hidden" name="command" value="playplayback">
				<input type="submit" value="Play">
			</form>
<?
			echo '</td>';

			# Extra Delete collumn
			echo '<td>';
?>			
			<form action="playbacks.php" method="post">
				<input type="hidden" name="nodename" value="<? echo $row[0]; ?>">
				<input type="hidden" name="playbackfolder" value="<? echo $row[1]; ?>">
				<input type="hidden" name="command" value="delplayback">
				<input type="submit" value="Delete">
			</form>
<?
			echo '</td>';
			
			# Extra Download collumn
			echo '<td>';
?>			
			<form action="playbacks.php" method="post">
				<input type="hidden" name="nodename" value="<? echo $row[0]; ?>">
				<input type="hidden" name="playbackfolder" value="<? echo $row[1]; ?>">
				<input type="hidden" name="command" value="downloadplayback">
				<input type="submit" value="Download">
			</form>
<?
			echo '</td>';
			
			echo "</tr>\n";
		}
?>
		</table>

		<br><br>

		<h2>Select Camera to play playback from</h2>
		<select onchange="createImageLayer();" name="cam" id="cam_id" size=4>
<?
		require_once('DBManager.php');
		db_connect();
				
		$result = getCamPlaybacksResult();
		
		while($cam = mysql_fetch_array($result)) {
			echo "\t\t\t<option value='$cam[0]:$cam[1]'>$cam[0]</option>\n";
		}
?>
		</select>
		<!-- Playback window 
		-->
		<div id="webcam"></div>
	</body>
</html>
