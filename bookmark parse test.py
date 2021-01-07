import json
import sys
import os

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
    
def getEffectData(jsonObject):
    effectMarks = []
    for x in jsonObject['_customData']['_bookmarks']:
        if x['_name'][0] == "/":
            effectMark = []
            temp = x['_name'].split()
            effectMark.append(strToClass(temp[1]))
            data = [x["_time"]]
            for i in range(2, len(temp)):
                data.append(temp[i])
            effectMark.append(data)
            effectMarks.append(effectMark)
    return effectMarks
            
    

def main():
    #fileName = getFile()
    fileName = "HardStandard.dat" #temp for testing
    file = open(fileName, "r")
    jsonObject = json.load(file)
    for x in getEffectData(jsonObject):
        x[0]()
    file.close()
    
    
    
#-----------------------------------------------------------------------------
# Effects Block
#  All functions defined here work to create effects. The name of the function
#  must be after the / in your bookmark for the effect to be applied
#-----------------------------------------------------------------------------

def test1():
    print("1")
    
def test2():
    print("2")
    
def test3():
    print("3")
    

# End of effects
if __name__ == "__main__":
    main()