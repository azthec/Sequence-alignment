# Load libraries
import platform, os, re, sys, time, urllib.request, urllib.parse, urllib.error, urllib.request, urllib.error, urllib.parse
from xmltramp2 import xmltramp
from optparse import OptionParser

baseUrl = 'placeholder global'
email1 = 'up201103891@fc.up.pt'
title1 = 'fcup bioinformatics'

# Set interval for checking status
checkInterval = 10
# Output level
outputLevel = 1
# Debug level
debugLevel = 2

# Debug print
def printDebugMessage(functionName, message, level):
    if(level <= debugLevel):
        print('[' + functionName + '] ' + message, file=sys.stderr)

# User-agent for request (see RFC2616).
def getUserAgent():
    printDebugMessage('getUserAgent', 'Begin', 11)
    # Agent string for urllib2 library.
    urllib_agent = 'Python-urllib/%s' % urllib.request.__version__
    clientRevision = '$Revision: 2809 $'
    clientVersion = '0'
    if len(clientRevision) > 11:
        clientVersion = clientRevision[11:-2]
    # Prepend client specific agent string.
    user_agent = 'EBI-Sample-Client/%s (%s; Python %s; %s) %s' % (
        clientVersion, os.path.basename( __file__ ),
        platform.python_version(), platform.system(),
        urllib_agent
    )
    printDebugMessage('getUserAgent', 'user_agent: ' + user_agent, 12)
    printDebugMessage('getUserAgent', 'End', 11)
    return user_agent

# Wrapper for a REST (HTTP GET) request
def restRequest(url):
    printDebugMessage('restRequest', 'Begin', 11)
    printDebugMessage('restRequest', 'url: ' + url, 11)
    # Errors are indicated by HTTP status codes.
    try:
        # Set the User-agent.
        user_agent = getUserAgent()
        http_headers = { 'User-Agent' : user_agent }
        req = urllib.request.Request(url, None, http_headers)
        # Make the request (HTTP GET).
        reqH = urllib.request.urlopen(req)
        result = reqH.read()
        reqH.close()
    # Errors are indicated by HTTP status codes.
    except urllib.error.HTTPError as ex:
        # Trap exception and output the document to get error message.
        print(ex.read(), file=sys.stderr)
        raise
    printDebugMessage('restRequest', 'End', 11)
    return result

# Get input parameters list
def serviceGetParameters():
    printDebugMessage('serviceGetParameters', 'Begin', 1)
    requestUrl = baseUrl + '/parameters'
    printDebugMessage('serviceGetParameters', 'requestUrl: ' + requestUrl, 2)
    xmlDoc = restRequest(requestUrl)
    doc = xmltramp.parse(xmlDoc)
    printDebugMessage('serviceGetParameters', 'End', 1)
    return doc['id':]

# Print list of parameters
def printGetParameters():
    printDebugMessage('printGetParameters', 'Begin', 1)
    idList = serviceGetParameters()
    for id in idList:
        print(id)
    printDebugMessage('printGetParameters', 'End', 1)    

# Get input parameter information
def serviceGetParameterDetails(paramName):
    printDebugMessage('serviceGetParameterDetails', 'Begin', 1)
    printDebugMessage('serviceGetParameterDetails', 'paramName: ' + paramName, 2)
    requestUrl = baseUrl + '/parameterdetails/' + paramName
    printDebugMessage('serviceGetParameterDetails', 'requestUrl: ' + requestUrl, 2)
    xmlDoc = restRequest(requestUrl)
    doc = xmltramp.parse(xmlDoc)
    printDebugMessage('serviceGetParameterDetails', 'End', 1)
    return doc

# Print description of a parameter
def printGetParameterDetails(paramName):
    printDebugMessage('printGetParameterDetails', 'Begin', 1)
    doc = serviceGetParameterDetails(paramName)
    print(str(doc.name) + "\t" + str(doc.type))
    print(doc.description)
    for value in doc.values:
        print(value.value, end=' ')
        if str(value.defaultValue) == 'true':
            print('default', end=' ')
        print()
        print("\t" + str(value.label))
        if(hasattr(value, 'properties')):
            for wsProperty in value.properties:
                print("\t" + str(wsProperty.key) + "\t" + str(wsProperty.value))
    #print doc
    printDebugMessage('printGetParameterDetails', 'End', 1)

# Submit job
def serviceRun(email, title, params):
    printDebugMessage('serviceRun', 'Begin', 1)
    # Insert e-mail and title into params
    params['email'] = email
    if title:
        params['title'] = title
    requestUrl = baseUrl + '/run/'
    printDebugMessage('serviceRun', 'requestUrl: ' + requestUrl, 2)
    # Signature methods requires special handling (list)
    applData = ''
    if 'appl' in params:
        # So extract from params
        applList = params['appl']
        del params['appl']
        # Build the method data options
        for appl in applList:
            applData += '&appl=' + appl
    # Get the data for the other options
    requestData = urllib.parse.urlencode(params)
    # Concatenate the two parts.
    requestData += urllib.parse.urlencode(applData)
    requestData = requestData.encode('utf-8')
    printDebugMessage('serviceRun', 'requestData: ' + str(requestData), 2)
    # Errors are indicated by HTTP status codes.
    try:
        # Set the HTTP User-agent.
        user_agent = getUserAgent()
        http_headers = { 'User-Agent' : user_agent }
        req = urllib.request.Request(requestUrl, None, http_headers)
        # Make the submission (HTTP POST).
        reqH = urllib.request.urlopen(req, requestData)
        jobId = reqH.read()
        reqH.close()
    except urllib.error.HTTPError as ex:
        # Trap exception and output the document to get error message.
        print(ex.read(), file=sys.stderr)
        raise
    printDebugMessage('serviceRun', 'jobId: ' + str(jobId), 2)
    printDebugMessage('serviceRun', 'End', 1)
    return jobId

# Get job status
def serviceGetStatus(jobId):
    printDebugMessage('serviceGetStatus', 'Begin', 1)
    printDebugMessage('serviceGetStatus', 'jobId: ' + str(jobId), 2)
    requestUrl = baseUrl + '/status/' + str(jobId).strip("b").strip("\'")
    # requestUrl = urllib.parse.quote_plus(requestUrl)
    printDebugMessage('serviceGetStatus', 'requestUrl: ' + str(requestUrl), 2)
    status = restRequest(requestUrl)
    printDebugMessage('serviceGetStatus', 'status: ' + str(status), 2)
    printDebugMessage('serviceGetStatus', 'End', 1)
    return status

# Print the status of a job
def printGetStatus(jobId):
    printDebugMessage('printGetStatus', 'Begin', 1)
    status = serviceGetStatus(jobId)
    print(status)
    printDebugMessage('printGetStatus', 'End', 1)
    

# Get available result types for job
def serviceGetResultTypes(jobId):
    printDebugMessage('serviceGetResultTypes', 'Begin', 1)
    printDebugMessage('serviceGetResultTypes', 'jobId: ' + str(jobId), 2)
    requestUrl = baseUrl + '/resulttypes/' + str(jobId).strip("b").strip("\'")
    printDebugMessage('serviceGetResultTypes', 'requestUrl: ' + requestUrl, 2)
    xmlDoc = str(restRequest(requestUrl)).strip("b").strip("\'")
    doc = xmltramp.parse(xmlDoc)
    printDebugMessage('serviceGetResultTypes', 'End', 1)
    return doc['type':]

# Print list of available result types for a job.
def printGetResultTypes(jobId):
    printDebugMessage('printGetResultTypes', 'Begin', 1)
    resultTypeList = serviceGetResultTypes(jobId)
    for resultType in resultTypeList:
        print(resultType['identifier'])
        if(hasattr(resultType, 'label')):
            print("\t", resultType['label'])
        if(hasattr(resultType, 'description')):
            print("\t", resultType['description'])
        if(hasattr(resultType, 'mediaType')):
            print("\t", resultType['mediaType'])
        if(hasattr(resultType, 'fileSuffix')):
            print("\t", resultType['fileSuffix'])
    printDebugMessage('printGetResultTypes', 'End', 1)

# Get result
def serviceGetResult(jobId, type_):
    printDebugMessage('serviceGetResult', 'Begin', 1)
    printDebugMessage('serviceGetResult', 'jobId: ' + jobId, 2)
    printDebugMessage('serviceGetResult', 'type_: ' + type_, 2)
    requestUrl = baseUrl + '/result/' + str(jobId ).strip('b').strip("\'") + '/' + type_
    result = restRequest(requestUrl)
    printDebugMessage('serviceGetResult', 'End', 1)
    return result

# Client-side poll
def clientPoll(jobId):
    printDebugMessage('clientPoll', 'Begin', 1)
    result = 'PENDING'
    while result == 'RUNNING' or result == 'PENDING':
        result = serviceGetStatus(jobId)
        print(result, file=sys.stderr)
        if result == 'RUNNING' or result == 'PENDING':
            time.sleep(checkInterval)
    printDebugMessage('clientPoll', 'End', 1)

# Get result for a jobid
def getResult(jobId):
    printDebugMessage('getResult', 'Begin', 1)
    printDebugMessage('getResult', 'jobId: ' + str(jobId), 1)
    # Check status and wait if necessary
    clientPoll(jobId)
    # Get available result types
    resultTypes = serviceGetResultTypes(jobId)

    output = ''
    counter = 0
    for resultType in resultTypes:
        if counter == 3:
            break
        counter += 1
        # Derive the filename for the result
        filename = str(jobId).strip("b").strip("\'") + '.' + str(resultType['identifier']) + '.' + str(resultType['fileSuffix'])

        # Get the result
        result = serviceGetResult(str(jobId).strip("b").strip("\'"), str(resultType['identifier']))
        result = str(result).strip("b").strip("\'").replace('\\n', '\n')
        if counter == 0:
            output = result
        else:
            output += '\n\n' + result

    printDebugMessage('getResult', 'End', 1)

    return output

def get_alignment(sequence1, sequence2, tipo, email1, title1):
    # No options... print help.
    params = {}
    
    params['asequence'] = sequence1
    params['bsequence'] = sequence2
    # Booleans need to be represented as 1/0 rather than True/False
    # Add the other options (if defined)
    params['stype'] = tipo
    # Submit the job
    jobid = serviceRun(email1, title1, params)
    print(jobid, file=sys.stderr)
    time.sleep(5)
    return getResult(jobid)

def emboss_smith_waterman(sequence1, sequence2, seq_type):
    global baseUrl
    baseUrl = 'http://www.ebi.ac.uk/Tools/services/rest/emboss_water'
    return get_alignment(sequence1, sequence2, seq_type, email1, title1)

def emboss_needleman_wunsch(sequence1, sequence2, seq_type):
    global baseUrl
    baseUrl = 'http://www.ebi.ac.uk/Tools/services/rest/emboss_needle'
    return get_alignment(sequence1, sequence2, seq_type, email1, title1)

def emboss_stretcher(sequence1, sequence2, seq_type):
    global baseUrl
    baseUrl = 'http://www.ebi.ac.uk/Tools/services/rest/emboss_stretcher'
    return get_alignment(sequence1, sequence2, seq_type, email1, title1)

def emboss_matcher(sequence1, sequence2, seq_type):
    global baseUrl
    baseUrl = 'http://www.ebi.ac.uk/Tools/services/rest/emboss_matcher'
    return get_alignment(sequence1, sequence2, seq_type, email1, title1)


# emboss_smith_waterman("ATTGACCTGA","ATCCTGA","protein")
# emboss_needleman_wunsch("ATTGACCTGA","ATCCTGA","protein")
# emboss_stretcher("ATTGACCTGA","ATCCTGA","protein")
# emboss_matcher("ATTGACCTGA","ATCCTGA","protein")
