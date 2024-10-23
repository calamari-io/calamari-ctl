#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
from requests.auth import HTTPBasicAuth
from datetime import datetime, timedelta
from src.calamari import employees, timesheet, holidays, workweeks, leave, tools

MAX_CALLS_PER_SECOND=10
MAX_CALLS_PER_HOUR=720
API_LOGIN="calamari"


def main(args):
  base_url = args.base_url
  api_key = args.api_key
  auth_basic=HTTPBasicAuth(API_LOGIN, api_key)

  if base_url[-1] != '/':
    base_url+='/'
  
  # build user email list
  employees_list=[]
  if args.all:
    response=employees.get_all_users(base_url, auth_basic)
    for employee in response:
      employees_list.append(employee['email'])
  else:
    if ',' in args.employees:
      employees_list=args.employees.strip().replace(' ','').split(',')
    else:
      employees_list.append(args.employees.strip().replace(' ',''))

  if args.action == 'list':
    print("Listing employees")
    for employee in employees_list:
      # validate user
      if '@' not in employee:
        print('Error',employee,'doesn\'t seem to be valid email address. Skipping.')
        continue 
      user=employees.get_user(base_url, auth_basic, employee, archived=args.archived)
      if user.status_code != 200:
        continue
      else:
        print(json.dumps(user.json(), indent=4))
  elif args.action == 'archive':
    print("Archiving employees")
    for employee in employees_list:
      # validate user
      if '@' not in employee:
        print('Error',employee,'doesn\'t seem to be valid email address. Skipping.')
        continue 
      response=employees.archive_user(base_url, auth_basic, employee)
      if response.status_code != 204:
        continue
      else:
        print('User',employee,'archived successfully.')

if __name__ == '__main__':
  parser = argparse.ArgumentParser(prog='employee_ctl.py', usage='%(prog)s [options]')
  parser.add_argument('action', choices=['list','archive'], help="Action to perform")
  parser.add_argument('-k','--api-key', required=True, help='API Key - can be found in Configuration->Integrations->API')
  parser.add_argument('-b','--base-url', required=True, help='API Base URL - can be found in Configuration->Integrations->API. I.e. https://sample-tenant.us.calamari.io/api/')
  parser.add_argument('--force', required=False, action='store_true', default=False,  help="Force delete without any prompts for confirmation")
  parser.add_argument('--archived', required=False, action='store_true', default=False,  help="List active and ARCHIVED employees")
  users = parser.add_mutually_exclusive_group(required=True) 
  users.add_argument('-e', '--employees', help='Comma-separated list of employees emails. Can\'t be used with -a')
  users.add_argument('-a', '--all', action='store_true', default=False,  help='Run for all users. Can\'t be used with -e')
  args, unknown = parser.parse_known_args()
  main(args)
