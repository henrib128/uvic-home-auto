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
			<th align="left"><img id="logo" src="/logo_big.png" alt="PiMation Logo"/></th>
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
