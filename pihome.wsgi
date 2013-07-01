"""
The WSGI script for our application.  It determines what other scripts need
to be run.
"""

import sys
import os
import os.path
import urlparse
import time
import threading

app_dir = os.path.dirname(__file__)
if app_dir not in sys.path:
    sys.path.append(app_dir)

#import logclient
#import tranclient
import socket

# Create singular socket connection to Log server for each Web-process
# This connection essentially creates one Log-thread for each web-process
#LogClient = logclient.LogClient()

# Create singular socket connection to Transaction server for each Web-process
# This connection essentially creates one Tran-thread for each web-process
#TranClient = tranclient.TranClient()

#semaphore = threading.Semaphore(1)

def abs_path(relative_path):
    """
    Get the absolute path for a path relative to this file.
    """
    return os.path.dirname(__file__) + os.sep + relative_path

def application(environ, start_response):
    #semaphore.acquire()

    # Determine what resource was requested
    request_path = environ["PATH_INFO"]
    sys.stderr.write("request_path: %s\n" % str(request_path))
    
    command = request_path[1:].upper()
    sys.stderr.write("command: %s\n" % str(command))
    
    # Get query parameters
    params = urlparse.parse_qs(environ["QUERY_STRING"])
    sys.stderr.write("params: %s\n" % str(params))
    
    # Try to extract out command parameters if existed, else assign empty string
    # Retrieve userid value
    try: userid = params["userid"][0]
    except KeyError: userid = ""
    # Retrieve stocksymbol value
    try: stocksymbol = params["stocksymbol"][0]
    except KeyError: stocksymbol = ""
    # Retrieve amount value
    try: amount = params["amount"][0]
    except KeyError: amount = ""
    # Retrieve filename value
    try: filename = params["filename"][0]
    except KeyError: filename = ""
    # Retrieve server hostname
    server=socket.gethostname()

    # Generic request template for transaction server including all possible parameter fields separated by ','
    tran_request = "%s,%s,%s,%s,%s" % (command, userid, stocksymbol, amount, filename)

    # Send logevent to logserver via logclient socket
    #LogClient.generate_user_command_log(time.time(), server, command, userid, stocksymbol, filename, amount)

    status = '200 OK'

    if command == "QUOTE":
        # Send logevent to logserver via logclient socket
        #LogClient.generate_user_command_log(time.time(), server, command, userid, stocksymbol, filename, amount)
        # Send generic transaction request to transerver via tranclient socket
        #TranClient.send(tran_request)
        sys.stderr.write("This is from QUOTE\n")

        output = '<b>This is QUOTE</b>'
        output = params.__str__()

    else:
        status = '404 Not Found'
        output = '<b>Page not found - Tri</b>'

    #semaphore.release()
    
    response_headers = [('Content-type', 'text/html'),
                        ('Content-Length', str(len(output)))]

    start_response(status, response_headers)
    return [output]

