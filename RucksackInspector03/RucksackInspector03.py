from aifc import Error
from math import floor
from os.path import exists

class Occurence:
    def __init__(self, item, occurenceFrequency):
        self.item = item
        self.occurenceFrequency = occurenceFrequency

def GetOccurenceFrequency(occurence):
    return occurence.occurenceFrequency

alpha_priority = [""]
for num in range(ord("a"), ord("z") + 1):
    alpha_priority.append(chr(num))
for num in range(ord("A"), ord("Z") + 1):
    alpha_priority.append(chr(num))


def DetermineDuplicateComparmentItems(inputFilePath):
    itemOccurences = []

    inputFile = open(inputFilePath, "r")
    for line in inputFile :
        if line.strip():
            normalizedLine = line.strip("\n")
            itemoccurenceFrequency = len(normalizedLine)
            itemsPerContainer = floor(itemoccurenceFrequency/2)
            if itemoccurenceFrequency % 2 != 0:
                raise Error("ItemoccurenceFrequency " + str(itemoccurenceFrequency) + " cannot be split evenly. Invalid line.")
            container1, container2 = normalizedLine[:floor(itemsPerContainer)], normalizedLine[floor(itemsPerContainer):]
            for item1 in container1:
                if next((item2 for item2 in container2 if item2 == item1), None) != None:
                    if len(itemOccurences) == 0:
                        itemOccurences.append(Occurence(item1, 1))
                    else:
                        addedItem = False
                        for o in itemOccurences:
                            if o.item == item1:
                                o.occurenceFrequency += 1
                                addedItem = True
                        if addedItem == False:
                            itemOccurences.append(Occurence(item1, 1))
                    break

    modifiedList = []
    sumOfAllPriorities = 0
    sumOfUniqueInstances = 0

    for occurence in itemOccurences:
        print(str(occurence.item) + " has occurenceFrequency " + str(occurence.occurenceFrequency))
        priorityModifier = alpha_priority.index(occurence.item)
        priority = priorityModifier * occurence.occurenceFrequency
        modifiedList.append(Occurence(occurence.item, priority))
        sumOfAllPriorities += priority
        sumOfUniqueInstances += priorityModifier

    modifiedList.sort(reverse=True, key=GetOccurenceFrequency)

    print(str(modifiedList[0].item) + " has highest priority of " + str(modifiedList[0].occurenceFrequency))
    print(str(sumOfAllPriorities) + " was the total of all items' priority.")
    print(str(sumOfUniqueInstances) + " was the total of each distinct items' priority.")


    inputFile.close()

def DetermineBadges(inputFilePath):
    inputFile = open(inputFilePath, "r")
    content = inputFile.readlines()
    groups = [[]]
    groupBadges = []
    currGroup = 0
    currLine = 0
    groupSize = 3

    for line in content:
        groups[currGroup].append(set(line.strip()))
        currLine += 1
        if (currLine % groupSize) == 0:
            groupBadges.append(next(iter((groups[currGroup][0].intersection(*groups[currGroup])))))
            currLine = 0
            currGroup += 1
            groups.append([])

    modifiedList = []
    sumOfAllPriorities = 0

    for badge in groupBadges:
        print(str(badge) + " is the badge of group " + str(groupBadges.index(badge)))
        priority = alpha_priority.index(badge)
        modifiedList.append(Occurence(badge, priority))
        sumOfAllPriorities += priority

    modifiedList.sort(reverse=True, key=GetOccurenceFrequency)

    print(str(modifiedList[0].item) + " has highest priority of " + str(modifiedList[0].occurenceFrequency))
    print(str(sumOfAllPriorities) + " was the total of all items' priority.")

    inputFile.close()

print("Welcome to Rucksack Inspection")

fileIsValid = False;
inputFilePath = ""

while not fileIsValid:
    inputFilePath = input("Enter file path: ")
    fileIsValid = exists(inputFilePath)
    if not fileIsValid:
        print(inputFilePath + " is not a valid file path.")

DetermineBadges(inputFilePath)