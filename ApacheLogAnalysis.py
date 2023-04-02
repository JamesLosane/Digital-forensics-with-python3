#!/bin/python3

import os 
import pandas as pd
import module.tablestream as tablestream
import sys
import csv
import gc 
import argparse

# Apache log analysis

banner = """
 \u001b[36m
                                                                                 
██╗      ██████╗  ██████╗  ██████╗██╗  ██╗███████╗ ██████╗██╗  ██╗
██║     ██╔═══██╗██╔════╝ ██╔════╝██║  ██║██╔════╝██╔════╝██║ ██╔╝
██║     ██║   ██║██║  ███╗██║     ███████║█████╗  ██║     █████╔╝ 
██║     ██║   ██║██║   ██║██║     ██╔══██║██╔══╝  ██║     ██╔═██╗ 
███████╗╚██████╔╝╚██████╔╝╚██████╗██║  ██║███████╗╚██████╗██║  ██╗
╚══════╝ ╚═════╝  ╚═════╝  ╚═════╝╚═╝  ╚═╝╚══════╝ ╚═════╝╚═╝  ╚═╝   
                                                                           \u001b[0m
                               \u001b[38;5;84mcoded with <3 by ish_Dante\u001b[0m """

def ip_uid_date_size_files(filename):
	text_data = {}
	current_file = filename
	open_file = open(current_file, 'r', encoding="latin-1")
	file_data = open_file.readlines()
	index = 0
	for line in file_data:
		count = line.strip().split(" ",1)[0]
		list_items = line.strip().split(" ",1)[1][1:].split(";")
		text_data[index] = [count,list_items]
		index = index + 1
	return text_data

def dpkg_file(filename):
    text_data = {}
    current_file = filename
    open_file = open(current_file, 'r', encoding="latin-1")
    file_data = open_file.readlines()
    index = 0
    for line in file_data:
    	splitted_lines = line.strip().split(" ")
    	text_data[f"{index}"] = splitted_lines[0:]
    	index += 1
    return text_data

def output_to_csv(filename):
	with open(f'{filename}', 'w') as csvfile:
		writer = csv.DictWriter(csvfile, fieldnames = field_names)
		writer.writeheader()
		for key in dictonary_of_output.keys():
			csvfile.write("%s,%s\n"%(key.replace(",",' ').replace(";",''),dictonary_of_output[key].replace(",",' ')))

#--------------------------------------------APACHE ACCESS LOG ( USERAGENT )--------------------------------------------------------------
def read_and_split_file_useragent(filename) :
    text_data = {}
    current_file = filename
    open_file = open(current_file, 'r', encoding="latin-1")
    file_data = open_file.readlines()
    for line in file_data:
    	line.strip()
    	splitted_lines = line.strip().split(" ",1)
    	if len(splitted_lines) < 2:
    		continue
    	text_data[f"{splitted_lines[1]}"] = splitted_lines[0]
    return text_data


def apache_user_agents_getdata(filename):
	command = 'awk -F\\"'  + " '{print $6}' " + filename + " | sed 's/(\([^;]\+; [^;]\+\)[^)]*)/(\1)/' | sort | uniq -c | sort -bgr > apache_user_agents.txt" 
	os.system(command)
	return True

def apache_user_agent(filename,save_csv=False,output_csv=None):
	if(apache_user_agents_getdata(filename)):
		print('\n\n \t\t\t \u001b[1m\u001b[38;5;178mApache Log ( useragent ) Results \u001b[0m')
		dictonary_of_useragent = read_and_split_file_useragent("apache_user_agents.txt")		
		field_names = ["User Agent","Count"]
		if output_csv != None:
			output_csvfile = output_csv.split('.')[0] + '_useragent.csv'
		else:
			output_csvfile = 'apache_user_agents.csv'
		if save_csv == True:
			print("\t\t\u001b[1m\u001b[38;5;8m==============================================\u001b[37;1m")
			print()
			print(f"\t\tResults saved in {output_csvfile}\u001b[37;1m")
			print()
			print("\t\t\u001b[1m\u001b[38;5;8m==============================================\u001b[37;1m")
			with open(output_csvfile, 'w') as csvfile:
				writer = csv.DictWriter(csvfile, fieldnames = field_names)
				writer.writeheader()
				for key in dictonary_of_useragent.keys():
					csvfile.write("%s,%s\n"%(key.replace(",",' ').replace(";",' '),dictonary_of_useragent[key].replace(",",' ')))
		useragent = list(dictonary_of_useragent.keys())
		counts = list(dictonary_of_useragent.values())
		t = tablestream.TableStream(column_width=(10, 50),header_row=('Count', 'User Agent'))
	
		try:
			count=0
			for i in range(len(useragent)):
				if count>5:
					break
				else:
					count+=1
				if int(counts[i])>50:
					COLOR_TYPE = {
                f'{useragent[i]}': 'red'
            }
				elif int(counts[i])>10:
					COLOR_TYPE = {
				f'{useragent[i]}': 'yellow'
			}
				color_type = COLOR_TYPE.get(useragent[i],None)
				t.write_row((counts[i], useragent[i]),colors=(None,color_type))
			t.close()
		except (IOError, OSError):
			sys.exit(141)
		os.system('rm -r apache_user_agents.txt')
		del useragent
		del dictonary_of_useragent
		del counts
		gc.collect()
				

#--------------------------------------------APACHE ACCESS LOG ( IP, UID, DATE TIME, STATUS CODE, CONTENT SIZE )--------------------------------------------------------------

def ip_uid_date_size_data(filename,ip=False,uid=False,date_time=False,status_code=False,content_size=False):
	requested_options = []
	count_length = 5
	ip_length = 16
	uid_length = 5
	date_time_lenght = 30
	status_code_length = 10
	content_size_length = 8
	header_width = [count_length]
	csv_filename = ''
	command = "awk '{print "
	command_end = "}' " + filename +" | sort | uniq -c | sort -bgr > ip_uid_date_size.txt"
	if ip == True:
		requested_options.append("IP")
		csv_filename +='ip_'
		command += '";"$1'
		header_width.append(ip_length)
	if uid == True:
		requested_options.append("User Id")
		csv_filename +='uid_'
		command += '";"$3'
		header_width.append(uid_length)
	if date_time == True:
		requested_options.append("Date/Time")
		csv_filename +='date_'
		command += '";"$4,$5'
		header_width.append(date_time_lenght)
	if status_code == True:
		requested_options.append("Status Code")
		csv_filename +='status_code_'
		command += '";"$9'
		header_width.append(status_code_length)
	if content_size == True:
		requested_options.append("Content Size")
		csv_filename +='content_size_'
		command += '";"$10'
		header_width.append(content_size_length)
	final_command = command + command_end
	os.system(final_command)
	return requested_options,header_width,csv_filename[:-1]


def row_write_query_creator(items_list,count=0):
	if count != 0:
		row_list =[count]
	else:
		row_list = []
	for items_values in items_list:
		row_list.append(items_values)
	return row_list


def row_write_query_creator_dpkg(items_list):
	row_list =[count]
	for items_values in items_list:
		row_list.append(items_values)
	return row_list	

def csv_file_string_creator(items_list):
	final_str =''
	for item in items_list:
		final_str +=str(item).replace(",",' ').replace(";",' ') + ','
	return( final_str[:-1] + '\n')

def ip_uid_date_size(filename,ip=False,uid=False,date_time=False,status_code=False,content_size=False,save_csv=False,output_csv=None):
	requested_options,header_width,csv_filename = ip_uid_date_size_data(filename,ip,uid,date_time,status_code,content_size)
	console_string = '\n\n \t \u001b[1m\u001b[38;5;178mApache Log ( '
	for req in requested_options:
		console_string += req + ' '
	console_string += ') Results \u001b[37;1m'
	print(console_string)
	data_txt = ip_uid_date_size_files("ip_uid_date_size.txt")

	field_names = ['Count'] + requested_options
	total_count = list(data_txt.keys())
	if output_csv != None:
		output_csvfile = output_csv.split('.')[0] + '_' + csv_filename +'.csv'
	else:
		output_csvfile = csv_filename + '.csv'

	if save_csv == True:
			print("\t\t\u001b[1m\u001b[38;5;8m==============================================\u001b[37;1m")
			print()
			print(f"\t\tResults saved in {output_csvfile}\u001b[37;1m")
			print()
			print("\t\t\u001b[1m\u001b[38;5;8m===============================================\u001b[37;1m")
			with open(output_csvfile, 'w') as csvfile:
				writer = csv.DictWriter(csvfile, fieldnames = field_names)
				writer.writeheader()
				for key in data_txt.values():
					csvfile.write(csv_file_string_creator(key))


	t = tablestream.TableStream(header_width,header_row=tuple(field_names))
	
	try:
		top_header=0
		for count,items in data_txt.values():
				if top_header > 5:
					break
				else:
					top_header = top_header + 1
				t.write_row(row_write_query_creator(items,count))

		t.close()
	except (IOError, OSError):
		sys.exit(141)
	os.system('rm -r ip_uid_date_size.txt')
	del data_txt
	del total_count
	gc.collect()

#--------------------------------------------apache access LOG ( request line, referer )--------------------------------------------------------------

def request_referer_data(filename,request_line=False,referer=False):
	requested_options = []
	count_length = 5
	request_length = 30
	referer_length = 30
	header_width = [count_length]
	command = 'awk -F\\"' +" '{print "
	command_end = "}' " + filename +" | sort | uniq -c | sort -bgr > request_referer.txt"
	csv_filename = ''
	if request_line == True:
		requested_options.append("Request Line")
		csv_filename +='request_'
		command += '";"$2'
		header_width.append(request_length)
	if referer == True:
		requested_options.append("Referer")
		csv_filename +='referer_'
		command += '";"$4'
		header_width.append(referer_length)
	final_command = command + command_end
	os.system(final_command)
	return requested_options,header_width,csv_filename[:-1]

def request_referer(filename,request_line=False,referer=False,save_csv=False,output_csv=None):
	requested_options,header_width,csv_filename = request_referer_data(filename,request_line,referer)
	console_string = '\n\n \t\t\t \u001b[1m\u001b[38;5;178mApache Log ( '
	for req in requested_options:
		console_string += req + ' '
	console_string += ') Results\u001b[37;1m'
	print(console_string)
	data_txt = ip_uid_date_size_files("request_referer.txt")

	field_names = ['Count'] + requested_options
	total_count = list(data_txt.keys())
	if output_csv != None:
		output_csvfile = output_csv.split('.')[0] + '_' +csv_filename +'.csv'
	else:
		output_csvfile = csv_filename + '.csv'

	if save_csv == True:
			print("\t\t\u001b[1m\u001b[38;5;8m==============================================\u001b[37;1m")
			print()
			print(f"\t\tResults saved in {output_csvfile}\u001b[37;1m")
			print()
			print("\t\t\u001b[1m\u001b[38;5;8m==============================================\u001b[37;1m")
			with open(output_csvfile, 'w') as csvfile:
				writer = csv.DictWriter(csvfile, fieldnames = field_names)
				writer.writeheader()
				for key in data_txt.values():
					csvfile.write(csv_file_string_creator(key))


	t = tablestream.TableStream(header_width,header_row=tuple(field_names))
	try:
		counts=0
		for count,items in data_txt.values():
				if counts > 5:
					break
				else:
					counts += 1
				t.write_row(row_write_query_creator(items,count))

		t.close()
	except (IOError, OSError):
		sys.exit(141)
	os.system('rm -r request_referer.txt')
	del data_txt
	del total_count
	gc.collect()


#--------------------------------------------DPKG LOG--------------------------------------------------------------

def dpkg_log_data(filename,half_installed=True,date=False,time=False):
	requested_options = ["count"]
	count_length = 5
	installed_length = 20
	version_length = 20
	date_length = 12
	time_length = 10
	header_width = [count_length]
	command_start = f"grep 'installed' {filename}| "
	command_mid = "awk '{print $5 \" \" $6 " 
	command_end = "}' | sort | uniq -c | sort -bgr > dpkg_log_analysis.txt"
	if half_installed == False:
		command_start += "grep -v half-installed |"
		command_start += command_mid
		requested_options.append("Installed / Half Installed")
	else:
		requested_options.append("Complete Installed")
		command_start += command_mid
	header_width.append(installed_length)
	header_width.append(version_length)
	requested_options.append("Version")
	if date == True:
		command_start += " \" \"$1 "
		requested_options.append("Date")
		header_width.append(date_length)
	if time == True:
		command_start += " \" \"$2 "
		requested_options.append("Time")
		header_width.append(time_length)
	final_command = command_start + command_end
	os.system(final_command)
	return requested_options,header_width

def dpkg_log_analysis(filename,half_installed=True,date=False,time=False,save_csv=False,output_csv=None):
	print("\n\n \t\t\t \u001b[1m\u001b[38;5;178mWorking on DPKG Log \u001b[37;1m")
	requested_options_dpkg, header_width_dpkg= dpkg_log_data(filename,half_installed,date,time)
	dpkg_dictonary = dpkg_file("dpkg_log_analysis.txt")
	total_count = len(list(dpkg_dictonary.keys()))
	if output_csv != None:
		output_csvfile = output_csv.split('.')[0] + '.csv'
	else:
		output_csvfile = 'dpkg_log_analysis.csv'

	if save_csv == True:
			print("\t\t\u001b[1m\u001b[38;5;8m==============================================\u001b[37;1m")
			print()
			print(f"\t\t\u001b[1m\u001b[38;5;196mResults saved in {output_csvfile}\u001b[37;1m")
			print()
			print("\t\t\u001b[1m\u001b[38;5;8m==============================================\u001b[37;1m")
			with open(output_csvfile, 'w') as csvfile:
				writer = csv.DictWriter(csvfile, fieldnames = requested_options_dpkg)
				writer.writeheader()
				for key in dpkg_dictonary.values():
					csvfile.write(csv_file_string_creator(key))
 

	t = tablestream.TableStream(header_width_dpkg,header_row=tuple(requested_options_dpkg))

	try:
		counts=0
		for items in dpkg_dictonary.values():
				if counts>5:
					break
				else:
					counts+=1
				t.write_row(row_write_query_creator(items_list=items))

		t.close()
	except (IOError, OSError):
		sys.exit(141)
	os.system('rm -r dpkg_log_analysis.txt')
	del dpkg_dictonary
	gc.collect()


if __name__ == "__main__":
	terminal_size = os.get_terminal_size()
	os.system('clear')
	if terminal_size[0] < 83:
		print("\u001b[1m\u001b[38;5;196mTERMINAL SIZE IS SMALLER IT WILL EFFECT THE OUTPUT VIEW\u001b[0m\n\n")
		continue_or_not = input("\u001b[1m\u001b[38;5;178mWant to continue (y/n): \u001b[0m")
		if continue_or_not == 'y' or continue_or_not == 'Y':
			pass
		else:
			exit()
	os.system('clear')
	print(banner)
	parser = argparse.ArgumentParser()
	subparser = parser.add_subparsers(dest='command')
	apache_log = subparser.add_parser('apache')
	dpkg_log = subparser.add_parser('dpkg')
	apache_log.add_argument('-useragent', action='store_true',help='To show useragent in apache log')
	apache_log.add_argument('-ip', action='store_true',help='To show ip in apache log')
	apache_log.add_argument('-uid', action='store_true',help='To show uid in apache log')
	apache_log.add_argument('-date', action='store_true',help='To show date in apache log')
	apache_log.add_argument('-status-code', action='store_true',help='To show status-code in apache log')
	apache_log.add_argument('-content-size', action='store_true',help='To show content-size in apache log')
	apache_log.add_argument('-referer', action='store_true',help='To show referer in apache log')
	apache_log.add_argument('-request-line', action='store_true',help='To show request-line in apache log')
	parser.add_argument('-save', action='store_true',help='To save the output in a csv file')
	dpkg_log.add_argument('-half', action='store_false',help='To show half installed packages in dpkg log')
	dpkg_log.add_argument('-date', action='store_true',help='To show date in dpkg log')
	dpkg_log.add_argument('-time', action='store_true',help='To show time in dpkg log')
	parser.add_argument('-f', type=str, required=True ,help="log file name")
	parser.add_argument('-o', type=str, required=False ,help="Name of output csv file")
	args = parser.parse_args()

	save_csv_bool = args.save
	output_bool = args.o
	if(os.path.isfile(os.path.abspath(args.f))):
		pass
	else:
		print(f"\n\u001b[1m\u001b[31m\t\t\tFile \u001b[37;1m{args.f} \u001b[31mdoesn't exist")
		exit()

	if args.command == "apache":
		filename  = os.path.abspath(args.f)
		if args.useragent == True:
			apache_user_agent(filename,save_csv_bool,output_bool)
		if args.ip == True or args.uid == True or args.date == True or args.status_code == True or args.content_size == True :
			ip_bool = args.ip
			uid_bool = args.uid
			date_bool = args.date
			status_code_bool = args.status_code
			content_size_bool = args.content_size
			ip_uid_date_size(filename,ip_bool,uid_bool,date_bool,status_code_bool,content_size_bool,save_csv_bool,output_bool)
		if args.referer == True or args.request_line == True :
			referer_bool = args.referer
			request_line_bool = args.request_line
			request_referer(filename,request_line_bool,referer_bool,save_csv_bool,output_bool)
	elif args.command == "dpkg":
		half_bool = args.half
		date_dpkg_bool = args.date
		time_bool = args.time
		filename  = args.f
		dpkg_log_analysis(filename,half_bool,date_dpkg_bool,time_bool,save_csv_bool,output_bool)

			
