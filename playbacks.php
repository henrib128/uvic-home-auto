<!DOCTYPE HTML>
<html>
	<head>
		<title>Cameras</title>
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
		<h1>Cameras</h1>
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
		<br><br>
		<div id="webcam"></div>
	</body>
</html>
