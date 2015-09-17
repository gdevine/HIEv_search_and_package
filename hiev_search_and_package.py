'''
Python script to perform a HIEv search api call (based on given query parameters) and then a packaging of the returned files 

Author: Gerard Devine
Date: September 2015
 
'''

import os
import json
import urllib2
from datetime import datetime
import requests


# Either set your api key via an environment variable (recommended) or add directly below 
# api_token = os.environ['STAGING_HIEV_API_KEY']
api_token = 'yDkDbTTTsmxjYY56yFt2'

# -- Set up global values
request_url = 'https://ic2-diver-staging-vm.intersect.org.au/data_files/api_search'
package_url = 'https://ic2-diver-staging-vm.intersect.org.au/packages/api_create?auth_token=' + api_token
publish_url = 'https://ic2-diver-staging-vm.intersect.org.au/packages/api_publish?auth_token=' + api_token

# -- Set up parameters in which to do the HIEv API search call (see dc21 github wiki for full list of choices available)
filenames = 'FACE_R1_P0037_SECURPHOT-TERNsnapshot_2015070.*\.jpg$'


# --Open log file for writing and append date/time stamp into file for a new entry
logfile = 'log.txt'
log = open(os.path.join(os.path.dirname(__file__), logfile), 'a')
log.write('\n----------------------------------------------- \n')
log.write('------------  '+datetime.now().strftime('%Y-%m-%d %H:%M:%S')+'  ------------ \n')
log.write('----------------------------------------------- \n')


# -- Set up the http request and handle the returned response
request_headers = {'Content-Type' : 'application/json; charset=UTF-8', 'X-Accept': 'application/json'}
request_data = json.dumps({'auth_token': api_token, 'filename':filenames})
request  = urllib2.Request(request_url, request_data, request_headers)
response = urllib2.urlopen(request)
js = json.load(response)


# If there are returned results then group file_ids into an array to be passed to the package API
log.write(' Number of search results returned = %s \n' %len(js))
if len(js):
    file_ids = [] 
    # --For each element returned append the file_id to the master array
    for entry in js:
        # Check if the file id already exists (it really shouldn't!)
        if not entry['file_id'] in file_ids:
            # append the ID
            file_ids.append(entry['file_id'])
        else:
            log.write(' Warning: File ID Exists - %s \n' %entry['file_id'])

    log.write('-- Complete \n')
else:
    log.write('No files matched the search params \n')
    log.write('\n')
    log.write('\n')

print file_ids

description = """Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod 
               tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, 
               quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. 
               Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat 
               nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia 
               deserunt mollit anim id est laborum."""

# Construct the metadata payload including the list of file ids to be packaged 
payload = {'file_ids[]': file_ids, 
           'filename': 'Gerry_api_record', 
           'experiment_id': 2, 
           'title': 'Data publication produced via HIEv package and publish API for January to September 2015',
           'access_rights_type' : 'Open',
           'description': description,
           'license': "CC-BY",
           'tag_names': '"My files", "Gerry", "HIE"',
           'label_names': '"Science", "Trees", "CO2"',
           'grant_numbers': '"AB34567", "CDEF123"',
           'related_websites': '"http://www.intersect.org.au","http://mq.edu.au"',
           'start_time': '2015-01-01 00:00:00',
           'end_time': '2015-09-01 00:00:00', 
           'run_in_background': False} 
  
#send the api call  
r = requests.post(package_url, data=payload)
   
#and capture the newly created package_id
package_id = json.loads(r.text)['package_id']   


#Publish the created package

p = requests.post(publish_url, {'package_id':package_id})

print p

# --Close log file
log.close()
