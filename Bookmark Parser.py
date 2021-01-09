import json
import sys
import os
import math as m
import easing_functions as ef

#-----------------------------------------------------------------------------
# Environment Blocks
#  Classes that hold the environment prop data or whatever else I learn I need
#-----------------------------------------------------------------------------
class Environment():
    ringLights = None
    rightLasers = None
    leftLasers = None
    
    
class PanicEnvironment(Environment):
    ringLights = 30

#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
# Engine Functions
#  The functions here do the parsing of bookmarks and interpreting 
#  intrepreting them
#-----------------------------------------------------------------------------

#https://stackoverflow.com/questions/1176136/convert-string-to-python-class-object
#This takes a str and convert to an object
#have to set a variable equal to it then run the variable
#this may be kinda jank but idc. it works for now
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
#  These don't directly generate and effect. They are used in many effects 
#  though. You can not call these with bookmarks. It will not work
#-----------------------------------------------------------------------------

#a function that's essentially a better range
def genFloats(lower, upper, step):
    floats = []
    current = lower
    if (lower <= upper):
        if (step <= 0):
            print("error with step")
            print(f'inputs: {lower}, {upper}, {step}')
            sys.exit()
        while (current <= upper):
            floats.append(current)
            current += step
    else:
        if (step >= 0):
            print("error with step")
            print(f'inputs: {lower}, {upper}, {step}')
            sys.exit()
        while (current >= upper):
            floats.append(current)
            current += step  
    return floats

#Removes a range of notes, events, or obstacles.
#I might make this more specific in the future. Like wipe just one event lane
#This function likely will never be bookmark callable
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
    newColor = []
    for x in colors:
        if (toggle):
            x = x * change
        newColor.append(x)
    return newColor, not toggle

#makes sure stuff starts opposite as previous time. It's jank but meh
def timeCheck(timeToggle):
    if timeToggle:
        lower = True
        timeToggle = False
    else: 
        lower = False
        timeToggle = True
    return timeToggle, lower

#function to convert bookmark color data into usuable values
def colorParse(raw):
    raw = raw.split(",")
    for x in range(len(raw)):
        raw[x] = float(raw[x])
    return raw

#Outputs a value based on an easing function 
#I know eval isn't ideal but why are you intentially hurting your machine
def easeValue(easing, start, stop, duration, position):
    easeObject = eval(f"ef.{easing}({start}, {stop}, {duration})")
    return round(easeObject.ease(position), 3)
    
#-----------------------------------------------------------------------------
# Notes Block
#  All functions defined here work to create note effects. The name of the 
#  function must be after the / in your bookmark for the effect to be applied. 
#  Yes, the command format is just like Minecraft. Fight me
#-----------------------------------------------------------------------------

#test function. 
def addNoteOnBeats(data):
    start = data[0]
    stop = float(data[1]) + start
    for time in range(m.ceil(start), int(m.floor(stop) + 1)):
        note = createNote(time, 1, 0, 0, 1)
        if note not in diff['_notes']:
            diff['_notes'].append(note)

#-----------------------------------------------------------------------------
# Light Block
#  All functions defined here work to create light effects. 
#-----------------------------------------------------------------------------

#wips all the lighting events in a certain time in one lighting lane
# /wipeGroup duration(beats) lightGroup
def wipeTrack(data):
    start = data[0]
    stop = float(data[1]) + start
    group = int(data[2])
    toYeet = []
    print(f"Running 'wipeTrack' at beat {start} until {stop}. Deleting _type {group}")
    for x in range(len(diff['_events'])):
        if (diff['_events'][x]['_time'] <= stop and 
            diff['_events'][x]['_time'] >= start
            and diff['_events'][x]['_type'] == group):
            toYeet.append(x)
    for x in range(len(toYeet) - 1, 0, -1):
        diff['_events'].pop(toYeet[x])
    print(f"Deleted {len(toYeet)} events")
#Creates a "shimmer" effect. Commonly seen in Jamman's maps
#event syntax: /ringShimmer duration(beats) red,green,blue decrease(decimal) 1/precision environment
def ringShimmer(data):
    start = data[0]
    stop = float(data[1]) + start
    colors = colorParse(data[2])
    decrease = float(data[3])
    precision = 1 / float(data[4])
    env = strToClass(data[5])
    timeToggle = True
    print(f"Running 'ringShimmer' at beat {start} until {stop}")
    for time in genFloats(start, stop, precision): 
        timeToggle, lower = timeCheck(timeToggle) 
        for prop in range(env.ringLights):
            lightColors, lower = flutter(colors, decrease, lower)
            custom = {"_color" : lightColors, "_propID" : prop}
            event = createLight(time, 1, 1, custom)
            diff['_events'].append(event)
                
#Creates a "shimmer" effect that transistions from one color to another
#event syntax: /gradRingShimmer duration(beats) r1,g1,b1,a1 r2,g2,b2,a2 decrease(decimal) 1/precision easing environment
def gradRingShimmer(data):
    start = data[0]
    stop = float(data[1]) + start
    startColor = colorParse(data[2])
    endColor = colorParse(data[3])  
    decrease = float(data[4])
    precision = 1 / float(data[5])
    env = strToClass(data[7])
    timeToggle = True
    colors = startColor
    print(f"Running 'gradRingShimmer' at beat {start} until {stop}")
    for time in genFloats(start, stop, precision):
        timeToggle, lower = timeCheck(timeToggle)
        for x in range(len(colors)):
            colors[x] = easeValue(data[6], startColor[x], 
                                  endColor[x], stop - start, time - start)
        
        for prop in range(env.ringLights):
            lightColors, lower = flutter(colors, decrease, lower)
            custom = {"_color" : lightColors, "_propID" : prop}
            event = createLight(time, 1, 1, custom)
            diff['_events'].append(event)

#Generates a ring prop gradient that slides down the prop. Basically, the 
# gradient starts later in each prop
#notation /offsetGrad duration r1,g1,b1,a1 r2,g2,b2,a2 1/precision easing timeDirection(bool) propDirection(bool) environment flutter(bool) decrease
def offsetGrad(data):
    start = data[0]
    stop = float(data[1]) + start
    startColor = colorParse(data[2])
    endColor = colorParse(data[3])
    precision = 1 / float(data[4])
    env = strToClass(data[8])
    if len(data) > 9:
        decrease = float(data[10])
    else:
        decrease = None
    
    propDirection = []
    if data[7].strip().lower() == "true":
        propDirection = [0, env.ringLights, 1]
    else:
        propDirection = [env.ringLights, 0, -1]
    timeToggle = False
    print(f"Running 'offsetGrad' from beat {start} to beat {stop}")
    if data[6].strip().lower() == "true":
        print(startColor, endColor)
        timeEaseObject = eval(f"ef.{data[5]}({start}, " +
                              f"{stop}, {env.ringLights})")
        for prop in range(propDirection[0], propDirection[1], propDirection[2]):
            easedStop = timeEaseObject.ease(prop)
            if easedStop == start:
                easedStop += .01
            colors = startColor
            
            for time in genFloats(start, easedStop, precision):
                timeToggle, lower = timeCheck(timeToggle)
                for x in range(len(colors)):
                    colors[x] = easeValue(data[5], startColor[x], endColor[x], easedStop - start, time - start)
                if decrease == None:
                    lightColors = colors
                    custom = {"_color" : lightColors, "_propID" : prop}
                    event = createLight(time, 1, 1, custom)
                    diff['_events'].append(event)
                else:
                    lightColors, lower = flutter(colors, decrease, lower)
                    custom = {"_color" : lightColors, "_propID" : prop}
                    event = createLight(time, 1, 1, custom)
                    diff['_events'].append(event)
         
    else:
        timeEaseObject = eval(f"ef.{data[5]}({stop}, " +
                              f"{start}, {env.ringLights})")
        for prop in range(propDirection[0], propDirection[1], propDirection[2]):
            colors = startColor
            easedStart = timeEaseObject.ease(prop)
            if easedStart == start:
                easedStart += .01
            for time in genFloats(easedStart, stop, precision):
                timeToggle, lower = timeCheck(timeToggle)
                for x in range(len(colors)):
                    colors[x] = easeValue(data[5], startColor[x], endColor[x], stop - easedStart, time - easedStart)
                if decrease == None:
                    lightColors = colors
                    custom = {"_color" : lightColors, "_propID" : prop}
                    event = createLight(time, 1, 1, custom)
                    diff['_events'].append(event)
                else:
                    lightColors, lower = flutter(colors, decrease, lower)
                    custom = {"_color" : lightColors, "_propID" : prop}
                    event = createLight(time, 1, 1, custom)
                    diff['_events'].append(event)
    
    
            
        
    
# End of effects
if __name__ == "__main__":
    main()
    