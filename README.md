# calamari-ctl repository
This repository contains a set of command-line tools used for interacting with calamari.io API

# Disclaimer
This software is provided "AS IS", without waranty of any kind. In no event shall the calamari.io company be liable for any claim, damages or other liability. USE AT YOUR OWN RISK!

# Prerequisites
For successfull installation you need [pipenv](https://pipenv.pypa.io/en/latest/). Type:

```pip3 install pipenv```

# Installation

Clone this repository:

```git clone https://github.com/calamari-io/calamari-ctl.git```

To install all requirements, simply type:

```pipenv install``` 

*Do it in the main repository directory - the one with file named `Pipfile`.*

# Scripts
## shift-import.py
Import shifts from .csv file

### Usage

To use this script you need Calamari API key and your Base URL. You can find detailed instruction on [calamari.io blog](https://help.calamari.io/en/collections/5990-api).

You can check all available script options using `--help` parameter. Simply run:
```
./shift-import.py --help
usage: shift-import.py [options]

options:
  -h, --help            show this help message and exit
  -k API_KEY, --api-key API_KEY
                        API Key - can be found in Configuration->Integrations->API
  -b BASE_URL, --base-url BASE_URL
                        API Base URL - can be found in Configuration->Integrations->API. I.e. https://sample-tenant.us.calamari.io/api/
  -f FILE, --file FILE  .csv file. Format described in README.md
```

#### Importing from .csv file

```
# pipenv run ./shift-import.py  -k '<API_KEY>' -b '<BASE_URL>' -f <file>.csv
```

The .csv file must be in the format specified below.

```
email,start_date,end_date
emai@addres1.com,2024-12-23T11:54:00,2024-05-01T13:11:00
email@address2.com,2024-12-23T09:00:00,2024-05-02T16:44:00
```


## shift-ctl.py
Manage calamari.io shifts from command line

### Usage

To use this script you need Calamari API key and your Base URL. You can find detailed instruction on [calamari.io blog](https://help.calamari.io/en/collections/5990-api).

You can check all available script options using `--help` parameter. Simply run:
```
# pipenv run ./shift-ctl.py --help
usage: shift-ctl.py [options]

positional arguments:
  {list,delete,create}  Action to perform

options:
  -h, --help            show this help message and exit
  -k API_KEY, --api-key API_KEY
                        API Key - can be found in Configuration->Integrations->API
  -b BASE_URL, --base-url BASE_URL
                        API Base URL - can be found in Configuration->Integrations->API. I.e. https://sample-tenant.us.calamari.io/api/
  -f DATE_FROM, --date-from DATE_FROM
                        Start date in 'YYYY-MM-DD' format
  -t DATE_TO, --date-to DATE_TO
                        End data. Today's date if empty
  --force               Force delete without any prompts for confirmation
  -e EMPLOYEES, --employees EMPLOYEES
                        Comma-separated list of employees emails. Can't be used with -a
  -a, --all             Run for all users. Can't be used with -e
```

#### Listing shifts
Listing shifts for specific users(s):

```
# pipenv run ./shift-ctl.py list -k '<API_KEY>' -b '<BASE_URL>' -f '<START_DATE>' -t '<END_DATE>' -e user1@yourdomain.io,user2@yourdomain.io
```
`<START_DATE>/<END_DATE>` - dates in `YYYY-MM-DD` format

Listing shifts for all users in organization:

```
# pipenv run ./shift-ctl.py list -k '<API_KEY>' -b '<BASE_URL>' -f '<START_DATE>' -t '<END_DATE>' -a
```

#### Creating shifts

Shifts will be created according to users work schedule.

Create shifts for specific user(s):

```
# pipenv run ./shift-ctl.py create -k '<API_KEY>' -b '<BASE_URL>' -f '<START_DATE>' -t '<END_DATE>' -e user1@yourdomain.io,user2@yourdomain.io
```

Create shifts for all users in organization:

```
# pipenv run ./shift-ctl.py list -k '<API_KEY>' -b '<BASE_URL>' -f '<START_DATE>' -t '<END_DATE>' -a
```

#### Deleting shifts

Script will ask you to review shifts that you're planning to delete and to confirm deletion. If you shure that you know what you're doing add `--force`

Delete shifts for specific user(s):

```
# pipenv run ./shift-ctl.py delete -k '<API_KEY>' -b '<BASE_URL>' -f '<START_DATE>' -t '<END_DATE>' -e user1@yourdomain.io,user2@yourdomain.io
```

Delete shifts for specific user(s), no questions asked:

```
# pipenv run ./shift-ctl.py delete -k '<API_KEY>' -b '<BASE_URL>' -f '<START_DATE>' -t '<END_DATE>' -e user1@yourdomain.io,user2@yourdomain.io --force
```

Delete shifts for all users in organization:

```
# pipenv run ./shift-ctl.py delete -k '<API_KEY>' -b '<BASE_URL>' -f '<START_DATE>' -t '<END_DATE>' -a
```


## employee-ctl.py
Manage employees 

### Usage

To use this script you need Calamari API key and your Base URL. You can find detailed instruction on [calamari.io blog](https://help.calamari.io/en/collections/5990-api).

You can check all available script options using `--help` parameter. Simply run:
```
$ pipenv run ./employee-ctl.py --help
usage: employees-ctl.py [options]

positional arguments:
  {list,archive}        Action to perform

options:
  -h, --help            show this help message and exit
  -k API_KEY, --api-key API_KEY
                        API Key - can be found in Configuration->Integrations->API
  -b BASE_URL, --base-url BASE_URL
                        API Base URL - can be found in Configuration->Integrations->API. I.e. https://sample-tenant.us.calamari.io/api/
  --force               Force delete without any prompts for confirmation
  --archived            List active and ARCHIVED employees
  -e EMPLOYEES, --employees EMPLOYEES
                        Comma-separated list of employees emails. Can't be used with -a
  -a, --all             Run for all users. Can't be used with -e
```

#### Listing employees details
Listing employees(s) account details

```
# pipenv run ./employees-ctl.py list -k '<API_KEY>' -b '<BASE_URL>' -e user1@yourdomain.io,user2@yourdomain.io
```

Listing all employees in organization

```
# pipenv run ./employees-ctl.py list -k '<API_KEY>' -b '<BASE_URL>' -a
```

#### Archiving  employees
Archive selected employees accounts

```
# pipenv run ./employees-ctl.py archive -k '<API_KEY>' -b '<BASE_URL>' -e user1@yourdomain.io,user2@yourdomain.io
```

Archive all employees. One (last) admin account will be keept active.

```
# pipenv run ./employees-ctl.py archive -k '<API_KEY>' -b '<BASE_URL>' -a
```
