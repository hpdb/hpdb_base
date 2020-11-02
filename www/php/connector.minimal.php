<?php

// // elFinder autoload
require './autoload.php';
// ===============================================

// // Enable FTP connector netmount
elFinder::$netDrivers['ftp'] = 'FTP';
// ===============================================

/**
 * Simple function to demonstrate how to control file access using "accessControl" callback.
 * This method will disable accessing files/folders starting from '.' (dot)
 *
 * @param  string    $attr    attribute name (read|write|locked|hidden)
 * @param  string    $path    absolute file path
 * @param  string    $data    value of volume option `accessControlData`
 * @param  object    $volume  elFinder volume driver object
 * @param  bool|null $isDir   path is directory (true: directory, false: file, null: unknown)
 * @param  string    $relpath file path relative to volume root directory started with directory separator
 * @return bool|null
 **/
function access($attr, $path, $data, $volume, $isDir, $relpath) {
	$basename = basename($path);
	return $basename[0] === '.'                // if file/folder begins with '.' (dot)
			 && strlen($relpath) !== 1             // but with out volume root
		? !($attr == 'read' || $attr == 'write') // set read+write to false, other (locked+hidden) set to true
		:  null;                                 // else elFinder decide it itself
}

// read config
function read_config($configFile) {
  $file_handle = fopen($configFile, "rb");
  while (!feof($file_handle) ) {
    $line_of_text = fgets($file_handle);
    $line_of_text = rtrim($line_of_text);
    if (preg_match("/=/", $line_of_text)){
      $parts = explode('=', $line_of_text);
      $array["$parts[0]"] = $parts[1];
    }
  }
  fclose($file_handle);
  return $array;
}

$hpdb_config = read_config(__DIR__ . "/../../sys.properties");

$conn = new mysqli('localhost', 'root', 'hpdb2020', 'hpdb');
if ($conn->connect_error) {
  die('{"result": "error", "message": "Failed to open MySQL connection."}');
}
$sql = "select * from sessions where sid='" . $_REQUEST["sid"] . "'";
$result = $conn->query($sql);
if ($result->num_rows == 0) {
  die('{"result": "error", "message": "Session expired."}');
}

$row = mysqli_fetch_assoc($result);
$userid = $row["userid"];
$userdir = $hpdb_config["hpdb_data"] . $userid;

// Documentation for connector options:
// https://github.com/Studio-42/elFinder/wiki/Connector-configuration-options
$opts = array(
	// 'debug' => true,
	'roots' => array(
		// Items volume
		array(
			'driver'        => 'LocalFileSystem',           // driver for accessing file system (REQUIRED)
			'path'          => $userdir,                    // path to files (REQUIRED)
      'alias'         => 'My Files',
			'URL'           => dirname($_SERVER['PHP_SELF']) . '/../files/', // URL to files (REQUIRED)
			'trashHash'     => 't1_Lw',                     // elFinder's hash of trash folder
			'winHashFix'    => DIRECTORY_SEPARATOR !== '/', // to make hash same to Linux one on windows too
			'uploadDeny'    => array('all'),                // All Mimetypes not allowed to upload
			'uploadAllow'   => array('image/x-ms-bmp', 'image/gif', 'image/jpeg', 'image/png', 'image/x-icon', 'text/plain'), // Mimetype `image` and `text/plain` allowed to upload
			'uploadOrder'   => array('deny', 'allow'),      // allowed Mimetype `image` and `text/plain` only
			'accessControl' => 'access'                     // disable and hide dot starting files (OPTIONAL)
		)
	)
);

// run elFinder
$connector = new elFinderConnector(new elFinder($opts));
$connector->run();

?>
