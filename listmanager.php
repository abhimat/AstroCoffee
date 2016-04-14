<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" 
"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">

<?php

// SET THE PATH TO YOUR PYTHON VERSION HERE
// $python = '/usr/bin/python';
$python = '/Users/abhimat/software/Ureka/variants/common/bin/python';

// CHOOSE YOUR TIMEZONE FROM THE LINK BELOW AND SET IT HERE
$CurrentVer = phpversion();
if(version_compare($CurrentVer, '5.1.0')>=0) {
    date_default_timezone_set('US/Pacific');
    #http://www.php.net/manual/en/timezones.others.php
}

// CHANGE THESE TO THE OUTPUT FROM THE passwords.py FILE IN ./Private
$username = "0d3c8122f02bf17ae3f09835b6604329";
$password = "b1f9aecb27fc571e73084b61ce0d8138";
$salt     = "!@#$%^&";

?>

<html>
<head><title>Astro-coffee article list handler</title>
<meta name="keywords" content="astro-ph, arxiv, astronomy, nmsu, coffee" />
<meta name="author" content="NMSU Astronomy" />
<link rel="stylesheet" type="text/css" href="style.css" />
</head>

<body>

<?php
$paperFile = 'papers';
$paperFile_discussed = 'papers_discussed';

$fp = @fopen($paperFile, "r");
$fp_discussed = @fopen($paperFile_discussed, "r");

$loadcontent = fread($fp, filesize($paperFile)); 
$loadcontent_discussed = fread($fp_discussed, filesize($paperFile_discussed)); 

$lines = file($paperFile) or die("can`t open file: ".$paperFile." for reading");
$count = count($lines);
$loadcontent = htmlspecialchars($loadcontent);
fclose($fp);

$lines_discussed = file($paperFile_discussed) or die("can`t open file: ".$paperFile_discussed." for reading");
$count_discussed = count($lines_discussed);
$loadcontent_discussed = htmlspecialchars($loadcontent_discussed);
fclose($fp_discussed);
?>


<h2>Astro-coffee article list handler  </h2>

Current contents of the article list file:

  <form name="form" method="post" action="<?php echo $_SERVER['php_SELF'];?>">
    <textarea style="text-align: left; padding: 0px; overflow: auto; border: 3px groove; font-size: 12px" name="savecontent" cols="80" rows="<?=($count+3);?>" wrap="OFF"><?=$loadcontent?></textarea>
	<textarea style="text-align: left; padding: 0px; overflow: auto; border: 3px groove; font-size: 12px" name="savecontent" cols="80" rows="<?=($count_discussed+3);?>" wrap="OFF"><?=$loadcontent_discussed?></textarea>
    <br>
    Username: <input type="text" name="txtUsername" />
    Password: <input type="password" name="txtPassword" />
    <input type="submit" name="save_file" value="submit and save">

  </form>
  <br><hr>
<?php
function trim_value(&$value) 
{ 
    $value = trim($value); 
}
?>

<?php
  if (!isset($_POST['save_file'])) {
    print "<p>Use this to clean out old entries from the database.  ";
    print "Edit the file as you see fit, and enter the appropriate ";
    print "username and password.</p><p>Then, click 'submit and save.'</p>";
    print "<p>Return to the <a href='./'>main page</a></p>";
  }

elseif (((md5($_POST['txtUsername'].$salt)==$username and md5($_POST['txtPassword'].$salt)== $password)) and (isset($_POST['save_file']))) { 
    if (isset($_POST["save_file"])){
        echo '<p>The new contents are:</p>';
        $contents = explode("\n",$_POST["savecontent"]);
        array_walk($contents, 'trim_value');
        $i=0;
        foreach ($contents as $con){
            echo $con."<br>";
            $contents["$i"] = trim($con);
            $i=$i+1;
        }
        if (count(array_unique($contents)) < count($contents)){
            echo "<p>WARNING: Duplicate entries exist!<br></p>";
        }
        $fp2 = @fopen($paperFile, "w") or die("can`t open file: ".$paperFile); 
        if (count($contents) == 1 and trim($contents[0]=="")){
            fwrite($fp2, "http://astronomy.nmsu.edu/rthamilt/codes/astrocoffee/");
            echo "You can't leave this blank!  Paper file autofilled...";
        }
        else{
            fwrite($fp2, $_POST["savecontent"]);
        }
        $nullRet = `$python runcoffee.py > /dev/null &`;
        fclose($fp2);
        $loadcontent = $_POST["savecontent"];

        # Get estimate of run time for the user
        $numlines = count(file($paperFile));
        $time  = $numlines * 10;
        echo "<p>It may be several minutes before the main page updates.</p>";
        echo "<p>$numlines items to update, so >$time seconds to finish.</p>";

        # Testing for duplicates
        foreach ($lines as $pap){
            if (trim($article) == trim($pap)) {
                echo '<p>Duplicate in list is found!</p>';
                echo '<p>Are you sure you know what you\'re doing?</p>';
            }
        }  
        echo '<META HTTP-EQUIV=Refresh CONTENT="10">';
    }
}
else{
    echo "<h3>No way, dude(tte).</h3>";
    echo "<p>You didn't enter the correct username/password!<br>";
    echo "Reloading the page in 5 seconds, to let ";
    echo 'you try again... </p>';
    echo '<META HTTP-EQUIV=Refresh CONTENT="5">';
}
?>
</body>
</html> 
