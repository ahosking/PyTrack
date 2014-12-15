import requests
import time #Required for time time stamping in youtrack
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
            return "Your time item was added successfully."
        except:
            return "Time addition failed."