from aifc import Error
from os.path import exists

class GnomeAssignment:
    def __init__(self, minJob, maxJob):
        if int(minJob) > int(maxJob):
            raise Error("minJob must be smaller than maxJob")
        self.minJob = int(minJob)
        self.maxJob = int(maxJob)
    def CompleteOverlap(self, other) -> int:
        if not isinstance(other, GnomeAssignment):
            raise Error("Not type of " + str(type(self)))
        if self.minJob <= other.minJob and self.maxJob >= other.maxJob:
            return 1
        elif self.minJob >= other.minJob and self.maxJob <= other.maxJob:
            return -1
        else:
            return 0
    def AnyOverlap(self, other) -> bool:
        if not isinstance(other, GnomeAssignment):
            raise Error("Not type of " + str(type(self)))
        if self.minJob <= other.maxJob and self.maxJob >= other.minJob:
            return True
        else:
            return False

defaultfilepath = "input.txt"
print("Welcome to Assignment Reduncey Checker")

fileIsValid = False;
inputFilePath = ""
completeOverlaps = 0

while not fileIsValid:
    inputFilePath = input("Enter file path: ")
    if inputFilePath == "":
        inputFilePath = defaultfilepath
    fileIsValid = exists(inputFilePath)
    if not fileIsValid:
        print(inputFilePath + " is not a valid file path.")

inputFile = open(inputFilePath, "r")

for line in inputFile:
    gnomeNumbers = [assignment.split('-') for assignment in line.strip().split(',')]
    gnomeAssignments = [GnomeAssignment(numberSet[0], numberSet[1]) for numberSet in gnomeNumbers]
    if gnomeAssignments[0].AnyOverlap(gnomeAssignments[1]) != 0: #Part Two
    #if gnomeAssignments[0].CompleteOverlap(gnomeAssignments[1]) != 0: #Part One
        completeOverlaps += 1
        print("Overlapping assignments found: " + line.strip())
    
print(str(completeOverlaps))
inputFile.close()