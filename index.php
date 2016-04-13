<!DOCTYPE html>
<!--
 
    UCLA Astro Coffee Page, by Abhimat Gautam
	based on previous versions by Ryan T. Hamilton, Ian J. Crossfield, and Nathaniel Ross
  
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

<html lang="en">
<head>
	<meta charset="UTF-8">
	<title>UCLA Astro Coffee</title>
	
	<!-- Google Web Fonts -->
	<link href='http://fonts.googleapis.com/css?family=Source+Sans+Pro:400,600,700,900,400italic,600italic,700italic,900italic' rel='stylesheet' type='text/css'>
	<link href='http://fonts.googleapis.com/css?family=Bree+Serif' rel='stylesheet' type='text/css'>
	<link href='http://fonts.googleapis.com/css?family=Montserrat:400,700' rel='stylesheet' type='text/css'>
	
	<meta name=viewport content='width=device-width, initial-scale=1'>
	
	<!--[if lt IE 9]>
		<script src="http://html5shim.googlecode.com/svn/trunk/html5.js"></script>
	<![endif]-->
	
	<!-- Favicon -->
	<link rel="shortcut icon" href="images/favicon.png">
	<link rel="apple-touch-icon" href="images/touch-icon.png">
	
	<!-- Styles -->
	<link rel="stylesheet" href="./styles.css" type="text/css" media="screen" />
	
	<!-- MathJax -->
	<script type="text/javascript"
	  src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML">
	  MathJax.Hub.Config({
	    tex2jax: {
	      inlineMath: [['$','$'], ['\\(','\\)']],
	      processEscapes: true
	    }
	  });
	</script>
</head>

<body>
	<header>
		<!-- <p><a href="http://www.astro.ucla.edu"><semibold><em>UCLA</em> Astronomy and Astrophysics</semibold></a></p> -->
		<!-- <h1>Astro Coffee</h1> -->
		<img src="images/Header_2x.png" srcset="images/Header_1x.png 1x, images/Header_2x.png 2x" alt="Astro Coffee" />
		
		<center><ul class="pages">
			<li><strong>Current Articles</strong></li>
			<li><a href="./archive/">Archive</a></li>
			<li><a href="./usefullinks/">Useful Links</a></li>
		</ul></center>
		
		<form method="post" class="submission" action="<?php echo $PHP_SELF;?>">
			<center><input type="text" name="article" maxlength="128" placeholder="Submit a URL (no PDF links) or arXiv-ID" class="field"/></center>
			<input type="submit" value="submit" name="submit" class="button"/>
		</form>
		
		<center><ul class="pages-small small">
			<li><a href="./bookmarklet/">Bookmarklet</a></li>
			<li><a href="./listmanager.php">Submissions</a></li>
			<li><a href="./status.log">Status Log</a></li>
		</ul></center>		
	</header>
	
	<div class="content wrap">
		<section class="blocks">
			<?php include("astro_coffee.php"); ?>
		</section> <!-- /blocks -->
	</div> <!-- /content -->
	
	<footer class="small wrap">
		<center><p class="small"><strong>Astro Coffee 2</strong><br>by <a href="http://astro.ucla.edu/~abhimat/">Abhimat Gautam</a></p></center>
		<center><p class="small">Based on previous versions of astroph.py by<br>Ryan T. Hamilton, Ian J. Crossfield, and Nathaniel Ross.</p></center>
		<center><p class="small"><a href="https://github.com/abhimat/AstroCoffee">Contribute on GitHub!</a></p></center>
	</footer>
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
  
  # Testing for PDF >:(
  if (strpos(trim($article), '.pdf') !== false) {
  	echo '<p>It appears that you have submitted a PDF link.<br><strong>Please submit a link to the webpage of the paper instead.</strong></p>';
  	echo '<p>If you think this is an error, tell the coffee czar.</p>';
  	echo "<p>You will be returned to your original page in 10 seconds.</p>";
  	echo "<p>If not, click <a href='".$article."'>here</a></p>";
  	die;
  }
  
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