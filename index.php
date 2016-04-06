<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<!--

Design by Free CSS Templates
http://www.freecsstemplates.org
Released for free under a Creative Commons Attribution 2.5 License

Name       : Tastelessly
Description: A very light design suitable for community sites and blogs.
Version    : 1.0
Released   : 20080122

Changed a lot from the original above, basically all I kept is the color
  scheme and some of the button styles.
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
$article = $_POST["article"];
$ipOfSubmitter=$_SERVER["REMOTE_ADDR"];

if ((!isset($_POST["submit"])) and (!isset($_POST["submitcheck"])))
  { // if page is not submitted, show the form
  ?>

<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="content-type" content="text/html; charset=utf-8" />
<title>UCLA astro-ph Coffee</title>
<meta name="keywords" content="" />
<meta name="description" content="" />
<link href="style.css" rel="stylesheet" type="text/css" media="screen" />
</head>
<body>
<div id="logo">
    <h1>UCLA astro-ph Coffee</h1>
    <!-- <p>Your Tagline Can Be Here!</p> -->
</div>
<!-- start page -->
<div id="page">
    <!-- Begin common header -->
    <div id="header">
        <div id="menu">
            <ul>
                <li class="current_page_item"><a href="./">Current Discussion Articles</a></li>
                <li><a href="./archive/">Discussion Paper Archive</a></li>
                <li><a href="./">Refresh Page</a></li>
            </ul>
        </div>
		<!-- <div id="search">
					<form method=GET action="http://www.google.com/search">
						<a href="http://www.google.com"><img src="http://www.google.com/logos/Logo_25wht.gif" border="0" ALT="Google" align="absmiddle"></A>
						<input type="hidden" name="ie" value="UTF-8" />
						<input type="text" name="q" size="20" maxlength=255 class="text" />
						<input type="submit" name="btnG" value="Search" class="button" />
						<input type="reset" name="btnC" value="Clear" class="button" />
					</form>
				</div> -->
	</div>
	<!-- End common header -->

	<!-- start content -->
    <div id="content">
        <div class="post">
			<?php include("astro_coffee.php"); ?>
        </div>
    </div>
	<!-- end content -->

	<!-- start sidebar one -->
	<div id="sidebar1" class="sidebar">
		<ul>
			<li id="recent-posts">
				<h2>Post a Paper/Link</h2>
				<p>
					<?php include("coffee_submit.php"); ?>
                    <div style="text-align: center;font-size: 0.5em;">
                    <a href="./status.log">Check Status Log</a>
                    </div>
				</p>
				<!-- <h2>Weather Checks</h2>
								<ul>
									<li>
										<p>
										<a href="http://forecast.weather.gov/MapClick.php?CityName=Las+Cruces&state=NM&site=EPZ&textField1=32.3361&textField2=-106.756">NOAA Forecast</a><br>
										LC:&nbsp&nbsp <a href=http://cleardarksky.com/c/LCruNMkey.html><img src="http://cleardarksky.com/c/LCruNMcs0.gif?1" border=0></a><br>
										APO: <a href=http://cleardarksky.com/c/ApachePtNMkey.html><img src="http://cleardarksky.com/c/ApachePtNMcs0.gif?1" border=0></a><br>
										</p>
									</li>
								</ul> -->
			</li>
		</ul>
	</div>
	<div id="sidebar1" class="sidebar">
			<h2>Useful Links</h2>
				<p>
				<?php include("useful.links"); ?>
				<br>
		<!-- </div>
				<div id="subsidebar2" class="subsidebar2">
					<h2>General Links</h2>
						<p>
						<?php include("general.links"); ?> -->
	</div>
	<!-- <div id="sidebar1" class="sidebar">
			<ul>
				<li>
					<h2>Calendar</h2>
	<!-- Insert your favorite online calendar link (Google Cals.) here -->

		</div>
	<!-- end sidebar one -->

	<div style="clear: both;">&nbsp;</div>
</div>
<!-- end page -->
<hr />
<!-- start footer -->
<div id="footer">
	<!-- <p>&copy;<script type="text/javascript">var d = new Date();document.write(d.getFullYear());</script> All Rights Reserved. &nbsp;&bull;&nbsp; Designed by <a href="http://www.freecsstemplates.org/">Free CSS Templates</a> and tweaked like heck by Ryan T. Hamilton.</p> -->
</div>
<!-- end footer -->
<!-- If you use Google Analytics, insert the tracking PHP file below... -->

</body>
</html>
<? // If check-form _was_ submitted, display this instead:
  } elseif (isset($_POST["submitcheck"])) {
  echo 'Loading article list manager...<br>';
  echo '<META HTTP-EQUIV=Refresh CONTENT="1;'.$listManager.'">';

// If submit-form _was_ submitted, display this instead:
} elseif (isset($_POST["submit"])) {
  $minlength = 5;
  echo '<META HTTP-EQUIV=Refresh CONTENT="10">';
  echo "<p>You submitted ".$article.".</p>";
  
  # Testing for duplicates
  $papers = file($paperFile) or die("can't open file: ".$paperFile);
  foreach ($papers as $pap){
     if (trim($article) == trim($pap)) {
         echo '<p>But it is a duplicate of a paper already submitted!</p>';
         echo '<p>If you think this is an error, tell the coffee czar.</p>';
         echo "<p>Returning to the main page automatically in 10 seconds</p>";
         echo "<p>If not, click <a href='./'>here</a></p>";
         die;
     }
  }

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
    echo "<p>You will be returned to the main page in 10 seconds.</p>";
    echo "<p>If not, click <a href='./'>here</a></p>";
    $str4log = date('D, d M Y H:i:s')."    ".$article."    ".$ipOfSubmitter;
    $f2 = fopen($logFile,"a") or die("can`t open file: ".$logFile);
    fwrite($f2, $str4log."\n");
    fclose($f2);

    $nullRet = `$python runcoffee.py > /dev/null &`;

  } else {
    echo "This is shorter than the minimum valid string length (".$minlength.").";
    echo "Thus your submission was not added to the papers list.";
  }

} else {
  echo "you should not have reached this point!";
}
?>
