#Standard classes
import time

#Dependencies
import requests
import xml.etree.ElementTree as ET

#This class will allow you to submit to a specified Youtrack installation
#via python and the requests module.

'''need to create error trapping for dead youtrack servers/connectios
###Also need to break out the connection so that it uses credentials while no cookies are available.
###Otherwise cookies should be used so that we are not always sending credentials
'''

class pytrack(object):
    def __init__(self, baseURL, port=None, username=None, password=None):
        self.baseURL = baseURL
        self.port = str(port)
        self.username = username
        self.password = password
        if self.port != None:
            #Port has been entered, affix it to the base URL
            self.baseURL += ":" + self.port + "/rest/"

    def comments_get(self, issue, wikifyDescription=None):
        #GET /rest/issue/{issue}/comment&{wikifyDescription}
        try:
            submitURL = self.baseURL + "issue/" + issue + "/comment"
            r = requests.get(submitURL, auth=(self.username, self.password))
            print "This has returned:\n", r.text
            #Parse things!
            tree = ET.fromstring(r.text)
            message = "------------------------------------\n"
            message += "There are " + str(len(tree)) + " comments in " + issue + ":\n"
            message += "------------------------------------\n"

            for x in tree.iter("comments"):
                # print x.tag, x.attrib
                for a in x.iter():
                    if a.tag == "comment":
                        # print a.attrib
                        # print a.text
                        comment = a.attrib
                        # format the message like below
                        # Comment ID|Comment|Author|Created
                        # 89-20|'Testing Phase 2'|'ahoskng'|'1422764898079'
                        message += (comment['id'] + " | " + comment['text'] + " | " + comment['author'] +\
                                    " | " + comment['created'] + "\n")
            print message
            return message
        except:
            message = "We could not retrieve comments for issue: " + issue
            print message
            return message

    def comments_add(self, issue, author, comment):
        '''
        This will enable you to add a comment to the issue specified with the associated author
        and the comment provided.
        :param issue:
        :param author:
        :param comment:
        :return:
        '''
        # youtrack_method = "issue/" + issue + "/execute?comment=" + comment + "&runas=" + author
        # youtrack_url = "http://youtrack.arcestra.com:8180/rest/" + youtrack_method
        try:
            submitURL = self.baseURL +\
                "issue/" + issue + "/execute?comment=" + comment + "&runas=" + author
            r = requests.post(submitURL, auth=(self.username, self.password))
            #print "Your attempt to add a comment to %s returned %s." % (issue, str(r.status_code)) #Originally used for debugging. Must make prettier!
            message = "You have successfully added the comment: \n\"" + comment + "\" to issue: " + issue
            print message
            return ("Your comment was added to " + issue + " successfully.")

        except:
            return submitURL

    def comments_remove(self, issue, comments, permanently=None):
        '''

        :param issue: String of the issue number
        :param comments: String or tuple of strings for comment(s) to delete
        :param permanently:  Boolean to permanently delete comments - It should be noted that as of 2/2/2015,\
         this does not work as expected. As of 02/07/2015 This is marked as fixed in youtrack 6.1
        :return: Summarize the actions taken
        '''
        # DELETE /rest/issue/{issue}/comment/{comment}?{permanently}
        print "You are trying to delete ", comments
        submitURL = ""
        if type(comments) == str:
            submitURL = self.baseURL + "issue/" + issue + "/comment/" + comments
        elif type(comments) == list:
            submitURL = []
            for item in comments:
                submitURL.append(self.baseURL + "issue/" + issue + "/comment/" + item)

        if permanently:
            if type(submitURL) == str:
                submitURL += "?permanently=true"
            else:
                for i in submitURL:
                    i += "?permanently=true"
        try:
            if type(submitURL) == str:
                print submitURL
                r = requests.delete(submitURL, auth=(self.username, self.password))
                if r.status_code != 200:
                    print submitURL, "either does not exist or couldn't be deleted."
            else:
                if permanently:
                    for i in submitURL:
                        i += "?permanently=true"
                        r = requests.delete(i, auth=(self.username, self.password))
                        if r.status_code != 200:
                            print submitURL, "either does not exist or couldn't be deleted."
                        else:
                            print i
                else:
                    for i in submitURL:
                        r = requests.delete(i, auth=(self.username, self.password))
                        if r.status_code != 200:
                            print submitURL, "either does not exist or couldn't be deleted."
                        else:
                            print i
        except:
            print "We failed..."


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


    def add_time(self, issue, timeadded, description=None, worktype=None):
        """
        :param issue: The issue number
        :param timeadded: Time in minutes to be added to the ticket
        :param description: Any text that should be added to the time entry
        :param worktype: This will work if any of the defined worktypes is entered. This is left out if unspecified
        :return: a success message with the issue, time added and text returned, else false
        """
        if worktype == None:
            workitem = "<workItem>\n" +\
                "<date>" + str(int(time.time())) + "000" + "</date>\n" +\
                "<duration>" + str(timeadded) + "</duration>\n" +\
                "<description>" + description + "</description>\n" +\
                "</workItem>"
        else:
            workitem = "<workItem>\n" +\
                "<date>" + str(int(time.time())) + "000" + "</date>\n" +\
                "<duration>" + str(timeadded) + "</duration>\n" +\
                "<description>" + description + "</description>\n" +\
                "<worktype><name>" + worktype + "</name></worktype>\n" +\
                "</workItem>"
        #Youtrack represents the correct date only when I add "000" to the end of the time stamp...
        try:
            submitURL = self.baseURL + "issue/" + issue + "/timetracking/workitem"
            headers = {'content-type': 'application/xml'}
            r = requests.post(submitURL, data=workitem, headers=headers, auth=(self.username, self.password))
            message = "You added %s minutes to ticket %s.\n %s" % (timeadded, issue, r.text)
            print message
            return message
        except:
            message = "You failed to add %s minutes to ticket %s.\n %s" % (timeadded, issue, r.text)
            print message
            return message

    def delete_time(self, issue, itemID):
        '''
        :param issue: The issue number
        :param itemID: The workitem (time entry) to be removed
        :return: Returns a message letting the user know of success or failure and the corresponding data
        '''
        submitURL = self.baseURL + "issue/" + issue + "/timetracking/workitem/" + itemID
        try:
            r = requests.delete(submitURL, auth=(self.username, self.password))
            message = "You successfully removed time entry %s on issue %s" % (issue, itemID)
            print message
            return message
        except:
            message = "You failed to remove time entry: %s on issue %s" % (itemID, issue)
            print message
            return message


    ### Projects ###
    def get_project(self, projectId, assignee=None):
        submitURL = self.baseURL + "admin/project/" + projectId
        if assignee != True:
            r = requests.get(submitURL, auth=(self.username, self.password))
            return r.text
        else:
            #We want the project assignee
            submitURL += "/assignee"
            r = requests.get(submitURL, auth=(self.username, self.password))
            return r.text
        #     tree = ET.fromstring(r.text)
        #     print "------------------------------------"
        #     print "Assignees in", projectId
        #     print "------------------------------------"
        #     for x in tree.iter("assignees"):
        #         # print x.tag, x.attrib
        #         try:
        #             for a in x.iter():
        #                 if not a.tag == "None":
        #                     if a.attrib == {}:
        #                         print a.tag, a.text
        #                     else:
        #                         print a.tag, a.attrib, a.text
        #         except:
        #             pass
        # returnData = ET.fromstring(r.text)
        # for i in tree.items():
        #     print "%s:%s" % (i[0], i[1])
        #     return ""


    def get_projects(self, verbose=None):
        '''
        :param verbose:
        :return: return a dictionary of projects that are currently available
        '''
        if verbose != True:
            verbose = False
        submitURL = self.baseURL + "project/all?" + str(verbose)

        r = requests.get(submitURL, auth=(self.username, self.password))
        # print r.status_code
        return r.text

    def put_project(self, projectId, projectName, startingNumber, projectLeadLogin, description=None):
        '''

        :param projectId: Unique STRING identifier for the project
        :param projectName: STRING name
        :param startingNumber: STRING integer for the first ticket number
        :param projectLeadLogin: STRING username to be assigned project leader
        :param description: Optional STRING description of the project
        :return: Undefined currently
        '''
        submitURL = self.baseURL + "admin/project/" + projectId + "?projectName=" + projectName + "&startingNumber=" \
                    + startingNumber + "&projectLeadLogin=" + projectLeadLogin
        if description != None:
            #Description has been defined so append it to our url
            submitURL += "&description=" + description

        r = requests.put(submitURL, auth=(self.username, self.password))
        message = "Your project: " + projectId + " returned: " + r.text
        return message   #This currently returns Nothing and status_code errors out despite the request succeeding...

    def delete_project(self, projectId):
        '''
        :param projectId: STRING the project ID to delete
        :return: a success message
        '''
        submitURL = self.baseURL + "admin/project/" + projectId
        r = requests.delete(submitURL, auth=(self.username, self.password))
        return r.text

    ### Issues ###
    def issues_add(self, project, summary, description=None, attachment=None, permittedGroup=None):
        '''
        #PUT /rest/issue?{project}&{summary}&{description}&{attachments}&{permittedGroup}
        :param project: STRING to define the project for the new issue
        :param summary: STRING "title" of the new issue
        :param description: STRING description of the issue
        :param attachment: Not Yet Available
        :param permittedGroup: STRING to set the visibility group
        :return: A message indicating success, ticket number, title and description otherwise failure
        '''
        submitURL = self.baseURL + "issue?project=" + project + "&summary=" + summary
        if description != None:
            submitURL += "&description=" + description
        # if attachment != None:
        #     submitURL += "&" + attachment
        # if permittedGroup != None:
        #     submitURL += "&" + permittedGroup

        #Submit the push request to create a ticket
        r = requests.put(submitURL, auth=(self.username, self.password))
        print r.status_code
        print r.text
        print r.headers
        print r.iter_lines