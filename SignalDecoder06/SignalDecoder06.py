from SharedLogic import GetFilePathFromUser

def determineuniqueletterend(inputText, letterCount, debug = False) -> int:
    firstUniqueSetPosition = -1
    possibleSetPosition = letterCount

    for subset in [inputText[x - letterCount : x] for x in range(letterCount, len(inputText))]:
        if debug : print(subset)
        if len(set(subset)) == letterCount:
            firstUniqueSetPosition = possibleSetPosition
            break
        possibleSetPosition += 1

    return firstUniqueSetPosition



print("Welcome to the signal decoder.")
filePath = GetFilePathFromUser()
debug = False

file = open(filePath, 'r')

inputText = file.readline()

#Part 1
firstUniquePacketPosition = determineuniqueletterend(inputText, 4, debug)
if firstUniquePacketPosition > 0:
    print("The start of the next signal starts at: " + str(firstUniquePacketPosition))
else:
    print("Could not find an set of unique characters to start the packet.")

#Part 2
firstUniqueMessagePosition = determineuniqueletterend(inputText, 14, debug)
if firstUniqueMessagePosition > 0:
    print("The start of the next message starts at: " + str(firstUniqueMessagePosition))
else:
    print("Could not find an set of unique characters to start the message.")

file.close()