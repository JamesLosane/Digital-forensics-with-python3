import sqlite3
import json
import datetime
import pytz
import re
import argparse
import csv

print ("""
   ▄████████  ▄█   ▄██████▄  ███▄▄▄▄   
  ███    ███ ███  ███    ███ ███▀▀▀██▄ 
  ███    ███ ███▌ ███    ███ ███   ███ 
  ███    ███ ███▌ ███    ███ ███   ███ 
▀███████████ ███▌ ███    ███ ███   ███ 
  ███    ███ ███  ███    ███ ███   ███ 
  ███    ███ ███  ███    ███ ███   ███ 
  ███    █▀  █▀    ▀██████▀   ▀█   █▀   

  Windows 10 Timeline Activity Parser                                       
                                       """)

parser = argparse.ArgumentParser()
parser.add_argument("f", type=str, help="ActivitiesCache file")
parser.add_argument("dbtz",  type=str, help="Timezone of examined system")
parser.add_argument("-o", "--output", type=str, help="CSV filename to extract the raw database")
args = parser.parse_args()

acdb = args.f
dbtimezone = args.dbtz
output_file = args.output

def timecon(trow,timestamp,timezone):
	format = "%Y-%m-%d %H:%M:%S %Z%z"
	#timezone from db
	dbtz = pytz.timezone(timezone)

	#timestamp ftom db
	dbts= int(timestamp)
	odt = datetime.datetime.fromtimestamp(dbts, dbtz)

	#convert timestamp to utc
	utcodt = datetime.datetime.fromtimestamp(dbts, datetime.timezone.utc)
		
	#covert to analyst timezone
	lodt = datetime.datetime.astimezone(utcodt)
	
	print (trow)
	print ('\t\t',"Timestamp from database timezone:",odt.strftime(format),'\n'
		   '\t\t',"Timestamp in UTC time:",utcodt.strftime(format),'\n'
		   '\t\t',"Timestamp in your local time:",lodt.strftime(format))
	

conn = sqlite3.connect(acdb)
c = conn.cursor()

#Activity table
c.execute("SELECT * FROM Activity")
for row in c:
	
	parsed_app = json.loads(row[1])
	print ('\n'"AppId:", '\t\t',parsed_app[0]['application'])
	print ("Platform:", '\t', parsed_app[0]['platform'])
	print ("PackageIdHash:",'\t',row[2])
	print ("AppActivityId:",'\t', row[3])
	print ("ActivityType:", '\t', row[4])
	print ("PlatformDeviceId:",row[15]) 
	timecon("Last Modified Time:", row[10], dbtimezone)
	timecon("Expiration Time:", row[11], dbtimezone)
	print ("Payload:")
	#parse payload from data to str
	bpayload = row[12].decode('utf-8')
	line = re.sub('[{}"]','',bpayload)	
	for c in line:
		a = line.split(",")
	for pitem in a:
		print ('\t\t',pitem)
	
	timecon("Start Time:", row[18], dbtimezone)
	timecon("End Time:", row[19], dbtimezone)
	timecon("Last Modified On Client:", row[20], dbtimezone)
	print ("ETag:", '\t', row[29])
	print("_"*80)

conn.close()

if args.output:
	conn = sqlite3.connect(acdb)
	ecursor = conn.cursor()
	ecursor.execute("SELECT * FROM Activity")
	with open(output_file, "w", newline='') as csv_file:  # Python 3 version    
	    csv_writer = csv.writer(csv_file)
	    csv_writer.writerow([i[0] for i in ecursor.description]) # write headers
	    csv_writer.writerows(ecursor)
	    conn.close()
