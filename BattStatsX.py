#! /usr/bin/python

import subprocess
import re
import time
import datetime

def secondsToHuman(totalTime):
	seconds = totalTime % 60
	totalTime /= 60
	minutes = totalTime % 60
	totalTime /= 60
	hours = totalTime

	return str(hours) + " Hours, " + str(minutes) + " Minutes and " + str(seconds) + " Seconds"

def unixToHuman(unixTime):
	return str(datetime.datetime.fromtimestamp(int(unixTime)).strftime('%Y-%m-%d %H:%M:%S'))


currentYear = datetime.datetime.now().year
currentTime = int(time.time())

PLUG_IN_FORMAT = '%Y %b %d %H:%M:%S'
WAKE_LOG_FORMAT = '%m/%d/%y, %I:%M:%S %p'

#call("pmset -g log | grep -E 'GMT\+?\s+(Wake|Sleep)\s+'")
pmsetOutput = subprocess.Popen(["syslog"], stdout = subprocess.PIPE).communicate()[0]
lines = pmsetOutput.splitlines()

lastPlugged = 0
lastUnplugged = 0
for line in lines:
	if line.find("magsafeStateChanged") != -1:
		if line.find("old 1 new 2") != -1:
			# Unplugged entry in log
			epoch = int(time.mktime(time.strptime(str(currentYear) + ' ' + line[:15], PLUG_IN_FORMAT)))
			lastUnplugged = epoch
		else:
			# Plugged entry in log
			epoch = int(time.mktime(time.strptime(str(currentYear) + ' ' + line[:15], PLUG_IN_FORMAT)))
			lastPlugged = epoch

pmsetOutput2 = subprocess.Popen(["pmset","-g","log"], stdout = subprocess.PIPE).communicate()[0]

lines = pmsetOutput2.splitlines()
raw_events = []
filtered_events = []

for line in lines:
	if re.search(r'GMT\+?\d?\s+(Wake|Sleep)\s+', line) != None:
		date_time = line[:line.find("GMT")-1]

		sleepTime = (line.find("Wake") == -1)
		
		epoch = int(time.mktime(time.strptime(date_time, WAKE_LOG_FORMAT)))
		#print epoch
		raw_events.append((epoch, sleepTime))


for i in range(1,len(raw_events)):
	if raw_events[i-1][1] != raw_events[i][1]:
		filtered_events.append(raw_events[i])

totalSleepTime = 0
currentSleepTime = -1
for event in filtered_events:
	if event[1] == True:
		currentSleepTime = max(event[0], lastUnplugged)
	if event[0] >= lastUnplugged:
		if currentSleepTime != -1 and event[1] == False:
			totalSleepTime += event[0] - currentSleepTime
			currentSleepTime = -1

totalUnpluggedTime = currentTime - lastUnplugged
totalBatteryUseTime = totalUnpluggedTime - totalSleepTime

print 'Total time since unplugged: ', secondsToHuman(totalUnpluggedTime)
print 'Total time on sleep: ', secondsToHuman(totalSleepTime)
print 'Total time on battery (Of actual use): ', secondsToHuman(totalBatteryUseTime)

