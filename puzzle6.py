'''
Couldn't solve this puzzle.

'''

from sys import maxsize
from coordinate_utils import CoordinateField, add

def parse_positions(puzzle_input: str):
    for line in puzzle_input.splitlines():
        yield tuple(map(int, line.split(', ')))


def manhattenDistance(firstPosition, secondPosition) -> int:
    return abs(firstPosition[0] - secondPosition[0]) + abs(firstPosition[1] - secondPosition[1])


INFINITE_DISTANCE = 500


def solve_part_1(puzzle_input: str):
    # Positions are named by index instead of letters (as in the example)
    basePositions = tuple(parse_positions(puzzle_input))

    # Could construct the edges of a coordinate field containing all values with this:
    minX = min(basePositions, key=lambda pos: pos[0])[0]
    minY = min(basePositions, key=lambda pos: pos[1])[1]
    maxX = max(basePositions, key=lambda pos: pos[0])[0]
    maxY = max(basePositions, key=lambda pos: pos[1])[1]

    infiniteDistance = max((maxX - minX) + 20, (maxY - minY) + 20)  # Enough for being "infinite"

    minX -= infiniteDistance
    minY -= infiniteDistance
    maxX += infiniteDistance
    maxY += infiniteDistance
    
    field = CoordinateField(minX, maxX, minY, maxY)

    basePositionClaimAreaByIndex = dict()  # Amount of claimed positions by base(Position)Index

    infiniteBasePositionIndecies = set()  # All base(Position)Index values that are considered infinite

    for baseIndex, basePosition in enumerate(basePositions):
        field[basePosition] = baseIndex
    
    
    for claimablePos in field.coordinates(only_existing=False):
        minDistance, minDistanceBasePositionIndecies = infiniteDistance + 1, []  # + 1 because infinite values are also needed to find
        
        for baseIndex, basePosition in enumerate(basePositions):
            dist = manhattenDistance(claimablePos, basePosition)
            if dist < minDistance:
                minDistance, minDistanceBasePositionIndecies = dist, [baseIndex]
            elif dist == minDistance and dist != infiniteDistance:
                #minDistanceBasePositionIndex = -1
                minDistanceBasePositionIndecies.append(baseIndex)

        # Values found at border are considered infinite:
        if claimablePos[0] == minX + 1 or claimablePos[0] == maxX - 1 or claimablePos[1] == minY + 1 or claimablePos[1] == maxY - 1:
            for minDistanceBasePositionIndex in minDistanceBasePositionIndecies:
                infiniteBasePositionIndecies.add(minDistanceBasePositionIndex)
        
        if minDistance == 0:
            continue  # Actual point found. Claim is taken for granted

        if minDistance != infiniteDistance and len(minDistanceBasePositionIndecies) == 1:
            # Position claimable by basePosition with unique shortest
            # (not infinite) manhatten distance
            
            field[claimablePos] = minDistanceBasePositionIndecies[0]
            basePositionClaimAreaByIndex[minDistanceBasePositionIndecies[0]] = basePositionClaimAreaByIndex.get(minDistanceBasePositionIndecies[0], 1) + 1
        else:
            field[claimablePos] = -1

    print(infiniteBasePositionIndecies)
    print(basePositionClaimAreaByIndex)
    # Find largest finite area:
    largestFiniteArea = 0
    finiteAreas = []

    reachableArea = dict()

    for baseIndex, basePosition in enumerate(basePositions):
        if baseIndex in infiniteBasePositionIndecies:
            continue
        
        claimedArea = basePositionClaimAreaByIndex[baseIndex]
        finiteAreas.append(claimedArea)
        if claimedArea > largestFiniteArea:
            largestFiniteArea = claimedArea

        def toString(pos):
            return '%dx%d' % pos

        def toPos(string):
            return tuple(map(int, string.split('x')))

        alreadyFound = set()  # Set of positions as string to be able to hash them
        notChecked = {toString(basePosition)} # Set of positions as string to be able to hash them

        print('Reachable area of %d is assumed to be %d. Checking...' % (baseIndex, claimedArea))

        while len(notChecked) > 0:
            currentPos = notChecked.pop()
            if currentPos in alreadyFound:
                continue
            alreadyFound.add(currentPos)
            for neighborPos in field.adjectents(toPos(currentPos), diagonals=False):
                neighborPosString = toString(neighborPos)
                if maxX - neighborPos[0] < 20 or maxY - neighborPos[1] < 20 or neighborPos[0] - minX < 20 or neighborPos[1] - minY < 20:
                    print('INFINITE!!!')
                    alreadyFound = notChecked = set()
                    break
                if field[neighborPos] == baseIndex and neighborPosString not in alreadyFound:
                    notChecked.add(neighborPosString)
        reachableArea[baseIndex] = len(alreadyFound)
        print('... actual reachable claimed positions: %d' % len(alreadyFound))
    
    #finiteAreas.sort()
    #print(finiteAreas)

    #return largestFiniteArea
    return max(reachableArea.values())
