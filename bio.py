

#def protein():
#
#	import requests
#
#	url = "https://blast.ncbi.nlm.nih.gov/Blast.cgi?PAGE=Proteins&PROGRAM=blastp&BLAST_PROGRAMS=blastp&PAGE_TYPE=BlastSearch&BLAST_SPEC=blast2seq"
#
#	headers = {
#    	'content-type': "application/json",
#    	'x-apikey': "560bd47058e7ab1b2648f4e7",
#    	'cache-control': "no-cache"
#    	}
#
#	response = requests.request("GET", url, headers=headers)
#
#	print(response.text)
#
#def gene():
#
#	import requests
#
#	url = "https://blast.ncbi.nlm.nih.gov/Blast.cgi?PAGE_TYPE=BlastSearch&BLAST_SPEC=blast2seq&LINK_LOC=align2seq"
#
#	headers = {
#   	'content-type': "application/json",
#    	'x-apikey': "560bd47058e7ab1b2648f4e7",
#   	'cache-control': "no-cache"
#    	}
#
#	response = requests.request("GET", url, headers=headers)
#
#	print(response.text)
#
#def main():
#	
#	user_input = input("Insert 1 for Protein or 2 for Nucleotide\n")
#	
#	
#	if user_input == '1':
#		protein()
#
#	else: gene()
#
#main()



#import urllib, json
#url = "https://blast.ncbi.nlm.nih.gov/Blast.cgi"
#response = urllib.urlopen(url)
#data = json.loads(response.read())
#print data

#!/usr/bin/env python
 

import json, requests, urllib2, os, platform
from xmltramp2 import xmltramp

debugLevel = 0

seq = "ATTGACCTGA"

URL = "http://www.ebi.ac.uk/Tools/services/rest/ncbiblast"

def printDebugMessage(functionName, message, level):
    if(level <= debugLevel):
        print >>sys.stderr, '[' + functionName + '] ' + message


def restRequest(url):
    printDebugMessage('restRequest', 'Begin', 11)
    printDebugMessage('restRequest', 'url: ' + url, 11)
    try:
        # Set the User-agent.
        user_agent = getUserAgent()
        http_headers = { 'User-Agent' : user_agent }
        req = urllib2.Request(url, None, http_headers)
        # Make the request (HTTP GET).
        reqH = urllib2.urlopen(req)
        result = reqH.read()
        reqH.close()
    # Errors are indicated by HTTP status codes.
    except urllib2.HTTPError, ex:
        # Trap exception and output the document to get error message.
        print >>sys.stderr, ex.read()
        raise
    printDebugMessage('restRequest', 'End', 11)
    return result

# User-agent for request (see RFC2616).
def getUserAgent():
    printDebugMessage('getUserAgent', 'Begin', 11)
    # Agent string for urllib2 library.
    urllib_agent = 'Python-urllib/%s' % urllib2.__version__
    clientRevision = '$Revision: 2673 $'
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

# Get input parameters list
def serviceGetParameters():
    printDebugMessage('serviceGetParameters', 'Begin', 1)
    requestUrl = 	URL + '/parameters'
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
        print id
    printDebugMessage('printGetParameters', 'End', 1)

# Get input parameter information
def serviceGetParameterDetails(paramName):
    printDebugMessage('serviceGetParameterDetails', 'Begin', 1)
    printDebugMessage('serviceGetParameterDetails', 'paramName: ' + paramName, 2)
    requestUrl = URL + '/parameterdetails/' + paramName
    printDebugMessage('serviceGetParameterDetails', 'requestUrl: ' + requestUrl, 2)
    xmlDoc = restRequest(requestUrl)
    doc = xmltramp.parse(xmlDoc)
    printDebugMessage('serviceGetParameterDetails', 'End', 1)
    return doc

# Print description of a parameter
def printGetParameterDetails(paramName):
    printDebugMessage('printGetParameterDetails', 'Begin', 1)
    doc = serviceGetParameterDetails(paramName)
    print str(doc.name) + "\t" + str(doc.type)
    print doc.description
    for value in doc.values:
        print value.value,
        if str(value.defaultValue) == 'true':
            print 'default',
        print
        print "\t" + str(value.label)
        if(hasattr(value, 'properties')):
            for wsProperty in value.properties:
                print  "\t" + str(wsProperty.key) + "\t" + str(wsProperty.value)
    #print doc
    printDebugMessage('printGetParameterDetails', 'End', 1)



print(restRequest(URL))
print(getUserAgent())
print(serviceGetParameters())
print(printGetParameters())
print(serviceGetParameterDetails("program"))
print(printGetParameterDetails("program"))


#PARAMS = {
#	'program':"blastp",
#  	'stype':"protein",
#  	'sequence':seq,
#  	'database':"uniprotkb",
#}
 
# sending get request and saving the response as response object
#r = requests.get(url = URL, params = PARAMS)

#data = r.json()


#https://api.github.com/events

#r = requests.get('https://www.ncbi.nlm.nih.gov/home/develop/api/')

#r.

#r = requests.post('http://httpbin.org/post', data = {'key':'value'})

#r = requests.put('http://httpbin.org/put', data = {'key':'value'})

#r = requests.delete('http://httpbin.org/delete')

#r = requests.head('http://httpbin.org/get')

#r = requests.options('http://httpbin.org/get')

