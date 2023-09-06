<!DOCTYPE html>
<!--
 
    UCLA Astro Coffee Page, by Abhimat Gautam
	based on previous versions by Ryan T. Hamilton, Ian J. Crossfield, and Nathaniel Ross
  
-->
<html lang="en">
<head>
	<meta charset="UTF-8">
	<title>UCLA Astro Coffee: Bookmarklet</title>
	
	<!-- Google Web Fonts -->
	<link href='https://fonts.googleapis.com/css?family=Source+Sans+Pro:400,600,700,900,400italic,600italic,700italic,900italic' rel='stylesheet' type='text/css'>
	<link href='https://fonts.googleapis.com/css?family=Bree+Serif' rel='stylesheet' type='text/css'>
	<link href='https://fonts.googleapis.com/css?family=Montserrat:400,700' rel='stylesheet' type='text/css'>
	
	<meta name=viewport content='width=device-width, initial-scale=1'>
	
	<!--[if lt IE 9]>
		<script src="http://html5shim.googlecode.com/svn/trunk/html5.js"></script>
	<![endif]-->
	
	<!-- Favicon -->
	<link rel="shortcut icon" href="../images/favicon.png">
	<link rel="apple-touch-icon" href="../images/touch-icon.png">
	
	<!-- Styles -->
	<link rel="stylesheet" href="../styles.css" type="text/css" media="screen" />
	
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
		<a href="../"><picture>
      <source srcset="../images/Header-Dark_1x.png 1x, ../images/Header-Dark_2x.png 2x" media="(prefers-color-scheme: dark)">
      <img src="../images/Header_2x.png" srcset="../images/Header_1x.png 1x, ../images/Header_2x.png 2x" alt="Astro Coffee" />
    </picture></a>
		
		<center><ul class="pages">
			<li><a href="../">Current Articles</a></li>
			<li><a href="../archive/">Archive</a></li>
			<li><a href="../usefullinks/">Useful Links</a></li>
		</ul></center>
		
	</header>
	
	<div class="content wrap">
		<section class="blocks">
			<article class="block">
				<h2>Bookmarklet</h2>
				<center><a class="large semibold" href="javascript:(function(){location.href='http://coffee.astro.ucla.edu/bookmarker.php?article='+encodeURIComponent(location.href);})();">Add to Astro Coffee</a></center>
				<p>Drag the above “Add to Astro Coffee” link to your browser’s bookmarks bar to set up the bookmarklet. Clicking the bookmarklet on a paper’s page will add the paper to the Astro Coffee page. Nifty and convenient, right?</p>
                <p>On iOS and use the <a href="https://support.apple.com/guide/shortcuts/welcome/ios">Shortcuts app</a>? Grab the <a href="https://www.icloud.com/shortcuts/4adcb3a066a8470d8449452ed05e0ad9">Add to Astro Coffee shortcut</a> to make adding papers to Astro Coffee even faster and easier through the share sheet menus!</p>
			</article>
			<img src="../images/HappyPaper_2x.png" srcset="../images/HappyPaper_1x.png 1x, ../images/HappyPaper_2x.png 2x" alt="Happy Paper!"/>
		</section> <!-- /blocks -->
	</div> <!-- /content -->

	<footer class="small wrap">
		<center><p class="small"><strong>Astro Coffee 2</strong><br>by <a href="http://astro.ucla.edu/~abhimat/">Abhimat Gautam</a></p></center>
		<center><p class="small"><a href="https://github.com/abhimat/AstroCoffee">Contribute on GitHub!</a></p></center>
	</footer>
</body>
</html>
