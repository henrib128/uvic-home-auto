<!DOCTYPE HTML>
<html>
	<head>
		<title>Pimation Playback Manager</title>
		<? include("meta.php"); ?>
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
		<? include("header.php"); ?>
		<h1>Welcome to Pimation Playback Manager!</h1>
		<p>Here you can view and manage all your recordings. Pick a recording and hit play to start viewing. Delete with remove the recording permanently. Right now you can only view one recording at a time.</p>
		<form action="<? echo $_SERVER['PHP_SELF']; ?>" method="post">
			<select name="cam" id="cam_id" size=4>
<?
			$cam_sel = '';
			$cam_rec = '';
			$loc = 'Location: ' . $_SERVER['PHP_SELF'];
			
			if(isset($_REQUEST['cam'])) {
				$cam_sel = $_REQUEST['cam'];
				
				if(isset($_REQUEST['action'])) {
					$a = explode(':', $cam_sel, 2);
					
					if(count($a) != 2) die('wrong count');
					
					if($_REQUEST['action'] == 'Play') {
						startPlayback($a[0], $a[1]);
						header($loc . '?cam=' . urlencode($cam_sel));
					}
					else if($_REQUEST['action'] == 'Delete') {
						# First delete playback from the database
						# Then sending delete command to the remote Pi
						deletePlayback($a[0], $a[1]);
						
						# Then sending INIT command to refresh the camera Pi
						camReset($a[0]);
						header($loc);
					}
					else die('invalid action');
				}
			}
			
			$result = getCamPlaybacksResult();
			while($cam = mysql_fetch_array($result)) {
				$op = $cam[0] . ':' . $cam[1];
				echo "\t\t\t\t<option value='$op'";
				if($op == $cam_sel) echo " selected";
				echo ">$op</option>\n";
				
			}
?>
			</select>
			<input type="submit" name="action" value="Play" />
			<input type="submit" name="action" value="Delete" />
		</form>
		
		<br><br>
		<div id="webcam"><img src='/blank.jpg' /></div>
		
		<?php include("footer.php"); ?>
	</body>
</html>
