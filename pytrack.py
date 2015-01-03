#Standard classes
import time #Required for time time stamping in youtrack

#Dependencies
import requests
import xml.etree.ElementTree as ET

#This class will allow you to submit to a specified Youtrack installation
#via python and the requests module.

class pytrack(object):
    def __init__(self, baseURL, port=None, username=None, password=None):
        self.baseURL = baseURL
        self.port = str(port)
        self.username = username
        self.password = password
        if self.port != None:
            #Port has been entered, affix it to the base URL
            self.baseURL += ":" + self.port + "/rest/"

    def add_comment(self, issue, author, comment):
        '''
        This will enable you to add a comment to the issue specified with the associated author
        and the comment provided.

        :param issue:
        :param author:
        :param comment:
        :return:
        '''
        # youtrack_method = "issue/" + issue + "/execute?comment=" + comment + "&runas=" + author
        # outrack_url = "http://youtrack.arcestra.com:8180/rest/" + youtrack_method
        try:
            submitURL = self.baseURL +\
                "issue/" + issue + "/execute?comment=" + comment + "&runas=" + author
            r = requests.post(submitURL, auth=(self.username, self.password))
            return ("Your comment was added to " + issue + " successfully.")
        except:
            return submitURL



    ### Time Tracking ###
    def get_time(self, issue):
        """
        This will get all available time items on a given issue.
        :param issue: The issue number to look up
        :return: return a class of time items that each contain: id, date, duration, description and author
        """
        #Submit the request
        submitURL = self.baseURL + "issue/" + issue + "/timetracking/workitem"
        r = requests.get(submitURL, auth=(self.username, self.password))
        #Parse the text and output it nicely:
        tree = ET.fromstring(r.text)
        print "------------------------------------"
        print "There are ", str(len(tree)), "work items in", issue
        print "------------------------------------"
        for x in tree.iter("workItem"):
            # print x.tag, x.attrib
            try:
                for a in x.iter():
                    if not a.tag == "workItem":
                        if a.attrib == {}:
                            print a.tag, a.text
                        else:
                            print a.tag, a.attrib, a.text
            except:
                pass

            
    def add_time(self, issue, timeadded, description=None):
        """
        :param issue: The issue number
        :param time: Time in a number with data for value, this must be converted to minutes (ex: H=hours, m=minutes)
        :param description: Any text that should be added to the time entry
        :return: a success message with the issue, time added and text returned, else false
        """
        workitem = "<workItem>\n" +\
            "<date>" + str(int(time.time())) + "000" + "</date>\n" +\
            "<duration>" + str(timeadded) + "</duration>\n" +\
            "<description>" + description + "</description>\n" +\
            "</workItem>"
        #Youtrack represents the correct date only when I add "000" to the end of the time stamp...
        try:
            submitURL = self.baseURL + "issue/" + issue + "/timetracking/workitem"
            headers = {'content-type': 'application/xml'}
            r = requests.post(submitURL, data=workitem, headers=headers, auth=(self.username, self.password))
            print r.status_code
            ##FINISH this message
            return "Your time item was added successfully."
        except:
            return

    def delete_time(self, issue, itemID):
        pass

    ### Projects ###
    def get_projects(self, verbose=None):
        '''
        :param verbose:
        :return: return a dictionary of projects that are currently available
        '''
        if verbose != True:
            verbose = False
        submitURL = self.baseURL + "project/all?" + str(verbose)

        r = requests.get(submitURL, auth=(self.username, self.password))
        print r.status_code
        return r.text