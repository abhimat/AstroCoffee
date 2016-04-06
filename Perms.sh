#!/bin/bash
# 2010-04-02 RTH: Created
#
# Set read-only permissions for most of the important coffee files so we 
#   don't bork anything up...
# a - all users
# u - current user/owner
# o - other users
# g - other users in group
# r - read
# w - write
# x - execute

chmod a+rwx ./archive .
chmod a+rw dregs.log status.log astro_coffee.php bs4
chmod a+rw papers ./archive/index.php archive_bottom.php archive_top.php
chmod a-wx listmanager.php runcoffee.py coffee_submit.php
chmod a-w index.php
chmod og-rwx ./Private
chmod og-r php_info.php
chmod og-r dregs.log
