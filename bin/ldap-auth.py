#!/usr/bin/python26
#
#
#
#       LDAP/AD Autentication Script 
#
#       Please see Splunk's official documentation on scripted authentication for more info
#       http://docs.splunk.com/Documentation/Splunk/5.0.4/Security/Createtheauthenticationscript
#
#       Written by: Nick MacCarthy  - 9/2013
#
#       Note, this script requires the python ldap libraries
#
#       Configure LDAP servers in $app/local/ldap.conf
#

import ldap
import getopt
import sys, os
from ConfigParser import ConfigParser
from logger import *
import usertools

# keys we'll be using when talking with splunk.
USERNAME    = "username"
USERTYPE    = "role"
SUCCESS     = "--status=success"
FAILED      = "--status=fail"

# Defines if we are using a domain user or not, domain user is "DOMAIN\username", insted of just thier username
DOMAIN_USER = False

def getservers():
    
    '''
        Gets our LDAP servers form our ldap.conf in $app_home/local
    '''

    ourconfig = os.path.abspath(os.path.join(os.path.dirname(__file__), '../', 'local', 'ldap.conf'))

    config = ConfigParser()
    config.read(ourconfig)

    serverlist = config.get('authentication','serverList').split(',')
    serverlist = map(lambda x: x.strip(), serverlist)

    formatted_server_list = []
    for server in serverlist:

        # Skip disabled hosts
        try:
            if config.get(server, 'disabled') == "1":
                continue
        except:
            pass

        try:
            if config.get(server, 'ldaps') == "1":
                prefix = "ldaps"
            else: 
                prefix = "ldap"
        except:
            pass

        try:
            host = config.get(server, 'host')
            port = config.get(server, 'port')
            formatted_server_list.append( "%s://%s:%s" % ( prefix, host, port ) )
        except Exception, e:
            logger.error('getServerList - message="Unable to set LDAP server", reason="%s"' % ( e ))
            

    return formatted_server_list 


def userLogin( info ):

    LDAP_SERVERS = getservers()

    found_user = False

    for LDAP_SERVER in LDAP_SERVERS:

        try:

            if DOMAIN_USER:

                BIND_DN = info['username']

                logger.info('userLogin - message="User logging in with domain and username"  username="%s"' % ( BIND_DN ))

            else:
                myuserinfo = userinfo.getUsersRole(info['username'])

                domain = myuserinfo['domain'].upper()
                username = myuserinfo['username'].upper()

                BIND_DN = "%s\\%s" % ( domain, username )

            BIND_PASS = info['password']

            ldap_connection = ldap.initialize(LDAP_SERVER)
            ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)
            ldap.set_option(ldap.OPT_X_TLS,ldap.OPT_X_TLS_DEMAND)
            ldap.set_option( ldap.OPT_X_TLS_DEMAND, True )
            ldap.set_option(ldap.OPT_REFERRALS, 0)
            ldap.set_option(ldap.OPT_PROTOCOL_VERSION, 3)
            
            # Debug Mode, uncomment this to see debug level information on the command line
            #ldap.set_option( ldap.OPT_DEBUG_LEVEL, 255 )

            auth = ldap_connection.simple_bind_s(BIND_DN, BIND_PASS)

            found_user = True


            break

        except Exception, e:

            pass


    if found_user:
        print SUCCESS
        logger.info('message="Login Success" type="login" outcome="success" user="%s" script_return="%s" domain_controller="%s"' % ( BIND_DN, SUCCESS, LDAP_SERVER ))

    else:
        print FAILED
        logger.info('message="Login Failure" type="login" outcome="failure" user="%s" script_return="%s" domain_controller="%s"' % ( BIND_DN, FAILED, LDAP_SERVER ) )



def getUserInfo( infoIn ):

    ourinfo = userinfo.getUsersRole( infoIn['username'] )

    logger.info('getUserInfo - message="function called", username="%s"' % ( infoIn['username'] ))

    try:

        if DOMAIN_USER:
            username = ourinfo['domain'] + "\\" + ourinfo['username']
        else:
            username = ourinfo['username']

        #outStr = SUCCESS + " --userInfo=" + ";;" + username + ";" + ourinfo['fullname'] + ";" + ourinfo['roles']
        outStr = SUCCESS + userinfo.createFormattedUser(username, ourinfo['fullname'], ourinfo['roles'])

        logger.info('getUserInfo - message="found user", outcome="success", username="%s", outStr="%s"' % ( infoIn['username'], outStr))

        print outStr


    except:
        
        logger.info('getUserInfo - message="method being called for an invalid user", username="%s"' % ( infoIn['username'] ))

        print FAILED

def getUsers( infoIn ):

    try:
        print SUCCESS + userinfo.getAllUsers()
    except: 
        print FAILED



def readinputs():

   '''
    reads the inputs coming in and put them in a dict for processing.
   '''
   optlist, args = getopt.getopt(sys.stdin.readlines(), '', ['username=', 'password='])

   returnDict = {}
   for name, value in optlist:
      returnDict[name[2:]] = value.strip()

   return returnDict


def checkusername(username):

    if not username:
        return ''
            
    if "\\" in username['username']:
        return "domain_user"
    else:
        return ''

if __name__ == "__main__":

    logging = logger()
    logger = logging.get_logger('ldap_auth')

    callname = sys.argv[1]

    dictin = readinputs()

    # find out if we are dealing with domain\username or just a username
    usertype = checkusername(dictin)
  
    userinfo = usertools.usertools(usertype)

    if usertype == "domain_user":
        DOMAIN_USER = True
     
    logger.info('method "%s" called' % (callname))

    if callname == "userLogin": 
        userLogin( dictin )
    elif callname == "getUsers":
      getUsers( dictin )
    elif callname == "getUserInfo":
        getUserInfo( dictin )
    elif callname == "getSearchFilter":
      getSearchFilter( dictin )
    else:
      print "ERROR unknown function call: " + callname
