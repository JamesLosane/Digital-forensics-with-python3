# os,json,urllib2 module

import os
import time
import json
import urllib2
import pyfiglet

# Banner

banner = pyfiglet.figlet_format("Identify VPN IP", font="slant")
print(banner)


print ("                        Author : ishDante")
print ("                        Github : https://github.com/Sima456")
print
#  Input
vpn_ip=raw_input('Enter a ip address :')

# While True Loop

while True:

    # api

    api='https://ipinfo.io/'
    r=urllib2.urlopen(api+vpn_ip)
    d=r.read()
    v=json.loads(d)

    # date 

    date = time.strftime("%d-%m-%y")
    

    print ("DATE               : "  +      date)
    print ("IP                 : "  +   v ['ip'])
    print ("COUNTRY            : "  +   v ['country'])
    print ("CITY               : "  +   v ['city'])
    print ("VPN SERVER         : "  +   v ['hostname']+"  <==== It is a vpn ip address.")
    
    break
