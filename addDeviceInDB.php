<?

$link = mysql_connect('localhost', 'ceng499', 'ceng499');
if(!$link) {
    die('Could not connect: ' . mysql_error());
}

$db_selected = mysql_select_db('pihome', $link);
if(!$db_selected) {
    die ('Can\'t use pihome: ' . mysql_error());
}

$query = sprintf("INSERT INTO Devices VALUES(%s, %s, '%s', 0, 0)",
	mysql_real_escape_string($_POST['dserial']),
	mysql_real_escape_string($_POST['dtype']),
	mysql_real_escape_string($_POST['dname'])
);

$result = mysql_query($query);
if(!$result) {
	$message  = 'Invalid query: ' . mysql_error() . "\n";
	$message .= 'Whole query: ' . $query;
	die($message);
}

echo 'Success';

?>
