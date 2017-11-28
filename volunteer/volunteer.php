<!DOCTYPE html>
<!--
 
    UCLA Astro Coffee Volunteer Sign Up
	by Abhimat Gautam	
	
	Volunteer sign up called by following syntax:
	http://coffee.astro.ucla.edu/volunteer/volunteer.php?ID=[ID]
  
-->

<html>
<head>
	<title>Astro Coffee Volunteer Sign Up</title>
	<!-- Google Web Fonts -->
	<link href='http://fonts.googleapis.com/css?family=Source+Sans+Pro:400,600,700,900,400italic,600italic,700italic,900italic' rel='stylesheet' type='text/css'>
	<link href='http://fonts.googleapis.com/css?family=Bree+Serif' rel='stylesheet' type='text/css'>
	<link href='http://fonts.googleapis.com/css?family=Montserrat:400,700' rel='stylesheet' type='text/css'>
	
	<!-- Styles -->
	<link rel="stylesheet" href="../styles.css" type="text/css" media="screen" />
</head>

<body>
    <h2>Volunteer to discuss a paper</h2>

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

        $paperFile_volunteer = '../papers_volunteers';

        $logFile = "../dregs.log";
        $listManager = "../listmanager.php";
        // $ID = $_POST["article"];
        $ipOfSubmitter=$_SERVER["REMOTE_ADDR"];

        $minlength = 2;
        echo "<p>Paper to volunteer for: ".$ID."</p>";
    ?>

    <form name="form" method="post" action="<?php echo $_SERVER['php_SELF'];?>">
        Your name: <input type="text" name="volunteer_name" />
        <input type="submit" name="save_volunteer" value="Submit">
    </form>

    <br>
    
    <?php
        if (isset($_POST["save_volunteer"])){
            $volunteer_name = $_POST['volunteer_name'];
            
            // Check for invalid characters
            if (preg_match("/[^A-Za-z0-9]/", $volunteer_name) or preg_match("/[^A-Za-z0-9\:\.\/]/", $ID)) {
                echo '<META HTTP-EQUIV=Refresh CONTENT="10;url=../">';

                echo '<p><strong>But the paper ID or your name contains invalid characters!</strong></p>';
                echo '<p>If you think this is an error, tell the coffee website manager.</p>';
                echo "<p>You will be returned to the main page in 10 seconds.</p>";
                die;
            }
            
            if (strlen($ID)>$minlength and strlen($volunteer_name)>$minlength) {
            	$f = fopen($paperFile_volunteer,"a") or die("can't open file: ".$paperFile_volunteer);
            	fwrite($f, "\n".trim($ID));
                fwrite($f, "\n".trim($volunteer_name));
            	fclose($f);
            	
                echo '<META HTTP-EQUIV=Refresh CONTENT="10;url=../">';
                
            	echo "<p>You were successfully added as a volunteer.</p>";
            	echo "<p>It may be several minutes before the main page is updated.</p>";
            	echo "<p>You will be returned to the main page in 10 seconds.</p>";
            	$str4log = date('D, d M Y H:i:s')."    ".$ID."    ".$volunteer_name." (".$ipOfSubmitter.") added as volunteer.";
            	$f2 = fopen($logFile,"a") or die("can`t open file: ".$logFile);
            	fwrite($f2, $str4log."\n");
            	fclose($f2);
            } else {
            	echo "<p>The paper ID or your name is shorter than the minimum valid length (".$minlength.").</p>";
            	echo "<p>Thus your submission was not added to the volunteer list.</p>";
            }
        }
    ?>
    
    <p>Return to the <a href='../'>main page</a></p>