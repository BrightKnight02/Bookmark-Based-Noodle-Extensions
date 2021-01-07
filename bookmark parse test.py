import json
import sys
import os

difficulties = ["Easy", "Normal", "Hard", "Expert", "ExpertPlus"]

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
    
def main():
    #fileName = getFile()
    fileName = "HardStandard.dat" #temp for testing
    file = open(fileName, "r")
    jsonObject = json.load(file)
    print(jsonObject['_customData']['_bookmarks'])
    file.close()
    

if __name__ == "__main__":
    main()