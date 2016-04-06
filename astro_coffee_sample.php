<?php

//
// 
// If you see this text in your browser, it means PHP scripts are not
// enabled on this web server.  Consult the internet or your local system
// administrator to enable PHP scripting.
//
//

$paperFile = "papers";
$logFile = "dregs.log";
$listManager = "listmanager.php";
$article = $_POST["article"];
$ipOfSubmitter=$_SERVER["REMOTE_ADDR"];
 
if ((!isset($_POST["submit"])) and (!isset($_POST["submitcheck"])))  
  { // if page is not submitted, show the form
  ?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<title>Astro-ph Coffee at UCLA</title>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<!--
<meta name="keywords" content="astro-ph, arxiv, astronomy, ucla, coffee" />
<meta name="author" content="UCLA Astronomy" />-->
<link rel="stylesheet" type="text/css" href="style.css" />
</head>


<body>
<h2>Astro-ph Coffee suggested papers for Thu, Feb 18, 2010</h2>
<div class="extras">
<div class="submission">
  
  <form method="post" action="<?php echo $PHP_SELF;?>">
  Submit a URL or arXiv-ID:<input type="text" size="12" maxlength="128" name="article">
    <input type="submit" value="submit" name="submit">
    <br><br>
    <input type="submit" value="check submissions file" name="submitcheck">
  </form>
 
</div>
</div>
<p>Astro-ph Coffee is held at 3:00 pm on Thursdays in the
 reading room.  Some new astro-ph postings of interest are
 listed below. Please feel free to suggest additional
 papers to Nate Ross (astro ID nross).</p>
<p> Web article: </p>
<div id="ptitle"><a href="http://coffee.astro.ucla.edu/astro_coffee.php">>astro-ph coffee at ucla</a></div>
<div id="pauthors"></div>
<div id="pabstract"></div>
<p></p>
<p> 5 Feb 2010 </p>
<div id="ptitle"><a href="http://arxiv.org/abs/1002.1115"> Extinction toward the Compact HII Regions G-0.02-0.07</a></div>
<div id="pauthors"> <a href="http://arxiv.org/find/astro-ph/1/au:+Mills_E/0/1/0/all/0/1">E.A. Mills</a>,  <a href="http://arxiv.org/find/astro-ph/1/au:+Morris_M/0/1/0/all/0/1">M.R. Morris</a>,  <a href="http://arxiv.org/find/astro-ph/1/au:+Lang_C/0/1/0/all/0/1">C.C. Lang</a>,  <a href="http://arxiv.org/find/astro-ph/1/au:+Cotera_A/0/1/0/all/0/1">A. Cotera</a>,  <a href="http://arxiv.org/find/astro-ph/1/au:+Dong_H/0/1/0/all/0/1">H. Dong</a>,  <a href="http://arxiv.org/find/astro-ph/1/au:+Wang_Q/0/1/0/all/0/1">Q.D. Wang</a>,  <a href="http://arxiv.org/find/astro-ph/1/au:+Stolovy_S/0/1/0/all/0/1">S.R. Stolovy</a></div>
<div id="pabstract"> The four HII regions in the Sgr A East complex: A, B, C, and D, represent evidence of recent massive star formation in the central ten parsecs. Using Paschen-alpha images taken with HST and 8.4 GHz VLA data, we construct an extinction map of A-D, and briefly discuss their morphology and location. </div>
<p></p>
<hr><p><a href='http://www.astro.ucla.edu/~ianc/astroph.shtml'>astroph.py v0.41</a>.  Updated 2010/02/12 13:03:49 </p>
</body>
</html>
<? // If check-form _was_ submitted, display this instead:
  } elseif (isset($_POST["submitcheck"])) {
  echo 'Loading article list manager...<br>';
  echo '<META HTTP-EQUIV=Refresh CONTENT="1;'.$listManager.'">';
 
// If submit-form _was_ submitted, display this instead:
} elseif (isset($_POST["submit"])) {
  $minlength = 5;
  echo "<p>You submitted ".$article.".</p>";
 
  if (strlen($article)>$minlength) {
    $f = fopen($paperFile,"a") or die("can't open file: ".$paperFile);
    fwrite($f, "\n".$article);
    fclose($f);
    echo "<p>Your sumission was successfully added to the list. </p>";
    echo "<p>Thanks for advancing knowledge!</p>";
    echo "<p>It may be several minutes before the main page is updated.</p>";
    $str4log = date(DATE_ATOM)."	".$article."	".$ipOfSubmitter;
    $f2 = fopen($logFile,"a") or die("can`t open file: ".$logFile);
    fwrite($f2, $str4log."\n");
    fclose($f2);
    $nullRet = `python runcoffee.py > /dev/null &`;
  } else {
    echo "This is shorter than the minimum valid string length (".$minlength.").";
    echo "Thus your submission was not added to the papers list.";
  }
 
} else {
  echo "you should not have reached this point!";
}
?>
<p><a href="astro_coffee.php">Go back</a> to the main page.</p>
