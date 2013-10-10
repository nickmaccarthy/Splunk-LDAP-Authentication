import os, sys
import csv



class usertools(object):

    def __init__(self, usertype=''):
  
        '''
            Gets us setup and get our list of users from our local/users.csv
        ''' 
        self.DOMAIN_USER = False
         
        if usertype == "domain_user":
            self.DOMAIN_USER = True
   
        self.users = self.get_users() 


    def get_users(self):

        '''
            Opens our users CSV file, maps our full name and provides a dictionary back 

            @return     dict    dictionary of users
        '''
        ourfile = os.path.abspath(os.path.join(os.path.dirname(__file__), '../', 'local', 'users.csv'))

        dr = csv.DictReader(open(ourfile, 'rb'))

        export = {}
        for row in dr:

            domain = row['Domain'].strip()
            username = row['Username'].strip()
            fullname = "%s %s - %s" % ( row['First Name'].strip(), row['Last Name'].strip(), row['Team'].strip() )
            roles = row['Splunk Roles'].strip()

            ## Deprecated 10/2013, no longer need both both domain\user and user
            ## Make both the domain\user and regular username dictionary so we can find users no matter which username they used to log in with
            ##export["%s\\%s" % (row['Domain'].upper(), row['Username'])] = ( domain, username, fullname, roles )

            export[row['Username']] = ( domain, username, fullname, roles )

        return export

    def getUsersRole( self, username ):

        '''
            Gets the foles for a user.  

            @param  username    string  username we will find in our self.users dictionary
            @return dict        Dict of our user
        '''
        for row in self.users:

            found = self.case_insensitive_key(self.users, username)

            if found:
                return { 'domain': found[0][0], 'username' : found[0][1], 'fullname': found[0][2], 'roles' : found[0][3] }
            else:
                return False

    def getAllUsers(self):

        '''
            Gets all of our users from users.csv and puts them in the format Splunk is looking for

            @return     string      String of users with proper formatting that splunk is expecting
        '''

        out = ""
        for k,v in self.users.iteritems():

            username = k
            fullname = v[2]
            roles = v[3]

            #out += ' --userInfo=' + username.lower() + ';' + fullname + ';' + roles
            out += self.createFormattedUser(username, fullname, roles)

        return out


    def createFormattedUser(self, username='', fullname='', roles=''):

        
        try:

         user = '--userInfo=' + ';' + username.lower() + ';' + fullname + ';' + roles + "\n"

         return user

        except Exception, e:

            return
            #logger.error('error in CreateFormattedUser: %s' % ( e ))


    def case_insensitive_key(self, a,k):

        '''
            Finds a needle in a haystack in a case insenseitive nature
        '''
        k = k.lower()

        return [ a[key] for key in a if key.lower() == k ]
