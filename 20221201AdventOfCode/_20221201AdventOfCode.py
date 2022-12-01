
from os.path import exists

fileIsValid = False;
inputFilePath = ""

while not fileIsValid:
    inputFilePath = input("Enter file path: ")
    fileIsValid = exists(inputFilePath)
    if not fileIsValid:
        print(fileIsValid + " is not a valid file path.")

gnomeTotals = [0]
gnomeIndex = 0
largestGnomeIndex = 0 
#in the event of multiple blanks, we want to track if gnome should be added
primedToAddGnome = True

inputFile = open(inputFilePath, "r")

for line in inputFile :
    if line.strip():
        primedToAddGnome = True
        gnomeTotals[gnomeIndex] += int(line)
    elif primedToAddGnome :
        if gnomeTotals[gnomeIndex] > gnomeTotals[largestGnomeIndex]:
            largestGnomeIndex = gnomeIndex
        gnomeIndex += 1
        gnomeTotals.append(0)
        primedToAddGnome = False
    
inputFile.close()

print("gnome " + str(largestGnomeIndex) + " " + str(gnomeTotals[largestGnomeIndex]))
