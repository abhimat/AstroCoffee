# Astro Coffee 2

Tools for generating and running a website for paper discussions.

Astro Coffee 2 is written by Abhimat Gautam (UCLA). It is based on the original version by Ian J. Crossfield and Nathaniel Ross, and subsequent updates by Ryan T. Hamilton and Fred Davies.

Current To-Dos:
* Use arXiv API to read in information for arXiv papers.
* Convert all arXiv submissions into just IDs, and clean up submissions list afterwards.
* Caching information pulled in for papers, so don't have to re-parse every paper every time page is updated.
* Allowing PDF links for some sites that offer easy to deal with links: e.g., MNRAS, PRL.
* Documentation and tools to allow setting up on independent servers.

Documentation from previous versions below:

---

=============
Introduction:
=============

This distribution are designed to generate a freestanding, maintenance-free web
site for listing arXiv.org files (or other URLs), as seen at
http://astronomy.nmsu.edu/agso/coffee. 

A PHP-enabled web site lists submitted articles, has an input form for
submitting additional articles of interest, and upon submission the site
automatically updates the PHP code. Items can be subsequently deleted from the
list using a password-protected PHP text editor. 

Astroph.py was created at UC Los Angeles by Ian J. Crossfield and Nathaniel
Ross. 

It was then heavily edited by Ryan T. Hamilton at New Mexico State University,
and became this distributed version, available at
https://bitbucket.org/astrobokonon/astrocoffee/ 

Re-use or modification is allowed and encouraged, so long as proper
acknowledgement is made to the original authors and institutions.

Bug reports, suggestions, or just emailing to say that the code has been useful
are all greatly encouraged!

Ryan Hamilton
Astronomy Graduate Student
New Mexico State University
rthamilt@nmsu.edu
https://bitbucket.org/astrobokonon/astrocoffee/overview

=====================================
Installation of the astroph.py Suite:
=====================================

This will hopefully get you up and running with the code.  The instructions are
long.  Sorry.  Please follow along and you should be fine.  If all else fails,
you can email me!  It's likely that there are bugs, and I'll be happy to take a
look and see if the problem is on your end or in the code somewhere that needs
to be fixed.  

This will follow N steps; general requirements, changes to the .py files,
changes to the .php files, additional comments, and debugging hints.
 
=====================
General Requirements:
=====================

1) You need a web server with PHP and Python scripting enabled.  Plenty of web
resources exist to guide you through configuration of your particular web
server.  In addition, you need to have the 'dateutil' module available through
Python.  To check, start Python and type 

import datetime
from dateutil.relativedelta import relativedelta, MO, TU, WE, TH, FR, SA, SU

If either of these give an import error, contact your local system
administrator or check for a different version of Python to run.  It is not
uncommon to have many versions of Python living together on the same server for
compatibility with pyraf and the STSCI Python packages.  

This was built and tested using Python v2.5, v2.6, and v2.7.x; haven't tested
against Python 3.x at all.

2) Contrary to previous versions, BeautifulSoup 4.3.2 is now included.  It's
great.

=========================
Changes to the .py Files:
=========================

The following files should be edited by the user:

./Private/passwords.py
runcoffee.py

runcoffee.py
------------

You should first edit the runcoffee.py file to change the date and time of the
meeting, as well as who gets the error email when something goes wrong.  See
the 'day', 'hour', 'min', and 'responsibles' variables at the top of this file.

'day' is a two letter abbreviation of a weekday, where the abbreviations
(starting with Monday) are MO, TU, WE, TH, FR, SA, SU.  'hour' should be input
in 24h ('military time'), but are converted to the normal US format for display
purposes.

When errors are found, it will send an automated message to those listed in the
'responsibles' variable.  The contents of that message can be found in the file
error.mail.  If you'd like to change who the email appears to be coming from,
then change the 'whosend' variable to what you'd like.  This is the newest
section of the code and could need some adjustments, so bugs are likely.  It
might be necessary to change the 'server' variable to be whatever your mail
(SMTP) server should be.  See the send_error_mail.py file and the python smtp
documentation for more details/help.

If you'd like the ability to comment on each posting, then it is possible using
IntenseDebate.  Please follow these directions, which admitedly may have
changed since I first wrote this section of the code.

   --- Sign up at IntenseDebate.com
   --- Be sure to click the box to use IntenseDebate on my website/blog.  
   --- After verifying your email address, add your website address   
   --- Click on 'Generic Install'  
         All we need from the code is the value of 'var idcomments_acct=', 
   --- In runcoffee.py, change 'idcomments = False' to '= True'
   --- In runcoffee.py replace YOURHASHGOESHERE with that value and comment 
         out the line 'idcomments=False' line.  
         *** Be sure you have the single quote ticks (\') properly escaped ***
   --- At the top of the IntenseDebate page goto 'Sites', clicking on your 
         newly setup website, and then in the 'Settings->Misc' section 
   --- Set your comment location to 'Frontpage'.  

Then you can customize to your heart's content, including adding Facebook
Connect and logging in via OpenID and Twitter as well.

passwords.py
------------

One should change the username, password, and salt variables in the
passwords.py file in the ./Private directory, run it, and then copy and paste
the output into the listmanager.php file.  This insures a bit more security
than having the username and password in plaintext in the listmanager.php file,
though the salt is there for any enterprising young hacker.  

==========================
Changes to the .php Files:
==========================

The following files should be edited by the user:

index.php
listmanager.php

1) See the passwords.py section above and make the necessary changes in
listmanager.php

2) Determine the path to your python executable and set the $python variable in
both index.php and listmanager.php to point towards it.  This also allows you
to specify a particular version if multiple exist.  Typically the full path is
required, though not always.  If in doubt, ask your sysadmin.  Incorrect or
non-functional versions of this will cause the code to fail, silently.

3) Change your timezone in the index.php and listmanager.php files to match
your own.  The format for the timezone string can be found at the link in the
php file or be found via the googles.

4) You'll need to change the affiliation to your own institution/group in the
following files:

./index.php
./archive_top.php
./archive_bottom.php
./useful.links
./general.links

You can change the CSS to your own needs on your own time, if you're setting
this up you probably know more than enough to change the weather links and
insert a calendar or whatever else you need to do.  You can add in your own
customizations by changing the contents of the sidebars in the index.php file.
See <h2>Weather Checks</h2>, <h2>Useful Links</h2>, <h2>General Links</h2>, and
<h2>Calendar</h2> sections.  

Be careful to mind the <div> tags when adding/changing things since and
extra/missing ones will cause the page to look like crap and the CSS to go
nuts.

You probably can use a different CSS sheet, though I don't guarantee that it
will work very well without editing astroph.py to close the correct <div>'s.
Your Milage May Vary.

============
Final Steps:
============

1) Once you have everything the way you'd like it to be, execute the Perms.sh
file to make sure the permissions are set as they should.  It will attempt to
set the permissions necessary for you, but you should double check to see if
the choices make sense.  

The *.php files, papers, and dregs.log will all be continually updated, and so
need to have at least write access enabled.  You will want to update the *.txt
files to customize your page, but after that they only need read access
enabled, as do the *.py files.  ./Archive needs full read/write access as well.

Permission errors will cause the scripts to fail silently and not update
anything.

2) To control access and try to prevent spam, determine your CIDR address range
and change the htaccess file to match.  This will give a 403 Forbidden error to
any address not in the CIDR range, and is a quick and easy way to prevent spam
bots from polluting the page.  You can also add specific IPs to allow, though
this is a bit difficult unless you have known/static IP addresses.  

The htaccess file included in the tarball is an example of what I use.  IF YOU
CHOOSE TO USE THIS FEATURE, rename 'htaccess' to '.htaccess' after you
determine your CIDR range.

================
Debugging Hints:
================

At this point, everything should be set up.  Point your webbrowser towards
where you set things up, and try a valid submission.  Wait a (few) minutes and
refresh the page, and it all is well then you should be good to go!

If things have not updated, there are a few things to try:

   --- Check the directions again, making sure you have not missed any steps :)
   --- Check the file permissions.  Incorrect file permissions will cause the 
         code to fail silently.
   --- Check your python path/executable.  Incorrect values/versions will cause 
         the code to fail silently.
   --- Attempt to run the code as a (normal non-root) user.  In the directory, 
         'touch papers; python runcoffee.py' 
         and check for any exceptions/errors.
   --- Email me or ask your local computer or *nix guru for help

status.log and dregs.log can be very useful to see what's going on with the
code and should (hopefully) let you see how far things have progressed before
dying on you.

If all else fails, you can email me!  It's likely that there are bugs, and I'll
be happy to take a look and see if the problem is on your end or in the code
somewhere that needs to be fixed.  Bug reports, suggestions, or just emailing
to say that the code has been useful are all greatly encouraged!

Ryan Hamilton
Visiting PostDoctoral Scientist
SOFIA-USRA
astrobokonon@gmail.com
https://bitbucket.org/astrobokonon/astrocoffee/overview
