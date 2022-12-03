from enum import IntEnum
from os.path import exists

class GameShape(IntEnum):
    Rock = 1
    Paper = 2
    Sissor = 3

class GameState(IntEnum):
    Loss = 0
    Tie = 1
    Win = 2

class GameInput:
    def __init__(self, playerMove, opponentMove):
        self.playerMove = playerMove
        self.opponentMove = opponentMove
    def __eq__(self, obj):
        return isinstance(obj, GameInput) and self.playerMove == obj.playerMove and self.opponentMove == obj.opponentMove

GameStateModifier = 3
WinStates = [GameInput(GameShape.Rock, GameShape.Sissor), GameInput(GameShape.Paper, GameShape.Rock), GameInput(GameShape.Sissor, GameShape.Paper)]

def MapInputToShape(inputCharacter):
    #A and X = Rock
    #B and Y = Paper
    #C and Z = Sissor
    if inputCharacter == "A" or inputCharacter == "X":
        return GameShape.Rock
    elif inputCharacter == "B" or inputCharacter == "Y":
        return GameShape.Paper
    elif inputCharacter == "C" or inputCharacter == "Z":
        return GameShape.Sissor
    else:
        raise TypeError("input character is not a valid gameshape.")

def MapInputToGameState(inputCharacter):
    if(inputCharacter == "X"):
        return GameState.Loss
    elif(inputCharacter == "Y"):
        return GameState.Tie
    elif(inputCharacter == "Z"):
        return GameState.Win
    else:
        raise TypeError("input character is not a valid game state.")

def DetermineGamestate(playerMove, opponentMove):
    if playerMove == opponentMove:
        return GameState.Tie

    currentGameState = GameInput(playerMove, opponentMove)
    playerWon = next((state for state in WinStates if state == currentGameState), None)
    if playerWon == None:
        return GameState.Loss
    else:
        return GameState.Win

def DetermineMatchScore(playerShape, opponentShape):
    score = 0
    score += int(playerShape)
    gameState = DetermineGamestate(playerShape, opponentShape)
    score += (int(gameState) * GameStateModifier)
    return [score, gameState]

def DeterminePlayerMoveBasedOnWantedResult(gameState, opponentShape):
    playerShape = GameShape.Rock #Need default

    if gameState == GameState.Tie:
        playerShape = opponentShape
    elif gameState == GameState.Loss:
        expectedShape = next((state for state in WinStates if state.playerMove == opponentShape), None)
        if expectedShape == None:
            raise Error("beans")
        else:
            playerShape = expectedShape.opponentMove
    elif gameState == GameState.Win:
        expectedShape = next((state for state in WinStates if state.opponentMove == opponentShape), None)
        if expectedShape == None:
            raise Error("salad")
        else:
            playerShape = expectedShape.playerMove

    return playerShape

def CalculateTotalsIfPlayerInputAreShapes(inputFile, totalScore, totalGames, opponentMoveRecord, playerMoveRecord):
    for line in inputFile :
        if line.strip():
            opponentInput = line[0]
            playerInput = line[2]
        
            playerShape = MapInputToShape(playerInput)
            opponentShape = MapInputToShape(opponentInput)

            opponentMoveRecord[int(opponentShape) - 1] += 1
            playerMoveRecord[int(playerShape) - 1] += 1

            result = DetermineMatchScore(playerShape, opponentShape)
            totalScore += result[0]
            print("As of game " + str(totalGames) + ", which we " + str(result[1]) + ", we have " + str(totalScore) + " points.")
            totalGames += 1
    
    print("Ending total score is: " + str(totalScore))
    print("Average per game: " + str((totalScore / totalGames)))
    print("Player moves: " + str(playerMoveRecord))
    print("Opponent moves: " + str(opponentMoveRecord))

def CalculateTotalsIfPlayerIsNeededResult(inputFile, totalScore, totalGames, opponentMoveRecord, playerMoveRecord):
    for line in inputFile :
        if line.strip():
            opponentInput = line[0]
            playerInput = line[2]
            
            opponentShape = MapInputToShape(opponentInput)
            expectedGameState = MapInputToGameState(playerInput)
            playerShape = DeterminePlayerMoveBasedOnWantedResult(expectedGameState, opponentShape)

            opponentMoveRecord[int(opponentShape) - 1] += 1
            playerMoveRecord[int(playerShape) - 1] += 1

            result = DetermineMatchScore(playerShape, opponentShape)
            totalScore += result[0]
            print("As of game " + str(totalGames) + ", which we " + str(result[1]) + ", we have " + str(totalScore) + " points.")
            totalGames += 1
    
    print("Ending total score is: " + str(totalScore))
    print("Average per game: " + str((totalScore / totalGames)))
    print("Player moves: " + str(playerMoveRecord))
    print("Opponent moves: " + str(opponentMoveRecord))

print("Welcome to Rock Paper Sissors Simulator Evaluator")

fileIsValid = False;
inputFilePath = ""

while not fileIsValid:
    inputFilePath = input("Enter file path: ")
    fileIsValid = exists(inputFilePath)
    if not fileIsValid:
        print(inputFilePath + " is not a valid file path.")

totalScore = 0
totalGames = 0
opponentMoveRecord = [0,0,0]
playerMoveRecord = [0,0,0]

inputFile = open(inputFilePath, "r")

CalculateTotalsIfPlayerIsNeededResult(inputFile, totalScore, totalGames, opponentMoveRecord, playerMoveRecord)

inputFile.close()
