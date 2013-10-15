import controllers.module as module

import splunk, splunk.search, splunk.util, splunk.entity
import splunk.appserver.mrsparkle.lib.util as app_util
import lib.util as util
import lib.i18n as i18n

import logging
logger = logging.getLogger('splunk.module.GetUsers')

import math
import cgi
import csv

import os, sys


APPS_DIR = app_util.get_apps_dir()
APP_NAME = os.path.split(os.path.abspath(os.path.join(__file__, '../', '../', '../', '../')))[1]
SPLUNK_HOME = os.environ.get('SPLUNK_HOME')

# Add our app's bin to our PATH
#if not os.path.join(APPS_DIR, APP_NAME, 'bin') in sys.path:
#    sys.path.append(os.path.join(APPS_DIR, APP_NAME, 'bin')

#import usertools

class GetUsers(module.ModuleHandler):

    def generateResults(self, host_app, client_app, sid, count=1000,
                            offset=0, entity_name='results'):

    
        usercsv = os.path.join(APPS_DIR, APP_NAME, 'local', 'users.csv')

        try:
            users = csv.DictReader(open(usercsv, 'rb'))
        except Exception, e:
            logger.error('GetUsers.generateResults - unable to open users.csv at location: %s; reason: %s' % ( usercsv, e ))


        output = []
        output.append('<div class="CustomResultsTableWrapper">') 
        output.append('<table class="CustomResultsTable splTable">')

        fieldNames = ['Domain', 'Username', 'First Name', 'Last Name', 'Team', 'Team Role', 'Splunk Roles', 'Phone Number', 'Notes']
       
        # field names are hard coded currently.  If you need pull them dynamically from the CSV, uncomment this code below 
        #for user in users:
        #    fieldNames =  user.keys()
        #    break

        #fieldNames.sort()

        # Create our headers
        output.append('<tr>')
        for field in fieldNames:

            output.append('<th>%s</th>' % ( field ))
        output.append('</tr>')

        # Build the rest of the table
        for user in users:

            output.append('<tr>')
            for field in fieldNames:
                output.append('<td>%s</td>' % ( user[field] ))

            output.append('</tr>')

        output.append('</table>')
        output.append('</div>')

        output = ''.join(output)

        return output

