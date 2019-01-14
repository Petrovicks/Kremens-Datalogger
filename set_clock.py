from test_wifi import *
import DS1307
from i2cDetect import *
import ntplib, datetime

internet = internet_on()
for i in range(128):
    clockCheck = i2cDetect(i)
    if clockCheck:
	break
    
timeCheck = False
if clockCheck:
    clock = DS1307.DS1307(1, 0x68)
    if internet:
        print("Can open google.com; setting RTC to NTP time.")
        #clock.write_now()
        ntpc = ntplib.NTPClient()
        clock.write_datetime(datetime.datetime.utcfromtimestamp(ntpc.request('europe.pool.ntp.org').tx_time))
        print('RTC sucessfully set')
        timeCheck = True
    #Check clock is up to date
    try:
        t1 = clock.read_datetime()
        print("Time read from RTC:",t1.strftime("%Y-%m-%d %H:%M:%S"))
        t1 = t1.timetuple()
        if t1[0] < 2017:
            print('Failed to updated RTC')
        else:
            if timeCheck == True:
                print('RTC is reset and up to date')
            else:
                print('RTC was not reset but was up to date as of last reset')
    except:
        print('Failed to read RTC to check time')
else:
    print('Failed to find RTC')
