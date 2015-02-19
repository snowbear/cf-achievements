import json
import logging
import urllib.error, urllib.request
import requests
from time import *

from cf_api_enums import *

class STATIC:
    session = None

def get_response(request):
    url = "http://codeforces.com/api/" + request + "&lang=en"
    logging.info("Sending HTTP request to url: %s", url)
    if STATIC.session == None:
        STATIC.session = requests.session()
        # del STATIC.session.headers['Accept-Encoding']
    
    response = STATIC.session.get(url)
    if response.status_code == 429:
        logging.info("CF says 'Too many requests'. Sleeping for a moment...")
        sleep(1)
        return get_response(request)
    response = response.text
    response = json.loads(response)
        
    if response['status'] != 'OK': raise Exception("Error occured while retrieving data from CF: %s" % response['status'])
    result = response['result']
    logging.info("Got HTTP response")
    return result

def get_response_multi_page(request, key_getter):
    result = []
    page_size = 30000
    next_item = 1
    
    finished = False
    
    while not finished:
        current_page = get_response("%s&from=%d&count=%d" % (request , next_item , page_size))
        
        finished = len(current_page) < page_size
        
        if len(result) > 0:
            current_page.reverse()
            while len(current_page) > 0 and key_getter(current_page[len(current_page) - 1]) >= key_getter(result[len(result) - 1]):
                current_page.pop()
            current_page.reverse()
        
        result.extend(current_page)
        next_item = next_item + page_size
        
    return result

def get_problems(contest):
    response = get_response("contest.standings?contestId=%s&from=1&count=1" % contest.id)
    return response['problems']

def get_contest_participants(contest):
    page_size = 500000
    response = get_response("contest.standings?contestId=%d&from=1&count=%d&showUnofficial=true" % (contest.id , page_size))
    result = response['rows']
    assert(len(result) < page_size)
    return result
    
def get_problems(contest):
    response = get_response("contest.standings?contestId=%s&from=1&count=1" % contest.id)
    return response['problems']
    
def get_contests():
    return get_response("contest.list?gym=false")
         
def filter_party(party):
    return party.is_online

def get_hacks(contest):
    logging.info("Getting hacks...")
    result = get_response("contest.hacks?contestId=%d" % contest.id)
    for h in result:
        (h['hacker'] , h['defender']) = (h['defender'] , h['hacker'])
    return result

def get_submissions(contest):
    logging.info("Getting submissions...")
    result = get_response_multi_page("contest.status?contestId=%d" % contest.id , lambda js: js['id'])
    return result