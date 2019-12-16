<?php

// Make sure file is not cached (as it happens for example on iOS devices)
header("Expires: Mon, 26 Jul 1997 05:00:00 GMT");
header("Last-Modified: " . gmdate("D, d M Y H:i:s") . " GMT");
header("Cache-Control: no-store, no-cache, must-revalidate");
header("Cache-Control: post-check=0, pre-check=0", false);
header("Pragma: no-cache");

// Support CORS
header("Access-Control-Allow-Origin: *");
// other CORS headers if any...
if ($_SERVER['REQUEST_METHOD'] == 'OPTIONS') {
  exit; // finish preflight CORS requests here
}

//read config
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

$hpdb_config = read_config(__DIR__ . "/../sys.properties");

// 5 minutes execution time
@set_time_limit(5 * 60);

// Uncomment this one to fake upload time
// usleep(5000);

$conn = new mysqli('localhost', 'root', 'hpdb2019', 'hpdb');
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
$targetDir = $hpdb_config["hpdb_data"] . $userid . '/MyUpload';
$cleanupTargetDir = true; // Remove old files
$maxDay = ($hpdb_config["hpdb_proj_store_days"] > 0) ? $hpdb_config["hpdb_proj_store_days"] : 1000;
$maxFileAge = $maxDay * 24 * 60 * 60; // Temp file age in maxday days

// Create target dir
if (!file_exists($targetDir)) {
  @mkdir($targetDir);
}

// Get a file name
if (isset($_REQUEST["name"])) {
  $fileName = $_REQUEST["name"];
} elseif (!empty($_FILES)) {
  $fileName = $_FILES["file"]["name"];
} else {
  $fileName = uniqid("file_");
}

$filePath = $targetDir . DIRECTORY_SEPARATOR . $fileName;

// Chunking might be enabled
$chunk = isset($_REQUEST["chunk"]) ? intval($_REQUEST["chunk"]) : 0;
$chunks = isset($_REQUEST["chunks"]) ? intval($_REQUEST["chunks"]) : 0;

// Remove old temp files
if ($cleanupTargetDir) {
  if (!is_dir($targetDir) || !$dir = opendir($targetDir)) {
    die('{"result": "error", "message": "Failed to open temp directory."}');
  }

  while (($file = readdir($dir)) !== false) {
    $tmpfilePath = $targetDir . DIRECTORY_SEPARATOR . $file;

    // If temp file is current file proceed to the next
    if ($tmpfilePath == "{$filePath}.part") {
      continue;
    }

    // Remove temp file if it is older than the max age and is not the current file
    if (preg_match('/\.part$/', $file) || (filemtime($tmpfilePath) < time() - $maxFileAge)) {
      unlink($tmpfilePath);
    }
  }
  closedir($dir);
}


// Open temp file
if (!$out = @fopen("{$filePath}.part", $chunks ? "ab" : "wb")) {
  die('{"result": "error", "message": "Failed to open output stream."}');
}

if (!empty($_FILES)) {
  if ($_FILES["file"]["error"] || !is_uploaded_file($_FILES["file"]["tmp_name"])) {
    die('{"result": "error", "message": "Failed to move uploaded file."}');
  }

  // Read binary input stream and append it to temp file
  if (!$in = @fopen($_FILES["file"]["tmp_name"], "rb")) {
    die('{"result": "error", "message": "Failed to open input stream."}');
  }
} else {
  if (!$in = @fopen("php://input", "rb")) {
    die('{"result": "error", "message": "Failed to open input stream."}');
  }
}

while ($buff = fread($in, 4096)) {
  fwrite($out, $buff);
}

@fclose($out);
@fclose($in);

// Check if file has been uploaded
if (!$chunks || $chunk == $chunks - 1) {
  // Strip the temp .part suffix off
  $fileType = mime_content_type("{$filePath}.part");
  if(preg_match("/text/i", $fileType)){
    system("sed 's/\r//' \"{$filePath}.part\" >$filePath");
    unlink("{$filePath}.part");
  }else{
    rename("{$filePath}.part", $filePath);
  }
}

// Return success response
die('{"result": "success"}');
?>