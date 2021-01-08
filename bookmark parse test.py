import json
import sys
import os
import math as m



# Environment Classes --------------------------------------------------------
class Environment():
    ringLights = None
    lasers = None
    
class PanicEnvironment(Environment):
    rightLights = 30


# Functions ------------------------------------------------------------------

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

def genFloats(lower, upper, step):
    floats = []
    current = lower
    while (current <= upper):
        floats.append(current)
        current += step
    return floats

#a more general function. if you want to wipe a range of notes, events, or 
#obstacles. notation /wipeRange end(beats) array(_notes, _events, _obstacles)
def wipeRange(lower, upper, array):
    toYeet = [] #I'm very mature
    for x in range(len(array)):
        if (array[x]['_time'] <= upper and array[x]['_time'] >= lower):
            print(x)
            toYeet.append(x)
    print(range(len(toYeet), 0, -1))
    for x in range(len(toYeet), 0, -1):
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
    precision = 1 / float(data[6])
    wipeRange(start, stop, diff['_events'])
    for time in genFloats(start, stop, precision):
        print("hi ", time)
    
    

# End of effects
if __name__ == "__main__":
    main()