<!DOCTYPE html>
<!--
 
    UCLA Astro Coffee Discussed List Adder
	by Abhimat Gautam
	based on previous work by Ryan T. Hamilton,
	Ian J. Crossfield, and Nathaniel Ross
	
	
	Discussed paper adder called by following syntax:
	http://coffee.astro.ucla.edu/discussed.php?ID=[ID]
  
-->

<?php

//
//
// If you see this text in your browser, it means PHP scripts are not
// enabled on this web server.  Consult the internet or your local system
// administrator to enable PHP scripting.
//
//

// SET THE PATH TO YOUR PYTHON VERSION HERE
// $python = '/usr/bin/python';

$ID = $_GET['ID'];

$python = '/Users/abhimat/software/Ureka/variants/common/bin/python';

// CHOOSE YOUR TIMEZONE FROM THE LINK BELOW AND SET IT HERE
$CurrentVer = phpversion();
if(version_compare($CurrentVer, '5.1.0')>=0) {
    date_default_timezone_set('US/Pacific');
    #http://www.php.net/manual/en/timezones.others.php
}

$paperFile = "../papers_discussed";
$logFile = "../dregs.log";
$listManager = "../listmanager.php";
// $ID = $_POST["article"];
$ipOfSubmitter=$_SERVER["REMOTE_ADDR"];

$minlength = 5;
// echo '<META HTTP-EQUIV=Refresh CONTENT="10">';
echo '<META HTTP-EQUIV=Refresh CONTENT="1;url=../">';
echo "<p>You submitted ".$ID.".</p>";

# Testing for coffee time (can't submit otherwise (silly robots :( ))
if (!(((date('H') >= 11 and date('H') < 12) or (date('H') >= 14 and date('H') < 15)) and (date('w') <= 5 and date('w') >= 1))) {
	echo '<p><strong>Not coffee time!</strong></p>';
	echo '<p>Paper not added to discussed list. Please wait until coffee time to add.</p>';
    echo "<p>Returning to the main page automatically in 1 second</p>";
    echo "<p>If not, click <a href='../'>here</a></p>";
	die;
}

# Testing for duplicates
$papers = file($paperFile) or die("can't open file: ".$paperFile);
foreach ($papers as $pap){
	if (trim($ID) == trim($pap)) {
		echo '<p>But it is a duplicate of a paper already submitted for the discussed list!</p>';
		echo '<p>If you think this is an error, tell the coffee czar.</p>';
        echo "<p>Returning to the main page automatically in 1 second</p>";
        echo "<p>If not, click <a href='../'>here</a></p>";
		die;
	}
}


# Valid submission
if (strlen($ID)>$minlength) {
	$f = fopen($paperFile,"a") or die("can't open file: ".$paperFile);
	fwrite($f, "\n".trim($ID));
	fclose($f);
	# Get estimate of run time for the user
	$lines = count(file($paperFile)); 
	$time  = $lines * 10;
	echo "<p>The paper was successfully added to the discussed papers list.</p>";
	echo "<p>It may be several minutes before the main page is updated.</p>";
	echo "<p>You will be returned to the main page in 1 second.</p>";
	echo "<p>If not, click <a href='../'>here</a></p>";
	$str4log = date('D, d M Y H:i:s')."    ".$ID."    ".$ipOfSubmitter."    Paper added to discussed papers list.";
	$f2 = fopen($logFile,"a") or die("can`t open file: ".$logFile);
	fwrite($f2, $str4log."\n");
	fclose($f2);
	
	$nullRet = `$python runcoffee.py > /dev/null &`;
	
} else {
	echo "This is shorter than the minimum valid string length (".$minlength.").";
	echo "Thus your submission was not added to the papers list.";
}
//
// } else {
// 	echo "you should not have reached this point!";
// }
?>