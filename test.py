##use this script
##This script has modified noise filter rather than frequency filter
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, sys, math, select
import time as tm
import datetime
import warnings
import tempfile

from feature_extraction import filters as fil
from feature_extraction import lpcgen as lpg
from feature_extraction import calcspectrum as csp
from feature_extraction import harmonics as hmn
from feature_extraction import fextract as fex
from feature_extraction import parsedata as par
from feature_extraction.getconfi import logdata
from feature_extraction.apicall import apicalls
from feature_extraction.specsub import reduce_noise

import pickle

######################################################################################################
global itervalue #I used this when I needed to get only a certain number o iterations
itervalue = 0

def dist_prediction_label(value):
    if value == 0:
        label = "far"
    elif value == 1:
        label = "midrange"
    elif value == 2:
        label = "near"
    elif value == 3:
        label = "vfar or nodrone"
    elif value == 4:
        label = "vnear"
    return label

######################################################################################################################
"""set api and initiate calls"""
# api_url = 'http://mlc67-cmp-00.egr.duke.edu/api/events' ##This is dukes server which Chunge created
api_url = 'http://mlc67-cmp-00.egr.duke.edu/api/gardens' ##This is garden server  

apikey = None
push_url = "https://onesignal.com/api/v1/notifications"
pushkey = None
sound_url = 'http://mlc67-cmp-00.egr.duke.edu/api/soundInfos'
soundkey = None
wav_url = ' http://mlc67-cmp-00.egr.duke.edu/api/sound-clips/gardens/upload'
wavkey = None
LOCATION = "Drone Detector A"
send = apicalls(api_url,apikey, push_url,pushkey, sound_url, soundkey, wav_url,wavkey, LOCATION)##This initiates the push notification and mongodb database

i = 0
bandpass = [600,10000]#filter unwanted frequencies
prev_time= tm.time()#initiate time
reccount = 0
basename = "drone"

"""main code"""
try:#don't want useless user warnings
    fileName = 'drone_test.wav'
    output = { 
            'Timestamp': str(datetime.datetime.now())[:-7], 
            'Label': "2", # near
            'Occurance': "", 
            'Confidence': 33,
            'fileName' : fileName }

    print('sent %s'% int(output['Label']))
    send.sendtoken(output)#This line sends the log to srver(recent detection with confidence)
    prev_time = tm.time()
    if int(output['Label']) == int(4) or int(output['Label']) == int(2):
        send.push_notify(fileName)#when drone is detected this sends push notification to user in his app
        #if reccount == 0:
        #    suffix = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
        print("pushed %s"% int(output['Label']))
        #win.addstr(8,5,"Data Sent!")
        send.wavsendtoken(fileName)        
    #recording for 10 secs:
    # if reccount > 0 and reccount < 12:
    #     recdata = np.concatenate([recdata, data])
    #     np.seterr(divide='ignore', invalid='ignore')
    #     recscaled = np.int16(recdata/np.max(np.abs(recdata)) * 32767)
    #     reccount += 1
    #     if reccount == 11:
    #         sfilename = "_".join([basename, suffix])+".wav" # e.g. 'mylogfile_120508_171442'
    #         #np.save(tf.name,recscaled)
    #         wavf.write(sfilename, fs, recscaled)
    #         send.infosendtoken(output, sfilename)
    #         send.wavsendtoken(sfilename)
    #         print("file succesfully uploaded to server!")
    #         os.remove(sfilename)
    #         recdata = np.array([],dtype="float32")
    #         reccount = 0

except KeyboardInterrupt:
    pass


print('iter_num:',i)

