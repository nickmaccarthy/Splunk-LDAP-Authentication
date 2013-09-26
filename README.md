# Splunk AD Auth #

What is this?
-----------------------------------
This is a homegown Splunk app that allows users to authenticate against LDAP servers in an AD realm while keeping the ability to maintain role administration within Splunk.


Why use this instead of Splunks built in LDAP Auth?
----------------------------------
Splunks built in AD relies on user roles being defined in AD first, then mapped later.  This requires users to have thier Splunk roles come from AD.  Here this script simply autenticates a user against an AD server, then thier roles are defined in users.csv keeping role administration local to the Splunk admin.


Where are my users defined?
----------------------------------
Users are defined in local/users.csv.   You can use the default/users.csv as a reference.  Multiple roles can be assigned to users by delmiting them with a ":"


What are the requirements?
----------------------------------
Python 2.6+ with the python ldap modules installed.  In RHEL, simply enable the EPEL repos and "yum install python26" ( at the time of this writing ) and the python26 ldap modules.  Splunks built in python does not contain the python ldap modules

For setting up the bin/ldap-auth.py script, please see Splunks official documentation on scripted authentication:
http://docs.splunk.com/Documentation/Splunk/5.0.4/Security/ConfigureSplunkToUsePAMOrRADIUSAuthentication


Can this authenticate against multiple AD servers/Domain Controllers?
----------------------------------
Yes it can.  Please see default/ldap.conf on how to set this up.

How do I set this thing up?
----------------------------------
1. Git clone this app to your $SPLUNK_HOME/apps directory
2. Create some users in default/users.csv and copy this file to local/users.csv
3. Define your ldap servers in default/ldap.conf and move this to local/ldap.conf
4. Setup Splunk to use scripted authentication, and point $SPLUNK_HOME/etc/system/local/autentication.conf to bin/ldap-auth.py
5. Reload auth:  splunk reload auth


### Author: Nick MacCarthy
### Email: nickmaccarthy@gmail.com
