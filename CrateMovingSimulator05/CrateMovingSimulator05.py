from SharedLogic import GetFilePathFromUser
from math import floor

def StringIsNumber(value) -> int:
    try:
        number = int(value)
        return number
    except ValueError:
        return None

def MoveOneCrateAtATime(stacks, instructions):
    for _ in range(0, int(instructions[0])):
        crate = stacks[int(instructions[1]) - 1].pop()
        stacks[int(instructions[2]) - 1].append(crate)

def MoveStackAtATime(stacks, instructions):
    movingStackIndex = int(instructions[1]) - 1
    stackGettingStackIndex = int(instructions[2]) - 1
    movementSize = int(instructions[0])
    splittingIndex = len(stacks[movingStackIndex]) - movementSize
    movingSet = stacks[movingStackIndex][splittingIndex:]
    stacks[movingStackIndex] = stacks[movingStackIndex][:splittingIndex]
    stacks[stackGettingStackIndex].extend(movingSet)

print("Welcome to the crane game!")

filePath = GetFilePathFromUser()
file = open(filePath, 'r')

hitEmptyLine = False
stacks = [[]]
while not hitEmptyLine:
    line = file.readline()
    print(line)
    if line.strip() and not line[1].isdigit():
        currCrates = [line[(4 * x) + 1] for x in range(0, floor(len(line)/4))]
        for y in range(0, len(currCrates)):
            if len(stacks) <= y:
                stacks.append([])
            if currCrates[y].strip():
                stacks[y].insert(0, currCrates[y])
    else:
        hitEmptyLine = True

print(stacks)

for line in file:
    if line.strip():
        instructions = [num for num in line.split() if StringIsNumber(num) != None]
        print(instructions)
        #MoveOneCrateAtATime(stacks, instructions) #Part One
        MoveStackAtATime(stacks, instructions) #Part Two


print([stack[-1] for stack in stacks])

file.close()