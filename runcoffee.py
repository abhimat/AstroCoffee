#!/usr/bin/env python

import sys
import astroph, shutil, time, datetime, os, re, send_error_mail
from dateutil.relativedelta import relativedelta, MO, TU, WE, TH, FR, SA, SU

# Change this to control the next meeting date & time
day=FR
hour=11
min=00

# Change this to send the error emails to the appropriate people
#   IT MUST BE A LIST, SO KEEP THE [ ] 
responsibles = ["abhimat@astro.ucla.edu"]

# Change this to your Intense Debate ID hash, or False to disable the comments
idcomments = False

# Initialize variables
paper_file = 'papers'
paper_discussed_file = 'papers_discussed'
paper_next_file = 'papers_next'
paper_volunteers_file = 'papers_volunteers'
main_file = 'astro_coffee.php'
temp_file = 'astro_coffee_temp.php'
stat_log = 'status.log'
# For emergency email reporting; Doesn't need to be changed
whosend = 'Automated_Astro_Coffee_Coding_Monkey@InsideTheServer.org' 

# Change this to wherever your mail server lives at your location if it doesn't
#   work...localhost should work since webservers usually mailservers too
server = 'localhost'

# Count the number of lines for the time to completion estimate
f=open(paper_file,'r')
for i, l in enumerate(f):
    pass
f.close()
nlines = i + 1

napTime = 4  # time, in seconds, to wait between web queries
# timecomp = napTime * nlines
# testimate = datetime.timedelta(seconds=timecomp)

# Check last-modified times:
paper_time = shutil.os.path.getmtime(paper_file)
paper_discussed_time = shutil.os.path.getmtime(paper_discussed_file)
paper_next_time = shutil.os.path.getmtime(paper_next_file)
web_time = shutil.os.path.getmtime(main_file)

# If list was updated, run the script!
if paper_time > web_time or paper_discussed_time > web_time or paper_next_time > web_time:
    before = datetime.datetime.now()
    (html, output) = astroph.docoffeepage(paper_file, paper_discussed_file, paper_next_file, paper_volunteers_file, temp_file, day, hour, min, sleep=napTime, idid=idcomments, php=True)
    # print html
    #     f = open(temp_file, 'w')
    #     for line in html:
    #         print line
    #         f.write(line)
    #     f.close()
    print output
    after = datetime.datetime.now()
    tdiff = after-before

    try:
        os.remove(stat_log)
    except:
        # Previous status log didn't exist for some reason
        #   so just keep on truckin'
        pass

    try:
        f=open(stat_log,'w')
        f.write(output)
        # f.write("\nRequest estimated at " + str(testimate) + "\n")
        # f.write("Request completed in " + str(tdiff) + "\n\n")
        f.close()
    except: 
        pass

    f=open(stat_log,'a')
    f.write("Attempting to move temp. PHP to main PHP...")
    try:
        shutil.move(temp_file, main_file)
        f.write("Success!\n")
    except Exception, why:
        f.write("Error encountered during the move process: \n")
        f.write(str(why) + "\n")
    f.close()

# Now check for any reported Errors
que = ''
matches = []
errflag=False
f = open(stat_log,'r')
for line in f.readlines():
    if line.startswith("ERRORS "):
        matches.append(line)
        errflag=True
f.close()

f=open(stat_log,'a')
f.write("\n")
f.write("Error Encountered During Reading of Sources: " + str(errflag) + "\n")

if errflag:
    try:
        f.write("Attempting to send an error email...\n")
        que=send_error_mail.send_error_mail("error.mail", responsibles, \
                                             matches, whosend, server)
        f.write("Sent Error Email Successfully!")
    except: 
        f.write("Unexpected error:" + str(sys.exc_info()[0]) + "\n")
        f.write("Warning: Could Not send the Error Mail Message :(\n")
        f.write("Mailserver replied: " + str(que))

f.close()
