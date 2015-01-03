# README #

This Readme will soon detail full use and integration of PyTrack!

# Requirements #
* Python 2.7
* python requests
        
        pip install requests

*Youtrack 4.0 or later should be fine


# Usage #

    from pytrack import pytrack
    p = pytrack(<YOUTRACK_URL>, <PORT>, <USERNAME>, <PASSWORD>)

## Methods ##
*add_comment
*get_time
*add_time
*delete_time(Not Working yet)
*get_projects

From here you can call the various methods providing you include the appropriate request data.