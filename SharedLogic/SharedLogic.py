from os.path import exists 

def GetFilePathFromUser(useDefaultPath = False, defaultPath = "") -> str:
    fileIsValid = False;
    inputFilePath = ""

    while not fileIsValid:
        inputFilePath = input("Enter file path: ")
        fileIsValid = exists(inputFilePath)
        if inputFilePath == "" and useDefaultPath:
            inputFilePath = defaultPath
        if not fileIsValid:
            print(inputFilePath + " is not a valid file path.")
    return inputFilePath