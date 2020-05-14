from urllib import request, parse, error
import json

def lambda_handler(event, context):
    urls = event['subscribers']
    message = event['message']
    data = parse.urlencode(message).encode()
    failedAttempts = []
    for url in urls:
        try:
            makeRequestToURL(url, data, failedAttempts)
        except error.HTTPError as e:
            failedAttempts.append({'url': url, 'error': e})
    
    if len(failedAttempts) > 0:
        raise Exception({'errorMessage': 'Not all HTTP requests succeeded!', 'failedAttempts': failedAttempts})

def makeRequestToURL(url, data, failedAttempts):
    req =  request.Request(url, data=data)
    request.urlopen(req)