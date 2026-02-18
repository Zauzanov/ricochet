# Bruter

## 1. Preparations: 
#### 1.2 Download a wordlist for finding resources on a web-app: https://github.com/danielmiessler/SecLists/tree/master/Discovery/Web-Content/File-Extensions-Universal-SVNDigger-Project
#### 1.3 You can use this site to test the code: http://testphp.vulnweb.com/, as it is a part of Acunetix’s intentionally vulnerable demo targets (“vulnweb”) that are publicly provided for security testing and scanner demos. So this specific site is OK to scan for testing. If you want the cleanest option for tests, consider running your own target locally (e.g., OWASP Juice Shop, DVWA, bWAPP) in Docker. I use Metasploitable2 VM. 

## 2. Run: 
```bash
python bruter.py
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
...................................................................................................................................................
Success (200: http://192.168.204.129//dav/).
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

Success (200: http://192.168.204.129//??.bak).                  # We have found backup files and so on. 
......................................................................................................
Success (200: http://192.168.204.129//??.txt.orig)
........................................................................................................................................
```