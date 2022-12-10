from os.path import exists
import requests

URLBASE = "https://randommer.io/api/Name?nameType=fullname&quantity="
HEADERS = {'X-Api-Key': 'bee93e4886c64e0c932d699b54bf99b4'}

class Gnome:
    def __init__(self, name):
        self.name = name
        self.CalorieCount = 0

def gnomeSort(gnome):
    return gnome.CalorieCount

print("Welcome to gnome snack calorie counter.")

fileIsValid = False
inputFilePath = ""

while not fileIsValid:
    inputFilePath = input("Enter file path: ")
    fileIsValid = exists(inputFilePath)
    if not fileIsValid:
        print(inputFilePath + " is not a valid file path.")

inputFile = open(inputFilePath, "r")
gnomeCountEstimate = len(inputFile.readlines()) / 3
inputFile.seek(0)

response = requests.get(URLBASE + str(int(gnomeCountEstimate)), headers=HEADERS)
gnomeNamePool = response.json()

gnomeTotals = []
gnomeIndex = -1
#in the event of multiple blanks, we want to track if gnome should be added
primedToAddGnome = True

for line in inputFile :
    if line.strip():

        if primedToAddGnome:
            gnomeIndex += 1
            gnomeTotals.append(Gnome(gnomeNamePool.pop()))
            primedToAddGnome = False
            print("Finding the totals out for " + gnomeTotals[gnomeIndex].name)

        gnomeTotals[gnomeIndex].CalorieCount += int(line)

    elif not primedToAddGnome :
        print("Total calories held by " + gnomeTotals[gnomeIndex].name + " is " + str(gnomeTotals[gnomeIndex].CalorieCount) + "\n")
        primedToAddGnome = True
    
print("Total calories held by " + gnomeTotals[gnomeIndex].name + " is " + str(gnomeTotals[gnomeIndex].CalorieCount) + "\n")

inputFile.close()

gnomeTotals.sort(key=gnomeSort, reverse=True)
gnomeTotals.index()
numberIsValid = False
numberOfGnomesToShare = -1

while not numberIsValid:
    strNumberOfGnomesToShare = input("How many of the top-snack holding gnomes do you want to see?\n")
    try:
        numberOfGnomesToShare = int(strNumberOfGnomesToShare)
        if numberOfGnomesToShare <= 0:
            print("We can't show you the non-existence of gnomes! Please choose a postive number.")
        elif numberOfGnomesToShare > len(gnomeTotals):
            print("We only have " + str(len(gnomeTotals)) +"! Please enter a more reasonable amount of gnomes.")
        else:
            numberIsValid = True
    except Exception as ex:
        print("Entry could not be parsed as a number - please try again")

currentGnomeIndex = 0
overallTotalOfTopGnomes = 0

while(currentGnomeIndex < numberOfGnomesToShare):
    currentGnome = gnomeTotals[currentGnomeIndex]
    print(currentGnome.name + " has " + str(currentGnome.CalorieCount) + " calories of snacks.")
    overallTotalOfTopGnomes += currentGnome.CalorieCount
    currentGnomeIndex += 1

print("For a total of " + str(overallTotalOfTopGnomes))