#!/usr/bin/env python3
import subprocess
import datetime
import sched, time


s = sched.scheduler(time.time, time.sleep)
def getImage(sc): 
    timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    script = 'ffmpeg -y -i rtmp://wzmedia.dot.ca.gov:1935/D4/W80_at_Carlson_Blvd_OFR.stream -vframes 1 ' + 'input/' + timestamp + '.jpg'

    subprocess.call(script, shell=True)
    s.enter(1, 1, getImage, (sc,))

s.enter(1, 1, getImage, (s,))
s.run()
