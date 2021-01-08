import json
import sys
import os
import math as m
import Environments as e

#https://stackoverflow.com/questions/1176136/convert-string-to-python-class-object
#This takes a str and convert to an object
#have to set a variable equal to it then run the variable
#this may be kinda jank but idc. it works for what I'm doing
def strToClass(classname):
    return getattr(sys.modules[__name__], classname)

def getFile():
    notValid = True
    fileName = None
    while (notValid):
        fileName = input("Enter the full name of the file: ")
        if (os.path.exists(fileName)):
            notValid = False
        else:
            print("Error: File does not exist in this location.")
    return fileName
    
def getEffectData():
    effectMarks = []
    for x in diff['_customData']['_bookmarks']:
        if x['_name'][0] == "/":
            effectMark = []
            temp = x['_name'].split()
            effectMark.append(strToClass(temp[0][1:]))
            data = [x['_time']]
            for i in range(1, len(temp)):
                data.append(temp[i])
            effectMark.append(data)
            effectMarks.append(effectMark)
    return effectMarks
            
    

def main():
    global diff
    #diffFileName = getFile()
    diffFileName = "HardStandard.dat" #temp for testing
    diffFile = open(diffFileName, "r")
    diff = json.load(diffFile)
    diffFile.close()
    for x in getEffectData():
        x[0](x[1])
    diffFile = open(diffFileName, "w")
    json.dump(diff, diffFile)
    diffFile.close()

#-----------------------------------------------------------------------------
# Tool Funtions
#  These don't directly generate and effect. they are used in many effects 
#  though. You can call the with bookmarks if you want. I can't guarantee they
#  will  do anything though
#-----------------------------------------------------------------------------

#a function that's essentially a better range
def genFloats(lower, upper, step):
    floats = []
    current = lower
    while (current <= upper):
        floats.append(current)
        current += step
    return floats

#Removes a range of notes, events, or obstacles. notation 
#/wipeRange end(beats) array(_notes, _events, _obstacles)
#I might make this more specific in the future. Like wipe just one event lane
def wipeRange(lower, upper, array):
    toYeet = [] #I'm very mature
    for x in range(len(array)):
        if (array[x]['_time'] <= upper and array[x]['_time'] >= lower):
            toYeet.append(x)
    for x in range(len(toYeet) - 1, 0, -1):
        array.pop(toYeet[x])
        
def createNote(time, lineIndex, lineLayer, typ, cut, custom = None):
    note = {"_time": time, "_lineIndex": lineIndex, "_lineLayer": lineLayer, 
            "_type": typ, "_cutDirection": cut}
    if (custom != None):
        note["_customData"] = custom
    return note

def createLight(time, typ, value, custom = None):
    event = {"_time": time, "_type": typ, "_value": value}
    if (custom != None):
        event["_customData"] = custom
    return event

#changes the values in colors by change depending on if toggle is true         
def flutter(colors, change, toggle):
    if (toggle):
        for x in colors:
            x *= change
        toggle = False
    else:
        toggle = True
    return colors, toggle

#makes sure stuff starts opposite as previous time. It's jank but meh
def timeCheck(timeToggle):
    if timeToggle:
        lower = True
        timeToggle = False
    else: 
        lower = False
        timeToggle = True
    return timeToggle, lower
    
#-----------------------------------------------------------------------------
# Effects Block
#  All functions defined here work to create effects. The name of the function
#  must be after the / in your bookmark for the effect to be applied. Yes, 
#  the command format is just like Minecraft. Fight me
#-----------------------------------------------------------------------------

#test function. 
def addNoteOnBeats(data):
    start = data[0]
    stop = float(data[1]) + start
    for time in range(m.ceil(start), int(m.floor(stop) + 1)):
        note = createNote(time, 1, 0, 0, 1)
        if note not in diff['_notes']:
            diff['_notes'].append(note)

#Creates a "shimmer" effect. Commonly seen in Jamman's maps
#event syntax: /ringShimmer duration(beats) red green blue decrease(decimal) 1/precision environment
def ringShimmer(data):
    start = data[0]
    stop = float(data[1]) + start
    
    r = float(data[2])
    g = float(data[3])
    b = float(data[4])
    
    decrease = float(data[5])
    precision = 1 / float(data[6])
    e.env = strToClass(data[7])
    wipeRange(start, stop, diff['_events'])
    
    timeToggle = True
    for time in genFloats(start, stop, precision):
        
        timeToggle, lower = timeCheck(timeToggle)
        
        for prop in range(e.env.ringLights):
            colors, lower = flutter([r, g, b], decrease, lower)
            custom = {"_color" : colors, "_propID" : prop}
            event = createLight(time, 1, 1, custom)
            diff['_events'].append(event)
                
#Creates a "shimmer" effect that transistions from one color to another
#event syntax: /gradRingShimmer duration(beats) r1 g1 b1 a1 r2 g2 b2 a2 decrease(decimal) 1/precision environment
def gradRingShimmer(data):
    start = data[0]
    stop = float(data[1]) + start
    r1 = float(data[2])
    g1 = float(data[3])
    b1 = float(data[4])
    a1 = float(data[5])
    r2 = float(data[6])
    g2 = float(data[7])
    b2 = float(data[8])
    a2 = float(data[9])   
    decrease = float(data[10])
    precision = 1 / float(data[11])
    e.env = strToClass(data[12])
    wipeRange(start, stop, diff['_events'])
    timeToggle = True
    numEvents = (stop - start) / precision
    r = r1
    g = g1
    b = b1
    a = a1
    dr = (r2 - r1) / numEvents
    dg = (g2 - g1) / numEvents
    db = (b2 - b1) / numEvents
    da = (a2 - a1) / numEvents
    colorLock = True
    for time in genFloats(start, stop, precision):
        if colorLock:
            colorLock = False
        else:
            r += dr
            g += dg
            b += db
            a += da
        
            timeToggle, lower = timeCheck(timeToggle)
        
        for prop in range(e.env.ringLights):
            colors, lower = flutter([r, g, b, a], decrease, lower)
            custom = {"_color" : colors, "_propID" : prop}
            event = createLight(time, 1, 1, custom)
            diff['_events'].append(event)

        
def offsetGrad(data):
    None
    
# End of effects
if __name__ == "__main__":
    main()