<?
if(isset($_REQUEST['logout'])) {
	#header('WWW-Authenticate: Basic realm="Pimation"');
	header('HTTP/1.0 401 Unauthorized');
}

require_once('DBManager.php');
?>

<ul id="menu">
	<table>
		<tr>
			<th align="center"><img id="logo" src="/logo.png" alt="PiMation Logo" width="100" height="100"/></th>
			<th align="left"><font size="7"><span style="color:white;font-weight:bold">Pi</span><span style="color:white;font-weight:bold">Mation</span></font></th>
		</tr>
		<tr>
			<form action="<? echo $_SERVER['PHP_SELF']; ?>" method="post" id="logout_form">
			<input type="hidden" name="logout">
			<td>
				<li><a href="/">Home</a></li>
				<li><a href="/listDevices.php">Devices</a></li>
				<li><a href="/triggers.php">Triggers</a></li>
				<li><a href="/cams.php">Live Cams</a></li>
				<li><a href="/playbacks.php">Playbacks</a></li>
				<li><a href="/logout" onclick="document.getElementById('logout_form').submit(); return false;">Logout</a></li>
			</td>
			</form>
		</tr>
	</table>
</ul>
<div id="main">
