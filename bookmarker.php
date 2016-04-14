<!DOCTYPE html>
<!--
 
    UCLA Astro Coffee Bookmarker Page
	by Abhimat Gautam
	based on previous work by Ryan T. Hamilton,
	Ian J. Crossfield, and Nathaniel Ross
	
	
	Bookmarker called by following syntax:
	http://coffee.astro.ucla.edu/bookmarker.php?article=[URL]
	
	To use as bookmarklet, use following link as bookmark:
	javascript:(function(){location.href='http://coffee.astro.ucla.edu/bookmarker.php?article='+encodeURIComponent(location.href);})();
  
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

$article = $_GET['article'];

$python = '/Users/abhimat/software/Ureka/variants/common/bin/python';

// CHOOSE YOUR TIMEZONE FROM THE LINK BELOW AND SET IT HERE
$CurrentVer = phpversion();
if(version_compare($CurrentVer, '5.1.0')>=0) {
    date_default_timezone_set('US/Pacific');
    #http://www.php.net/manual/en/timezones.others.php
}

$paperFile = "papers";
$logFile = "dregs.log";
$listManager = "listmanager.php";
// $article = $_POST["article"];
$ipOfSubmitter=$_SERVER["REMOTE_ADDR"];

$minlength = 5;
// echo '<META HTTP-EQUIV=Refresh CONTENT="10">';
echo '<META HTTP-EQUIV=Refresh CONTENT="10;'.$article.'">';
echo "<p>You submitted ".$article.".</p>";

# Testing for duplicates
$papers = file($paperFile) or die("can't open file: ".$paperFile);
foreach ($papers as $pap){
	if (trim($article) == trim($pap)) {
		echo '<p>But it is a duplicate of a paper already submitted!</p>';
		echo '<p>If you think this is an error, tell the coffee czar.</p>';
		echo "<p>You will be returned to your original page in 10 seconds.</p>";
		echo "<p>If not, click <a href='".$article."'>here</a></p>";
		die;
	}
}

# Testing for usage on an Astro Coffee page >:(
if (strpos(trim($article), 'coffee.astro.ucla.edu') !== false) {
	echo '<p>Please do not use bookmarklet on the Astro Coffee page >:(</p>';
	echo '<p>If you think this is an error, tell the coffee czar.</p>';
	echo "<p>You will be returned to your original page in 10 seconds.</p>";
	echo "<p>If not, click <a href='".$article."'>here</a></p>";
	die;
}

# Testing for PDF >:(
if (strpos(trim($article), '.pdf') !== false) {
	echo '<p>It appears that you have submitted a PDF link.<br><strong>Please submit a link to the webpage of the paper instead.</strong></p>';
	echo '<p>(Come on Devin…)</p>';
	echo '<p>If you think this is an error, tell the coffee czar.</p>';
	echo "<p>You will be returned to your original page in 10 seconds.</p>";
	echo "<p>If not, click <a href='".$article."'>here</a></p>";
	die;
}

# Valid submission
if (strlen($article)>$minlength) {
	$f = fopen($paperFile,"a") or die("can't open file: ".$paperFile);
	fwrite($f, "\n".trim($article));
	fclose($f);
	# Get estimate of run time for the user
	$lines = count(file($paperFile)); 
	$time  = $lines * 10;
	echo "<p>Your sumission was successfully added to the list. </p>";
	echo "<p>Thanks for advancing knowledge!</p>";
	echo "<p>It may be several minutes before the main page is updated.</p>";
	echo "<p>I see $lines items to update, so it will take >$time seconds.</p>";
	echo "<p>You will be returned to your original page in 10 seconds.</p>";
	echo "<p>If not, click <a href='".$article."'>here</a></p>";
	$str4log = date('D, d M Y H:i:s')."    ".$article."    ".$ipOfSubmitter;
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