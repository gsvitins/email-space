#!/usr/bin/env python2.7
# Displays size of dovecot mailboxes
# Usage: ./email-space.py > mail.txt

import os,subprocess

# Change 'maildir' to your own
maildir = '/usr/local/virtual'

data = []

print '\nCalculating disk space. This might take some time.\n'

# resize 'df -hs' output to show size in GB·
def resize_gb(nr):
    nr = nr.replace(',', '.')
    if nr[-1] == 'K':
        gnr = float(nr[:-1]) / 1000000
    elif nr[-1] == 'M':
        gnr = float(nr[:-1]) / 1000
    else:
        gnr = float(nr[:-1])
    return gnr 

# check if provided maildir path has '/' at the end of it
if maildir[-1] == '/':
    slash = ''
else:
    slash = '/' 

# check, format and put dir size in 'data' list
for d in os.listdir(maildir):
    for u in os.listdir(maildir + slash + d): 
        space = subprocess.check_output(['du','-hs', maildir + slash + d + '/' + u]) 
        space = space[:space.rfind('\t')]
        space = resize_gb(space)
        email = u + '@' + d 
        data.append([email, space])

# sort data list by highest number
data = sorted(data, key = lambda x: x[1], reverse = True)

for i in data:
    print "%-*s %.2fG" % (40, i[0], i[1])
