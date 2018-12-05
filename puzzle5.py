def react_polymers(polymerList: list) -> int:
    """
    Removes polymers of opposite polarity and returns the size.
    The given list 'polymerList' will get modified!
    """
    
    index = 0
    polymerSize = len(polymerList)  # Should stay same as 'len(polymerList)'

    # Reducing all opposite polarities:
    while index < (polymerSize-1):
        if index < 0:
            index = 0
        
        # There is no performance difference in using this rather than comparing ord()-values
        polyA, polyB = polymerList[index], polymerList[index + 1]
        # Check for opposite polarity:
        if polyA != polyB and polyA.lower() == polyB.lower():
            polymerList.pop(index)
            polymerList.pop(index)
            polymerSize -= 2
            # Go back one before this is removed to check
            # if a new pair was created that can get removed:
            index -= 2

        index += 1
    
    return polymerSize


def solve_part_1(puzzle_input: str):
    return react_polymers(list(puzzle_input))

def solve_part_2(puzzle_input: str):
    # Find all possible polymers (not the complete alphabet is used)
    possiblePolymers = set()
    for polymer in puzzle_input:
        if not polymer == polymer.lower():
            continue
        if polymer not in possiblePolymers:
            possiblePolymers.add(polymer)

    # Check every polymerList without a certain polymer
    # and look for the best size:
    bestPolymerSize = None
    
    for excludedPolymer in possiblePolymers:
        polmerList = list(puzzle_input.replace(excludedPolymer, '').replace(excludedPolymer.upper(), ''))
        polymerSize = react_polymers(polmerList)

        # Check if this run was better:
        if bestPolymerSize is None or polymerSize < bestPolymerSize:
            bestPolymerSize = polymerSize
    
    return bestPolymerSize