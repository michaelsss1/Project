import biplist
import os
import sys
import sqlite3
import argparse
import csv



def PlistInv(plist):
    try:
        data = biplist.readPlist(plist)
    except (biplist.InvalidPlistException, biplist.NotBinaryPlistException):
        print("[-] Invalid PLIST file - unable to opened by biplist")
        sys.exit(1)
    print(data)

def SmsInv(sms):
    Conn = sqlite3.connect(sms)
    c = Conn.cursor()
    c.execute("pragma table_info(message)")
    table_data = c.fetchall()
    colums = [x[1] for x in table_data]
    c.close()
    return colums

def Write_csv(data, output_directory, name = None):
    if name is None:
        name = "report1.csv"
    print(f'Writing {name} to {output_directory}')
    with open(os.path.join(output_directory, name), "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
#        writer.writerow(header)
        writer.writerow(data)
        csvfile.close()


parser = argparse.ArgumentParser(description = "Tool for investiagte Mobile PLIST file.")
parser.add_argument("-p", "--plistFile", help = "plist file for read.")
parser.add_argument("-s", "--smsDB", help = "sms DB file for read.")
args = parser.parse_args()
if args.plistFile is not None and args.smsDB is None:
    Write_csv(PlistInv(args.plistFile), os.getcwd(), name = 'Plistdata.csv')
elif args.plistFile is None and args.smsDB is not None:
    Write_csv(SmsInv(args.smsDB), os.getcwd(), name = "SMS.csv")
elif args.plistFile is not None and args.smsDB is not None:
    Write_csv(PlistInv(args.plistFile), os.getcwd(), name = 'Plistdata.csv')
    Write_csv(SmsInv(args.smsDB), os.getcwd(), name = "SMS.csv")

