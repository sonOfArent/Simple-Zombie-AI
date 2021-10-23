
import random

########################################################## Classes #################################################################

class Zombie():

    def __init__(self):

        self.character = "Z"

        self.location = None
        self.fromBrain = None

    def __repr__(self):

        return "Z"

    def __str__(self):
        
        return "zombie"

class Brain():

    def __init__(self):

        self.location = None
        self.character = "@"
        self.fromBrain = 0

    def __repr__(self):

        return "@"
    
    def __str__(self):

        return "brain"

class Cell():

    def __init__(self):

        self.fromBrain = None
        self.contains = None
        self.character = "-"
    
    def __repr__(self):

        return "-"

    def __str__(self):

        if self.contains == None:

            return "Empty"

        return self.contains

    
############################################################ Map ###################################################################

def SimpleZombieAI():

    map = [Cell() for num in range(144)]

    def addEntities(zombieNum, brainNum): # Automatically adding entities to the map.

        # I need it to choose a random index in map, not what's in it.

        for num in range(int(zombieNum)): # Choose a random number. Then, pop it and insert a zombie/brain there.

            randomNum = random.choice(range(len(map)))

            if map[randomNum].contains == None: # I need to make this a loop, rerandomizing the number over and over again if map[currentNum] isn't None.

                map.pop(randomNum)

                map.insert(randomNum, Zombie())

                map[randomNum].contains = "zombie"

        for num in range(int(brainNum)):

            randomNum = random.choice(range(len(map)))

            if map[randomNum].contains == None:

                map.pop(randomNum)

                map.insert(randomNum, Brain())

                map[randomNum].contains = "brain"

    addEntities(1, 1)


    ######################################################### Functions ################################################################

    def checkMapSquareSize(): # Checking what size of square the map is.

        numsList = [num for num in range(len(map))] 
        numsList.reverse()

        for num in numsList:

            if len(map) - (num ** 2) == 0: # prolly coulda used sqrRoot or some shit but ah well

                return num

        return "Not a perfect square."


    def findBrain():

        temp = None

        for cell in map:

            if type(cell) == Brain:

                temp = cell

        return map.index(temp)

    def findZombie():

        temp = None

        for cell in map:

            if type(cell) == Zombie:

                temp = cell

        return map.index(temp)


    def updateFromBrainDistances(): # I don't actually remember what this function was intended for. A small consequence of leaving your work!

        staticBrainLocation = findBrain()
        iteration = 1
        sqrt = checkMapSquareSize()

        # Alright, I'll have it radial search from the brain; the first cells it finds will be given a tag of "1". Second wave will be "2", etc.
        
        while iteration < sqrt:

            for horizontal in range(-iteration, iteration + 1):
                for vertical in range(-iteration, iteration + 1):

                    currentCell = staticBrainLocation + horizontal + (vertical * sqrt)
                    
                    try:

                        if currentCell >= 0 and map[currentCell].fromBrain == None:

                            map[currentCell].fromBrain = iteration

                            # if iteration == 1:
                                
                            #     # print(f"{currentCell} is {iteration} cell away.")

                            # else:

                            #     # print(f"{currentCell} is {iteration} cells away.")
                            
                    except:

                        pass


            iteration += 1
            

    updateFromBrainDistances()

    def terminalFormatting(): # So that my terminal is way cleaner to look at from a human perspective.

        # I want it to add a newline as it prints, depending on what the square root is.
        # A way I can think of is to turn a maplist into a string, insert a \n after so many characters, and print the string instead.
        
        sqrt = checkMapSquareSize()

        concatCount = 0

        mapString = ""

        for cell in map:

            mapString += cell.character + " "

            concatCount += 1

            if concatCount == sqrt:

                concatCount = 0

                mapString += "\n"

        return mapString

    print(terminalFormatting())

    for cell in map:

        if type(cell) == Zombie:

            if cell.fromBrain != 1:

                print(f"There is a zombie currently {cell.fromBrain} spots away.\n")

            else:

                print(f"There is a zombie currently {cell.fromBrain} spot away.\n")

    # Now, I just need to make the Zombie object take the closest path. This can be done by checking around it for the lowest fromBrain
    # property, then switching spots with that cell. I will have my program update every cycle so that the fromBrain properties get fixed.

    def findNextStone():

        sqrt = checkMapSquareSize()
        zombieLocation = findZombie()
        
        leastDistance = 50
        nextStoneIndex = None

        for horizontal in range(-1, 2):
                for vertical in range(-1, 2):

                    currentCell = zombieLocation + horizontal + (vertical * sqrt)

                    try:

                        if map[currentCell].fromBrain < leastDistance:

                            leastDistance = map[currentCell].fromBrain
                            nextStoneIndex = currentCell
                    except:

                        pass
                    
        return nextStoneIndex

    def swapCells(fromCell, toCell): # If I want to use zombie or brain specifically, I have to comb through/find the zombie and brain, and assign temporary variables to them.

        fromCellIndex = map.index(fromCell)
        toCellIndex = map.index(toCell)

        if toCell.contains == None:

            map.pop(toCellIndex)                    # toCell = fromCell
            map.insert(toCellIndex, fromCell)

            map.pop(fromCellIndex)                  # fromCell = toCell
            map.insert(fromCellIndex, toCell)

        else:

            map.pop(toCellIndex)                    # toCell = fromCell
            map.insert(toCellIndex, fromCell)

            map.pop(fromCellIndex)                  # different this time, fromCell becomes vacant.
            map.insert(fromCellIndex, Cell())

    def brainRemaining():

        for cell in map:

            if type(cell) == Brain:

                return True
        
        return False


    # Lastly (I think), I need to build the While loop, so my level keeps operating.

    turnCounter = 0

    while (brainRemaining()):

        print(terminalFormatting())

        turnCounter += 1

        zombieLocation = findZombie()
        nextStoneIndex = findNextStone()

        swapCells(map[zombieLocation], map[nextStoneIndex])


    print("It found the brain!")


if __name__ == "__main__":

    SimpleZombieAI()