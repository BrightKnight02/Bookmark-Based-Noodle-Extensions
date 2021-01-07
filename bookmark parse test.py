import json
import sys
import os
import math as m

#https://stackoverflow.com/questions/1176136/convert-string-to-python-class-object
#This takes a str and convert to an object
#have to set a variable equal to it then run the variable
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
            effectMark.append(strToClass(temp[1]))
            data = [x['_time']]
            for i in range(2, len(temp)):
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
    
    
    
#-----------------------------------------------------------------------------
# Effects Block
#  All functions defined here work to create effects. The name of the function
#  must be after the / in your bookmark for the effect to be applied
#-----------------------------------------------------------------------------

def test1(data):
    print(data)
    
def test2(data):
    print(data)
    
def test3(data):
    print(data)
    
def addNoteOnBeats(data):
    start = data[0]
    stop = float(data[1])
    for time in range(m.ceil(start), int(m.floor(stop) + start + 1)):
        note = {"_time": time, 
                "_lineIndex": 1, 
                "_lineLayer": 0, 
                "_type": 0, 
                "_cutDirection": 1,}
        if note not in diff['_notes']:
            diff['_notes'].append(note)
    
    
    
    

# End of effects
if __name__ == "__main__":
    main()