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
<head>
	<title>Astro Coffee Papers List Handler</title>
	<!-- Google Web Fonts -->
	<link href='https://fonts.googleapis.com/css?family=Source+Sans+Pro:400,600,700,900,400italic,600italic,700italic,900italic' rel='stylesheet' type='text/css'>
	<link href='https://fonts.googleapis.com/css?family=Bree+Serif' rel='stylesheet' type='text/css'>
	<link href='https://fonts.googleapis.com/css?family=Montserrat:400,700' rel='stylesheet' type='text/css'>
	
	<!-- Styles -->
	<link rel="stylesheet" href="./styles.css" type="text/css" media="screen" />
</head>

<body>

<?php
$paperFile_next = 'papers_next';
$paperFile = 'papers';
$paperFile_discussed = 'papers_discussed';
$paperFile_volunteers = 'papers_volunteers';

$fp_next = @fopen($paperFile_next, "r");
$fp = @fopen($paperFile, "r");
$fp_discussed = @fopen($paperFile_discussed, "r");
$fp_volunteers = @fopen($paperFile_volunteers, "r");

$loadcontent_next = fread($fp_next, filesize($paperFile_next));
$loadcontent = fread($fp, filesize($paperFile));
$loadcontent_discussed = fread($fp_discussed, filesize($paperFile_discussed));
$loadcontent_volunteers = fread($fp_volunteers, filesize($paperFile_volunteers));


$lines_next = file($paperFile_next) or die("can`t open file: ".$paperFile_next." for reading");
$count_next = count($lines_next);
$loadcontent_next = htmlspecialchars($loadcontent_next);
fclose($fp_next);

$lines = file($paperFile) or die("can`t open file: ".$paperFile." for reading");
$count = count($lines);
$loadcontent = htmlspecialchars($loadcontent);
fclose($fp);

$lines_discussed = file($paperFile_discussed) or die("can`t open file: ".$paperFile_discussed." for reading");
$count_discussed = count($lines_discussed);
$loadcontent_discussed = htmlspecialchars($loadcontent_discussed);
fclose($fp_discussed);

$lines_volunteers = file($paperFile_volunteers) or die("can`t open file: ".$paperFile_volunteers." for reading");
$count_volunteers = count($lines_volunteers);
$loadcontent_volunteers = htmlspecialchars($loadcontent_volunteers);
fclose($fp_volunteers);
?>


<h2>Astro-coffee article list handler</h2>
Current contents of the papers and discussed papers lists:
  <form name="form" method="post" action="<?php echo $_SERVER['php_SELF'];?>">
	<p>Papers added this week (papers_next)</p>
	<textarea style="text-align: left; padding: 0px; overflow: auto; border: 3px groove; font-size: 12px" name="savecontent_next" cols="80" rows="<?=($count_next+3);?>" wrap="OFF"><?=$loadcontent_next?></textarea>
	<p>Papers added last week (papers)</p>
	<textarea style="text-align: left; padding: 0px; overflow: auto; border: 3px groove; font-size: 12px" name="savecontent" cols="80" rows="<?=($count+3);?>" wrap="OFF"><?=$loadcontent?></textarea>
	<p>Papers already discussed (papers_discussed)</p>
	<textarea style="text-align: left; padding: 0px; overflow: auto; border: 3px groove; font-size: 12px" name="savecontent_discussed" cols="80" rows="<?=($count_discussed+3);?>" wrap="OFF"><?=$loadcontent_discussed?></textarea>
	<p>Volunteers for papers</p>
	<textarea style="text-align: left; padding: 0px; overflow: auto; border: 3px groove; font-size: 12px" name="savecontent_volunteers" cols="80" rows="<?=($count_volunteers+3);?>" wrap="OFF"><?=$loadcontent_volunteers?></textarea>
    <hr><br>
    Username: <input type="text" name="txtUsername" />
    Password: <input type="password" name="txtPassword" />
    <input type="submit" name="save_file" value="submit and save">

  </form>
  <br>
<?php
function trim_value(&$value) 
{ 
    $value = trim($value); 
}
?>

<?php
  if (!isset($_POST['save_file'])) {
    print "<p>Use this to clean out old entries from the database.  ";
    print "Edit the files as you see fit, and enter the appropriate ";
    print "username and password.</p><p>Then, click 'submit and save.'</p>";
    print "<p>Return to the <a href='./'>main page</a></p>";
  }

elseif (((md5($_POST['txtUsername'].$salt)==$username and md5($_POST['txtPassword'].$salt)== $password)) and (isset($_POST['save_file']))) { 
    if (isset($_POST["save_file"])){
        // echo '<p>The new contents are:</p>';
		
		$contents_next = explode("\n",$_POST["savecontent_next"]);
        $contents = explode("\n",$_POST["savecontent"]);
		$contents_discussed = explode("\n",$_POST["savecontent_discussed"]);
        $contents_volunteers = explode("\n",$_POST["savecontent_volunteers"]);
        
		# papers_next file
        // echo "<p>Papers added this week (papers_next)</p>";
		array_walk($contents_next, 'trim_value');
        $i=0;
        foreach ($contents_next as $con){
            // echo $con."<br>";
            if (preg_match("/[^A-Za-z0-9\:\.\/\?\_\#\-\=]/", $con))
            {
            	echo "<p><strong>Your submission contains invalid characters!</strong></p>";
            	echo "<p>If you think this is an error, tell the coffee website manager.</p>";
                echo '<META HTTP-EQUIV=Refresh CONTENT="10">';
              die;
            }
                      
            $contents_next["$i"] = trim($con);
            $i=$i+1;
        }
        if (count(array_unique($contents_next)) < count($contents_next)){
            echo "<p>WARNING: Duplicate entries exist!<br></p>";
        }
        $fp2 = @fopen($paperFile_next, "w") or die("can`t open file: ".$paperFile_next); 
        if (count($contents_next) == 1 and trim($contents_next[0]=="")){
            fwrite($fp2, "\n");
        }
        else{
            fwrite($fp2, $_POST["savecontent_next"]);
        }
        $nullRet = `$python runcoffee.py > /dev/null &`;
        fclose($fp2);
        $loadcontent_next = $_POST["savecontent_next"];
		
		# papers file
        // echo "<p>Papers added last week (papers)</p>";
		array_walk($contents, 'trim_value');
        $i=0;
        foreach ($contents as $con){
            // echo $con."<br>";
            if (preg_match("/[^A-Za-z0-9\:\.\/\?\_\#\-\=]/", $con))
            {
            	echo "<p><strong>Your submission contains invalid characters!</strong></p>";
            	echo "<p>If you think this is an error, tell the coffee website manager.</p>";
                echo '<META HTTP-EQUIV=Refresh CONTENT="10">';
              die;
            }
            
            $contents["$i"] = trim($con);
            $i=$i+1;
        }
        if (count(array_unique($contents)) < count($contents)){
            echo "<p>WARNING: Duplicate entries exist!<br></p>";
        }
        $fp2 = @fopen($paperFile, "w") or die("can`t open file: ".$paperFile); 
        if (count($contents) == 1 and trim($contents[0]=="")){
            fwrite($fp2, "\n");
        }
        else{
            fwrite($fp2, $_POST["savecontent"]);
        }
        $nullRet = `$python runcoffee.py > /dev/null &`;
        fclose($fp2);
        $loadcontent = $_POST["savecontent"];
		
		# papers_discussed file
        // echo "<p>Papers already discussed (papers_discussed)</p>";
        array_walk($contents_discussed, 'trim_value');
        $i=0;
        foreach ($contents_discussed as $con){
            // echo $con."<br>";
            if (preg_match("/[^A-Za-z0-9\:\.\/\?\_\#\-\=]/", $con))
            {
                echo "<p><strong>Your submission contains invalid characters!</strong></p>";
                echo "<p>If you think this is an error, tell the coffee website manager.</p>";
                echo '<META HTTP-EQUIV=Refresh CONTENT="10">';
                die;
            }
            $contents_discussed["$i"] = trim($con);
            $i=$i+1;
        }
        if (count(array_unique($contents_discussed)) < count($contents_discussed)){
            echo "<p>WARNING: Duplicate entries exist!<br></p>";
        }
        $fp2 = @fopen($paperFile_discussed, "w") or die("can`t open file: ".$paperFile_discussed); 
        if (count($contents_discussed) == 1 and trim($contents_discussed[0]=="")){
            fwrite($fp2, "\n");
        }
        else{
            fwrite($fp2, $_POST["savecontent_discussed"]);
        }
        $nullRet = `$python runcoffee.py > /dev/null &`;
        fclose($fp2);
        $loadcontent_discussed = $_POST["savecontent_discussed"];
        
		# papers_volunteers file
        // echo "<p>Volunteers for papers (papers_volunteers)</p>";
		array_walk($contents_volunteers, 'trim_value');
        $i=0;
        foreach ($contents_volunteers as $con){
            // echo $con."<br>";
            if (preg_match("/[^A-Za-z0-9\:\.\/\?\_\#\-\=]/", $con))
            {
                echo "<p><strong>Your submission contains invalid characters!</strong></p>";
                echo "<p>If you think this is an error, tell the coffee website manager.</p>";
                echo '<META HTTP-EQUIV=Refresh CONTENT="10">';
                die;
            }
            $contents_volunteers["$i"] = trim($con);
            $i=$i+1;
        }
        if (count(array_unique($contents_volunteers)) < count($contents_volunteers)){
            echo "<p>WARNING: Duplicate entries exist!<br></p>";
        }
        $fp2 = @fopen($paperFile_volunteers, "w") or die("can`t open file: ".$paperFile_volunteers); 
        if (count($contents_volunteers) == 1 and trim($contents_volunteers[0]=="")){
            fwrite($fp2, "\n");
        }
        else{
            fwrite($fp2, $_POST["savecontent_volunteers"]);
        }
        $nullRet = `$python runcoffee.py > /dev/null &`;
        fclose($fp2);
        $loadcontent_volunteers = $_POST["savecontent_volunteers"];
		
        # Get estimate of run time for the user
        $numlines = count(file($paperFile_next)) + count(file($paperFile));
        $time  = $numlines * 10;
        echo "<p>It may be several minutes before the main page updates.</p>";
        echo "<p>Return to the <a href='./'>main page</a></p>";

        // # Testing for duplicates
        // foreach ($lines as $pap){
        //     if (trim($article) == trim($pap)) {
        //         echo '<p>Duplicate in list is found!</p>';
        //         echo '<p>Are you sure you know what you\'re doing?</p>';
        //     }
        // }
        echo '<META HTTP-EQUIV=Refresh CONTENT="10">';
    }
}
else{
    echo "<p>You didn't enter the correct username/password.<br>";
    echo "Reloading the page in 5 seconds, to let ";
    echo 'you try again... </p>';
    echo '<META HTTP-EQUIV=Refresh CONTENT="5">';
}
?>
</body>
</html> 
