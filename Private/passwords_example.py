#!/usr/bin/python

import hashlib

username = "astro_coffee"
password = "robustPassword_goesHere"
salt     = "!@#$%^&"

u = hashlib.md5()
u.update(username)
u.update(salt)
usrmd5 = u.hexdigest()

p = hashlib.md5()
p.update(password)
p.update(salt)
pasmd5 = p.hexdigest()

print "$username = \"" + usrmd5 + "\";"
print "$password = \"" + pasmd5 + "\";"
print "$salt     = \"" + salt + "\";"
