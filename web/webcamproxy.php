<?
if(!isset($_REQUEST['cam']) || !isset($_REQUEST['port']) || !isset($_REQUEST['n'])) exit();

require_once('DBManager.php');

$n = $_REQUEST['n'];
$cam_sel = $_REQUEST['cam'];
$ip = getCamIP($cam_sel);
$port = $_REQUEST['port'];

set_time_limit(0);
$fp = fsockopen($ip, $port, $errno, $errstr, 30);

if(!$fp) {
	echo "$errstr ($errno)<br>\n";
} else {
	$urlstring = "GET /?action=snapshot&n=" . $n . " HTTP/1.0\r\n\r\n";
	fputs ($fp, $urlstring);
	
	while ($str = trim(fgets($fp, 4096))) {
		header($str);
	}
		
	fpassthru($fp);
	fclose($fp);
}
?>
