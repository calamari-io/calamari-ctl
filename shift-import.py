#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
import re
import csv
from datetime import datetime, timedelta
from requests.auth import HTTPBasicAuth
from src.calamari import timesheet

MAX_CALLS_PER_SECOND=10
MAX_CALLS_PER_HOUR=720
API_LOGIN="calamari"

def main(args):
  #global base_url, api_key, auth_basic
  base_url = args.base_url
  api_key = args.api_key
  auth_basic=HTTPBasicAuth(API_LOGIN, api_key)

  if base_url[-1] != '/':
    base_url+='/'

  print('Parsing .csv file')
  parse_csv(args.file)
  print('Importing data ...')
  import_csv(args.file, base_url, auth_basic)

def check_date_format(date, date_format):
  # 2020-03-15T08:30:00
  try:
    if date != datetime.strptime(date, '%Y-%m-%dT%H:%M:%S').strftime('%Y-%m-%dT%H:%M:%S'):
      raise ValueError
    return True
  except ValueError:
    return False

def parse_csv(file):
  row_number=1
  with open(file, newline='') as csvfile:
    reader=csv.DictReader(csvfile)
    for row in reader:
      row_number+=1
      # check email address
      valid = re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', row['email'])
      if not valid:
        print(row['email'],'is not a valid email address (line: ', row_number,')')
        exit(1)
      # check date format
      if not check_date_format(row['start_date'],'%Y-%m-%dT%H:%M:%S'):
        print(row['start_date'],'is not in \'%Y-%m-%dT%H:%M:%S\' format (line: ', row_number,')')
        exit(1)
      if not check_date_format(row['end_date'],'%Y-%m-%dT%H:%M:%S'):
        print(row['end_date'],'is not in \'%Y-%m-%dT%H:%M:%S\' format (line: ', row_number,')')
        exit(1)
      # compare dates
      if datetime.strptime(row['start_date'],'%Y-%m-%dT%H:%M:%S') > datetime.strptime(row['start_date'],'%Y-%m-%dT%H:%M:%S'):
        print('Shift start date is after shift end date (line:', row_number,')')
        exit(1)

def import_csv(file, base_url, auth_basic):
  errors=[]
  with open(file, newline='') as csvfile:
    reader=csv.DictReader(csvfile)
    for row in reader:
      response=timesheet.create_shift(base_url, auth_basic, row['start_date'], row['end_date'], row['email'])
      if response.status_code != 200:
        print('Error creating shifts for',row['email'],'. Error: [',response.status_code,']: ',response.text)
        errors.append({'email': row['email'], 'start_date': row['start_date'], 'end_date': row['end_date']})
        continue

  if len(errors) > 0:
    print(errors)
    error_file_name=file.replace('.csv','').replace('.CSV','').replace('.Csv','')+'-errors.csv'
    fieldnames = ['email','start_date','end_date']
    with open(error_file_name,'w', encoding='UTF8', newline='') as error_file:
      writer=csv.DictWriter(error_file, fieldnames=fieldnames)
      writer.writeheader()
      writer.writerows(errors)
    
    print(len(errors),'lines were not imported. They were save in ', error_file_name)
  else:
    print('Import completed.')
  
  
        
  

if __name__ == '__main__':
  parser = argparse.ArgumentParser(prog='shift-import.py', usage='%(prog)s [options]')
  parser.add_argument('-k','--api-key', required=True, help='API Key - can be found in Configuration->Integrations->API')
  parser.add_argument('-b','--base-url', required=True, help='API Base URL - can be found in Configuration->Integrations->API. I.e. https://sample-tenant.us.calamari.io/api/')
  parser.add_argument('-f','--file', required=True, help='.csv file. Format described in README.md')
  args, unknown = parser.parse_known_args()
  main(args)
