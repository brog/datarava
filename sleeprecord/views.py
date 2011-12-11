# Create your views here.
from django.http import HttpResponse
from django.template import Context, loader
from sleeprecord.models import Sleeprecord
from django.db.models import  Avg, StdDev
from django.conf import settings
import urllib2
import json
import re
import base64
import io
#import pickle
from urlparse import urlparse
import time, datetime
from django.contrib.auth.decorators import login_required
import logging
logger = logging.getLogger('datarava')

@login_required
def index(request): 
    if request.user.is_authenticated():
        # Do something for authenticated users.
        user_id = request.user.id
         
        sleep_records = Sleeprecord.objects.filter(user_id=user_id).order_by('-sleepgraphstarttime').all()
        sleep_aggs = Sleeprecord.objects.filter(user_id=user_id).all().aggregate(Avg('zq'), StdDev('zq'))
        #logger.error('testteststs')
	
        t = loader.get_template('sleeprecord/index.html')
        c = Context({
            'sleep_records' : sleep_records, 
            'sleep_aggs' : sleep_aggs,
            'MEDIA_URL' : settings.MEDIA_URL,
            'user' : request.user, 

        })

    else:
        # Do something for anonymous users.
        t = loader.get_template('sleeprecord/index.html')
        c = Context({
            'sleep_records' : None, 
            'sleep_aggs' : None,
            'MEDIA_URL' : settings.MEDIA_URL,
            'user' : None, 
        })

    return HttpResponse(t.render(c))

@login_required
def updatemydata(request):
    if request.user.is_authenticated():
        
        logger.debug('lets update my data')
        # Do something for authenticated users.
        userid = request.user.id    
        time_format = "%m-%d-%Y %H:%M:%S"   
        try:
            most_recent_local = Sleeprecord.objects.filter(user_id=userid).order_by('-sleepgraphstarttime')[0]
            most_recent_local = most_recent_local.sleepgraphstarttime
            most_recent_local_string = most_recent_local.strftime("%Y-%m-%d")
        except IndexError, e:
            most_recent_local_string = "1999-01-01"
            most_recent_local = datetime.datetime(1999,01,01)
        #d.strftime("%d/%m/%y")
        most_recent_remote= datetime.datetime.fromtimestamp(time.mktime(time.strptime(getMostRecentSleepRecord(userid, request.user), time_format)))
        update_or_not = ''
        #most_recent_remote = timestring = "2005-09-01 12:30:09"
        if most_recent_local < most_recent_remote :
            update_or_not = getDatesWithSleepDataInRange(most_recent_local_string, request.user) 
            sync_with_db(update_or_not, userid, request.user)
        else:
            update_or_not = 'not'


        t = loader.get_template('sleeprecord/updatemydata.html')
        c = Context({
        'update_data_type' : 'Sleeprecord',
        'userid' : userid,
        'most_recent_local' : most_recent_local,
        'most_recent_remote': most_recent_remote,
        'update_or_not' : update_or_not, 
        'MEDIA_URL' : settings.MEDIA_URL
        })
    else:
        t = loader.get_template('sleeprecord/updatemydata.html')
        c = Context({
        'update_data_type' : 'Sleeprecord',
        'userid' : None,
        'most_recent_local' : None,
        'most_recent_remote': None,
        'update_or_not' : 'not', 
        'MEDIA_URL' : settings.MEDIA_URL
        })

    return HttpResponse(t.render(c))

def sync_with_db(update_or_not, userid, user):
    datelist = update_or_not['response']['dateList']['date']
    print datelist
    for date in datelist:
        something = 'something'
        sleepRecord = callZeoApi('getSleepRecordForDate', user, month=date['month'],day=date['day'],year=date['year'])
        #sleepRecord['response']['sleepRecord']['startDate']
        ########
        t = sleepRecord['response']['sleepRecord']['bedTime']
        bedtime = datetime.datetime(t['year'],t['month'],t['day'],t['hour'],t['minute'],t['second'])
        
        t = sleepRecord['response']['sleepRecord']['riseTime']
        risetime = datetime.datetime(t['year'],t['month'],t['day'],t['hour'],t['minute'],t['second'])
        
        t = sleepRecord['response']['sleepRecord']['startDate']
        startdate = datetime.date(t['year'],t['month'],t['day'])
        
        t = sleepRecord['response']['sleepRecord']['sleepGraphStartTime']
        sleepgraphstarttime = datetime.datetime(t['year'],t['month'],t['day'],t['hour'],t['minute'],t['second'])
        #a if b else c 
        #<true value> if <conditional> else <false value>
        #I'm going to use this in order to set a default value for all of these sleeprecord objects (except user id)
        
        #grouping constants... maybe these go in a model somewhere?
        grouping = ""
        g = sleepRecord['response']['sleepRecord']['grouping']
        if   g == 'COMBINED':
            grouping = 1
        elif g == 'DAILY':
            grouping = 2
        elif g == 'WEEKLY':
            grouping = 3
        elif g == 'MONTHLY':
            grouping = 4
        else:
            grouping = 999

        #alarmreason constants .... maybe these go in a model somewhere?
        alarmreason = "" 
        a = sleepRecord['response']['sleepRecord']['alarmReason'] 
        if a=='REM_TO_NON_REM_TRANSITION':
            alarmreason = 1
        elif a=='NON_REM_TO_REM_TRANSITION':
            alarmreason = 2
        elif a=='WAKE':
            alarmreason = 3
        elif a=='DEEP_RISING':
            alarmreason = 4
        elif a=='END_OF_WAKE_WINDOW':
            alarmreason = 5
        elif a=='NO_ALARM':
            alarmreason = 6
        else:
            alarmreason = 999	


        sr = Sleeprecord( 
        user_id = userid, 
        awakenings = sleepRecord['response']['sleepRecord']['awakenings'] if 'awakenings' in sleepRecord['response']['sleepRecord'] else None, 
        awakeningszqpoints = sleepRecord['response']['sleepRecord']['awakeningsZqPoints'] if 'awakeningsZqPoints' in sleepRecord['response']['sleepRecord'] else None, 
        bedtime = bedtime if bedtime else None, 
        grouping = grouping if 'grouping' in sleepRecord['response']['sleepRecord'] else None, 
        morningfeel = sleepRecord['response']['sleepRecord']['morningFeel'] if 'morningFeel' in sleepRecord['response']['sleepRecord'] else None, 
        risetime = risetime if risetime else None, 
        startdate = startdate if startdate else None, 
        timeindeep = sleepRecord['response']['sleepRecord']['timeInDeep'] if 'timeInDeep' in sleepRecord['response']['sleepRecord'] else None, 
        timeindeeppercentage = sleepRecord['response']['sleepRecord']['timeInDeepPercentage'] if 'timeInDeepPercentage' in sleepRecord['response']['sleepRecord'] else None, 
        timeindeepzqpoints = sleepRecord['response']['sleepRecord']['timeInDeepZqPoints'] if 'timeInDeepZqPoints' in sleepRecord['response']['sleepRecord'] else None,
        timeinlight = sleepRecord['response']['sleepRecord']['timeInLight'] if 'timeInLight' in sleepRecord['response']['sleepRecord']  else None,
        timeinlightpercentage = sleepRecord['response']['sleepRecord']['timeInLightPercentage'] if 'timeInLightPercentage' in sleepRecord['response']['sleepRecord']  else None,
        timeinlightzqpoints = sleepRecord['response']['sleepRecord']['timeInLightZqPoints'] if 'timeInLightZqPoints' in sleepRecord['response']['sleepRecord'] else 0,
        timeinrem = sleepRecord['response']['sleepRecord']['timeInRem'] if 'timeInRem' in sleepRecord['response']['sleepRecord'] else None,
        timeinrempercentage = sleepRecord['response']['sleepRecord']['timeInRemPercentage'] if 'timeInRemPercentage' in sleepRecord['response']['sleepRecord'] else None,
        timeinremzqpoints = sleepRecord['response']['sleepRecord']['timeInRemZqPoints'] if 'timeInRemZqPoints' in sleepRecord['response']['sleepRecord'] else None,
        timeinwake = sleepRecord['response']['sleepRecord']['timeInWake'] if 'timeInWake' in sleepRecord['response']['sleepRecord']  else None,
        timeinwakepercentage = sleepRecord['response']['sleepRecord']['timeInWakePercentage'] if 'timeInWakePercentage' in sleepRecord['response']['sleepRecord']  else None,
        timeinwakezqpoints = sleepRecord['response']['sleepRecord']['timeInWakeZqPoints'] if 'timeInWakeZqPoints' in sleepRecord['response']['sleepRecord']  else None,
        timetoz = sleepRecord['response']['sleepRecord']['timeToZ'] if 'timeToZ' in sleepRecord['response']['sleepRecord']  else None,
        totalz = sleepRecord['response']['sleepRecord']['totalZ'] if 'totalZ' in sleepRecord['response']['sleepRecord'] else None,
        totalzzqpoints = sleepRecord['response']['sleepRecord']['totalZZqPoints'] if sleepRecord['response']['sleepRecord']['totalZZqPoints'] else None,
        zq = sleepRecord['response']['sleepRecord']['zq'] if 'zq' in sleepRecord['response']['sleepRecord'] else None,
        alarmreason = alarmreason if 'alarmReason' in sleepRecord['response']['sleepRecord']  else None,
        alarmringindex = sleepRecord['response']['sleepRecord']['alarmRingIndex'] if 'alarmRingIndex' in sleepRecord['response']['sleepRecord'] else None,
        dayfeel = sleepRecord['response']['sleepRecord']['dayFeel'] if 'dayFeel' in sleepRecord['response']['sleepRecord']  else None,
        sleepgraph = sleepRecord['response']['sleepRecord']['sleepGraph'] if 'sleepGraph' in sleepRecord['response']['sleepRecord']  else None,
        sleepgraphstarttime = sleepgraphstarttime if sleepgraphstarttime else None,
        sleepstealerscore = sleepRecord['response']['sleepRecord']['sleepStealerScore'] if 'sleepStealerScore' in sleepRecord['response']['sleepRecord']  else None,
        wakewindowendindex = sleepRecord['response']['sleepRecord']['wakeWindowEndIndex'] if 'wakeWindowEndIndex' in sleepRecord['response']['sleepRecord']  else None,
        wakewindowshow = sleepRecord['response']['sleepRecord']['wakeWindowShow'] if 'wakeWindowShow' in sleepRecord['response']['sleepRecord']  else None, 
        wakewindowstartindex = sleepRecord['response']['sleepRecord']['wakeWindowStartIndex'] if 'wakeWindowStartIndex' in sleepRecord['response']['sleepRecord']  else None
        )
        
        sr.save()

    return "something"

def callZeoApi(method, user, *args, **kwargs):
    apikey = "09AF4677D82B1511F538FAF51E69BD67"
    referrer = "http://themattnicole.com"
    zeologin = user.get_profile().zeologin
    zeopass = user.get_profile().zeopass
    
    logger.error('zeologin: %s | zeopass: %s' % (zeologin, zeopass ))
    
    #username = "d43pan@gmail.com"
    #password = "SHOCKORR4"
    username = zeologin
    password = zeopass
    host = "api.myzeo.com:8443"
    baseUrl = "zeows/api/v1/json/sleeperService"
    accept_header_json = "application/json"
    url = ""

    #method = "getLatestSleepRecord"
    #if the method passed in takes any other query parameters then add them to the url
    if method == 'getSleepRecordForDate':
        url = "https://%s/%s/%s?key=%s&date=%s-%s-%s" % (host, baseUrl,method,apikey,kwargs['year'],kwargs['month'],kwargs['day'])
    elif method == 'getDatesWithSleepDataInRange':
        url = "https://%s/%s/%s?key=%s&dateFrom=%s" % (host, baseUrl,method,apikey,kwargs['dateFrom'])
    else:
        url = "https://%s/%s/%s?key=%s" % (host, baseUrl,method,apikey) 

    # create the request
    request = urllib2.Request(url, None, {'Referer': referrer})
    # create the base64string for basic auth
    base64string = base64.encodestring('%s:%s' % (username, password))[:-1]
    # create the auth header
    authheader =  "Basic %s" % base64string
    # add the auth header
    request.add_header("Authorization", authheader)
    #debug line - print the desired url if you'd like
    #print "calling url: " + url + "\n"
    # call the URL
    response = urllib2.urlopen(request)
    results = json.load(response)
    return results
    
def getMostRecentSleepRecord(userid, user, *args, **kwargs):
    results = callZeoApi('getLatestSleepRecord', user)
    startDateTime = "%d-%d-%d %d:%d:%d" % (results['response']['sleepRecord']['sleepGraphStartTime']['month'],results['response']['sleepRecord']['sleepGraphStartTime']['day'],results['response']['sleepRecord']['sleepGraphStartTime']['year'],results['response']['sleepRecord']['sleepGraphStartTime']['hour'],results['response']['sleepRecord']['sleepGraphStartTime']['minute'],results['response']['sleepRecord']['sleepGraphStartTime']['second'])
    return startDateTime

def getDatesWithSleepDataInRange(dateFrom, user, *args, **kwargs):
    kwargs = {"dateFrom":dateFrom}
    results = callZeoApi('getDatesWithSleepDataInRange', user, **kwargs)
    #dateFrom e.g. 2010-01-01
    
    return results
    
