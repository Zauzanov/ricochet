# Bruter
A multi-threaded web content discovery tool for finding hidden web content using a wordlist + common extensions. Built for security labs and CTF practice.
## 

## 1. Preparations: 
#### 1.2 Download a wordlist for finding resources on a web-app: https://github.com/danielmiessler/SecLists/tree/master/Discovery/Web-Content/File-Extensions-Universal-SVNDigger-Project
#### 1.3 You can use this site to test the code: http://testphp.vulnweb.com/, as it is a part of Acunetix’s intentionally vulnerable demo targets (“vulnweb”) that are publicly provided for security testing and scanner demos. So this specific site is OK to scan for testing. If you want the cleanest option for tests, consider running your own target locally (e.g., OWASP Juice Shop, DVWA, bWAPP) in Docker. I use Metasploitable2 VM. 

## 2. Run: 
```bash
python bruter.py
# or make it less noisy:
python bruter.py 2> /dev/null
```

### Output:
```bash
common
CVS
root
Entries
lang
home.php
setup.php
...
Press return to continue.
sudo python wr01.py 2> /dev/null
[sudo] password for kali: 
Press return to continue.


Success (200): http://192.168.204.129//phpinfo.php
403 => http://192.168.204.129//.htaccess
403 => http://192.168.204.129//.htaccess.inc
403 => http://192.168.204.129//.htaccess.php
403 => http://192.168.204.129//.htaccess.orig
403 => http://192.168.204.129//.htaccess.bak

Success (200): http://192.168.204.129//index/

Success (200): http://192.168.204.129//index.php

Success (200): http://192.168.204.129//index.php

Success (200): http://192.168.204.129//????.txt

Success (200): http://192.168.204.129//????.txt.orig

Success (200): http://192.168.204.129//????.txt.bak

Success (200): http://192.168.204.129//????.txt.php

Success (200): http://192.168.204.129//????.txt.inc

Success (200): http://192.168.204.129//??.txt.php

Success (200): http://192.168.204.129//??.inc

Success (200): http://192.168.204.129//??.orig

Success (200): http://192.168.204.129//??.bak

Success (200): http://192.168.204.129//??.txt

Success (200): http://192.168.204.129//??/

Success (200): http://192.168.204.129//??.txt.inc

Success (200): http://192.168.204.129//??.txt.orig

Success (200): http://192.168.204.129//??.txt.bak

Success (200): http://192.168.204.129//??.php
403 => http://192.168.204.129//.htpasswd
403 => http://192.168.204.129//.htpasswd.inc
403 => http://192.168.204.129//.htpasswd.orig
403 => http://192.168.204.129//.htpasswd.php
403 => http://192.168.204.129//.htpasswd.bak
403 => http://192.168.204.129//cgi-bin/

Success (200): http://192.168.204.129//????.orig

Success (200): http://192.168.204.129//????.bak

Success (200): http://192.168.204.129//????.php

Success (200): http://192.168.204.129//????.inc

Success (200): http://192.168.204.129//????/

Success (200): http://192.168.204.129//dav/
403 => http://192.168.204.129//.htaccess.svn-base
403 => http://192.168.204.129//.htaccess.svn-base.inc
403 => http://192.168.204.129//.htaccess.svn-base.bak
403 => http://192.168.204.129//.htaccess.svn-base.orig
403 => http://192.168.204.129//.htaccess.svn-base.php
403 => http://192.168.204.129//.htaccess.dist.php
403 => http://192.168.204.129//.htaccess.dist.inc
403 => http://192.168.204.129//.htaccess.dist
403 => http://192.168.204.129//.htaccess.dist.orig
403 => http://192.168.204.129//.htaccess.dist.bak
...................................................................................................................................................
Success (200: http://192.168.204.129//dav/).
Success (200): http://192.168.204.129//phpinfo.php..
....................
Success (200): http://192.168.204.129//phpinfo/
..................................................
........................................................................................................................................................................................................
..............................
Success (200: http://192.168.204.129//??.txt.inc)..
.....................................................................
Success (200: http://192.168.204.129//??.php)
.................................................................................................
Success (200: http://192.168.204.129//??.inc)
.....................
Success (200: http://192.168.204.129//??/)
..
Success (200: http://192.168.204.129//??.txt.bak)
.......................................
Success (200: http://192.168.204.129//??.txt.php).
...............
Success (200: http://192.168.204.129//??.orig)
...........................................
Success (200: http://192.168.204.129//??.txt)

Success (200: http://192.168.204.129//??.bak).                  # We have found backup files. 
......................................................................................................
Success (200: http://192.168.204.129//??.txt.orig)
........................................................................................................................................

# Against other test site: 

Success (200: http://testphp.vulnweb.com//CVS/)

Success (200: http://testphp.vulnweb.com//admin/)

Success (200: http://testphp.vulnweb.com//index.php)

Success (200: http://testphp.vulnweb.com//index.bak)

Success (200: http://testphp.vulnweb.com//search.php)

Success (200: http://testphp.vulnweb.com//login.php)

Success (200: http://testphp.vulnweb.com//login.php)

Success (200: http://testphp.vulnweb.com//images/)

Success (200: http://testphp.vulnweb.com//index.php)

Success (200: http://testphp.vulnweb.com//logout.php)

Success (200: http://testphp.vulnweb.com//categories.php)

# Using common.txt wordlist for Web-content discovery:
Success (200): http://192.168.204.129//.bash_history
403 => http://192.168.204.129//.hta
403 => http://192.168.204.129//.hta.php
403 => http://192.168.204.129//.hta.bak
403 => http://192.168.204.129//.hta.inc
403 => http://192.168.204.129//.hta.orig
403 => http://192.168.204.129//.htaccess
403 => http://192.168.204.129//.htaccess.php
403 => http://192.168.204.129//.htaccess.bak
403 => http://192.168.204.129//.htaccess.inc
403 => http://192.168.204.129//.htaccess.orig
403 => http://192.168.204.129//.htpasswd
403 => http://192.168.204.129//.htpasswd.php
403 => http://192.168.204.129//.htpasswd.bak
403 => http://192.168.204.129//.htpasswd.orig
403 => http://192.168.204.129//.htpasswd.inc
403 => http://192.168.204.129//cgi-bin//
403 => http://192.168.204.129//cgi-bin/

Success (200): http://192.168.204.129//dav/

Success (200): http://192.168.204.129//doc/

Success (200): http://192.168.204.129//icons/

Success (200): http://192.168.204.129//index.php

Success (200): http://192.168.204.129//index/

Success (200): http://192.168.204.129//index.php

Success (200): http://192.168.204.129//phpinfo.php

Success (200): http://192.168.204.129//phpinfo/

Success (200): http://192.168.204.129//phpinfo.php

Success (200): http://192.168.204.129//phpMyAdmin/

Success (200): http://192.168.204.129//test/

Success (200): http://192.168.204.129//twiki/


```