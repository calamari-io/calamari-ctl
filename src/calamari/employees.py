import requests
import json
from ratelimit import limits, sleep_and_retry
from requests.models import Response

MAX_CALLS_PER_SECOND=10
MAX_CALLS_PER_HOUR=720

@sleep_and_retry
@limits(calls=MAX_CALLS_PER_HOUR, period=3600)
@sleep_and_retry
@limits(calls=MAX_CALLS_PER_SECOND, period=1)
def get_users(base_url, auth_basic, page):
  endpoint_url=base_url+'employees/v1/list'
  payload = {
      "page":  page
  }

  response = requests.post(
     endpoint_url,
     json=payload,
     auth=auth_basic
  )
  if response.status_code != 200:
    print('Error getting users Error: [',response.status_code,']: ',response.text)
    response.raise_for_status()
  
  return response.json()

@sleep_and_retry
@limits(calls=MAX_CALLS_PER_HOUR, period=3600)
@sleep_and_retry
@limits(calls=MAX_CALLS_PER_SECOND, period=1)
def get_user(base_url, auth_basic, user, archived):
  endpoint_url=base_url+'employees/v1/search'

  # search for archived user
  if archived:
    payload = {
      "withArchived": archived
    }
    response = requests.post(
       endpoint_url,
       json=payload,
       auth=auth_basic
    )
    # dirty hack - api is unable to search for specific archived employee
    modified_response={"employees":[]}
    for employee in response.json()['employees']:
      if employee['email'] == user:
        modified_response['employees'].append(employee)
    # swap original response
    modified_response_obj = Response()
    modified_response_obj.status_code = 200
    modified_response_obj._content = json.dumps(modified_response).encode('ascii')
    
    if len(modified_response['employees']) != 0:
      return modified_response_obj
    
  # if archived users was not found proceed with regular search  
  payload = {
    "employee": user,
    "contractTypes": [],
    "positions": [],
    "teams": [],
    "withArchived": archived
  }
  response = requests.post(
     endpoint_url,
     json=payload,
     auth=auth_basic
  )

  if response.status_code != 200:
    print('Error getting user',user,'Error: [',response.status_code,']: ',response.text)
  
  return response

def archive_user(base_url, auth_basic, user):
  endpoint_url=base_url+'employees/v1/archive'
  payload = {
    "employee": user,
  }

  response = requests.post(
     endpoint_url,
     json=payload,
     auth=auth_basic
  )
  if response.status_code != 204:
    print('Error archiving user',user,'Error: [',response.status_code,']: ',response.text)
  
  return response

def get_all_users(base_url, auth_basic):
  page=0
  employee_list=[]

  while True:
    response=get_users(base_url, auth_basic, page)
    for employee in response['employees']:
      employee_list.append(employee)

    page+=1
    if page == response['totalPages']:
      break

  return employee_list
