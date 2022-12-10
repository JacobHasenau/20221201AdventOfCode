from SharedLogic import GetFilePathFromUser
TotalDiskSpace = 70000000
NeededUpdateSpace = 30000000
SmallFileLimit = 100000

def maketabstring(tabs) -> str:
    baseString = ""
    for x in range(0, tabs + 1):
        baseString += ("\t")
    return baseString

class file:
    def __init__(self, fileName, size):
        self.fileName = fileName
        self.size = size

class directory:
    def __init__(self, name, depth, containingDirectory):
        self.name = name
        self.depth = depth
        self.contains = []
        self.containingDirectory = containingDirectory
        self.totalSize = -1

    def calculatesize(self, recalc = False) -> int:
        if self.totalSize > 0 and not recalc:
            return self.totalSize

        calculatedSize = 0

        for object in self.contains:
            if isinstance(object, file):
                calculatedSize += object.size
            elif isinstance(object, directory):
                calculatedSize += object.calculatesize(recalc)
            else:
                raise TypeError("unknown type in contains")

        self.totalSize = calculatedSize
        return calculatedSize
    
    def getfilestructer(self) -> str:
        tabString = maketabstring(self.depth)
        baseString = ""

        if self.depth == 0:
            baseString = self.name + ":\n"

        for object in self.contains:
            if isinstance(object, file):
                baseString += tabString + object.fileName + " file has size: " + str(object.size) + "\n"
            elif isinstance(object, directory):
                baseString += tabString + "\\" + object.name + "\\ directory has size: " + str(object.calculatesize()) + ":\n" + object.getfilestructer()
            else:
                raise TypeError("unknown type in contains")
        return baseString

    def __str__(self) -> str:
        return self.name

    def getcontaineddirectories(self):
        directDirectories = list(filter(lambda obj: isinstance(obj, directory), self.contains))
        indirectDirectories = list()
        for dir in directDirectories:
            currIndirectDirs = dir.getcontaineddirectories()
            if currIndirectDirs is not None and len(currIndirectDirs) > 0:
                indirectDirectories.extend(currIndirectDirs)
        if indirectDirectories is not None and len(indirectDirectories) > 0:
            directDirectories.extend(indirectDirectories)
        
        return directDirectories

def orderlistbysize(dir):
    return dir.totalSize



print("Welcome to SpaceDeterminer!")
filePath = GetFilePathFromUser()

fileInput = open(filePath, 'r')
directories = [directory("C:\\root\\", 0, None)]
baseDirectory = directories[0]
currDirectory = baseDirectory
lineNumber = 0
depth = 0

for line in fileInput:
    lineNumber += 1
    entry = line.strip()
    if entry == "$ cd /" or  entry == "$ ls": #come back to this, could be considered going back to the start
        continue
    elif entry == "$ cd ..":
        currDirectory = currDirectory.containingDirectory
        depth -= 1
    elif entry[0:4] == "dir ":
        currDirectory.contains.append(directory(entry.split()[1], depth + 1, currDirectory))
        continue
    elif entry[0:5] == "$ cd ":
        depth += 1
        dirName = entry.split()[2]
        currDirectory = next(dir for dir in currDirectory.contains if isinstance(dir, directory) and dir.name == dirName)
        continue
    else:
        newFile = entry.split()    
        currDirectory.contains.append(file(newFile[1], int(newFile[0])))

fileInput.close()

baseDirectory.calculatesize(True)

print(baseDirectory.getfilestructer())

allDirectories = baseDirectory.getcontaineddirectories()
smallDirectories = list(filter(lambda dir: dir.calculatesize() <= SmallFileLimit, allDirectories))

answerPartOne = "All directories with a size less then 100,000 are:\n"
totalOfAllSmalls = 0

for dir in smallDirectories:
    answerPartOne += dir.name + " with size " + str(dir.totalSize) + "\n"
    totalOfAllSmalls += dir.totalSize

print(answerPartOne + "For a total of: " + str(totalOfAllSmalls) + "<-- Part one answer")

neededSpace = (NeededUpdateSpace + baseDirectory.totalSize) - TotalDiskSpace

bigEnoughDirectories = list(filter(lambda dir: dir.calculatesize() >= neededSpace, allDirectories))
bigEnoughDirectories.sort(key=orderlistbysize)
print("directory with size: " + str(bigEnoughDirectories[0].totalSize) + " named: " + bigEnoughDirectories[0].name + " is the best choice to delete. <-- Part two answer.")
