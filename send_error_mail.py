def send_error_mail(email_file, people, badlines, fromaddr, server="localhost"):

    # Emailing from Python
    import smtplib
    from email.MIMEText import MIMEText

    # Read in the error email file
    f = open(email_file, "r")
    body = f.read()
    f.close()

    body = body + "=====\nOffending entry/entries:\n"
    body = body + ''.join(badlines)

    # Set up a MIMEText object (it's a dictionary)
    msg = MIMEText(body)

    # You can use add_header or set headers directly ...
    msg['Subject'] = "AstroCoffee Submission Error Notification"
    # Following headers are useful to show the email correctly
    # in your recipient's email box, and to avoid being marked
    # as spam. They are NOT essential to the snemail call later
    msg['From'] = fromaddr
    msg['Reply-to'] = ""

    # Establish an SMTP object and connect to your mail server
    s = smtplib.SMTP()
    s.connect(server)
    # Send the email - real from, real to, extra headers and content ...
    mailresult = s.sendmail(fromaddr, people, msg.as_string())

    s.close()

    return mailresult
