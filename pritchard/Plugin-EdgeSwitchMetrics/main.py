from ubnt import UnifiSwitchClient
import json
import time
import requests
import csv
import datetime
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from collections import deque
import queue
import pprint
#from waggle.plugin import Plugin
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
wattagerecorders=[queue.Queue() for i in range(8)] #ceates list of 8 ques for different ports
#pluggschanged = [0] *8 #1=, something plugged in, 2= something unplugged
#pluggschanged= [0.0 for i in range(8)]

isoncurrent =  [False for i in range(8)] 
isonrecent =  [False for i in range(8)]
Averages = [0] * 8
Averages= [0.0 for i in range(8)]
Minimums = [0] * 8
Minimums = [150 for i in range(8)]#assumes that no port will have a higher minimum then 150 watts
Maximums = [0] * 8
Maximums = [0 for i in range(8)]

for y in range(5): #iterations set to 30 in fianl project
        with UnifiSwitchClient(
                host='https://192.168.0.5',
                username='ubnt',
                password='why1not2') as client:
                info = client.get_POE_info()
        data=json.loads(json.dumps(info))
        pp = pprint.PrettyPrinter(indent=2, width=30, compact=True)
        pp.pprint(data) #prints json prettily to screen
        first_elem= data[0]
        interfaces =first_elem['interfaces']
        for x in range(3): #iterates through each port, 8 in final
                poePower = interfaces[x]['statistics']['poePower']

                print (interfaces[x]['statistics']['poePower']) #this is the first POE reading, so 2.58
                if poePower!=0:#checks to see if anything currently plugged in
                                isoncurrent[x]= True
                else:
                                isoncurrent[x]= False
                if y==0:
                                wattagerecorders[x].put(isoncurrent[x]) #this puts the first value
                elif isonrecent[x]!=isoncurrent[x]:#isonoriginal[x]!=isoncurrent[x]:
                                wattagerecorders[x].put(datetime.datetime.now())
                                wattagerecorders[x].put(isoncurrent[x])
                                '''''
                                if isonoriginal[x]== True:
                                        pluggschanged[x]= 2 #something was unplugged at this port
                                else:
                                        pluggschanged[x]= 1 #something was plugged in at this port
                                '''   
                isonrecent[x]=isoncurrent[x]     
                if poePower<Minimums[x]: #compars and sets maximums and mins per port
                        Minimums[x]=poePower
                if poePower>Maximums[x]:
                        Maximums[x]=poePower
                Averages[x]=Averages[x]+(poePower-Averages[x])/(y+1) #rolling average calculation
                print ("port", x+1)
        print ("iterations=", y+1)
        time.sleep(1) #set to 10 in final project 

print (Averages[0])
print (Maximums[0])
print (Minimums[0])
#print (pluggschanged[0])
header = ['minimums', 'maximums', 'averages'] #,'pluggschanged', 'Started plugged in']
Port1 = [Minimums[0], Maximums[0], Averages[0]]#, pluggschanged[0], isonoriginal[0]]
header2 = ['started on', 'every time it changed', 'what it changed to each time']
firstque = wattagerecorders[0]
print (type(firstque))
que = list(firstque.queue)#wattagerecorders[0])
with open('edgeswitch.csv', 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerow(Port1)
        writer.writerow(header2)
        writer.writerow(que)

# questions about  if os.path.exists('testing.0.0.0'):

"""
with Plugin() as plugin:
        plugin.upload_file('edgeswitch', timestamp=str(datetime.now()))
"""
# Plugin.publish('test.bytes',self.parse())
#remeber to pass isonoriginal[] so plugging or unplugging at moment of testing can be detected


"""
                if y!=0
                       if isoncurrent[x]!=isonpast[x]
                        if (isonpast[x]&)
                                print("plugged in")
                        else
                """

"""
[{'device': {'cpu': [{'identifier': 'ARMv7 Processor rev 1 (v7l)',
                      'usage': 54}],
             'fanSpeeds': [],
             'power': [],
             'ram': {'free': 69324800, 'total': 262553600, 'usage': 73},
             'storage': [],
             'temperatures': [{'name': 'TEMP-1',
                               'type': 'other',
                               'value': 61.0},
                              {'name': 'TEMP-2',
                               'type': 'other',
                               'value': 64.0},
                              {'name': 'PoE-01',
                               'type': 'other',
                               'value': 49.0},
                              {'name': 'PoE-02',
                               'type': 'other',
                               'value': 51.0}],
             'uptime': 84676},
  'interfaces': [{'id': '0/1',
                  'name': '',
                  'statistics': {'bytes': 0,
                                 'dropped': 0,
                                 'errors': 0,
                                 'packets': 0,
                                 'poePower': 2.58,
                                 'pps': 0,
                                 'rate': 0,
                                 'rxBytes': 0,
                                 'rxErrors': 0,
                                 'rxPPS': 0,
                                 'rxPackets': 0,
                                 'rxRate': 0,
                                 'txBytes': 0,
                                 'txErrors': 0,
                                 'txPPS': 0,
                                 'txPackets': 0,
                                 'txRate': 0}},
"""
