
def oppsite_polarity(a, b):
    """Returns True when a and b are lower and upper case or vice versa."""
    return abs(ord(a) - ord(b)) == 32  # 32 decimal places apart in ASCII chart


def react_polymers(polymerList):
    """Counts polymers, returns the length of the final polymerList"""
    
    index = 0
    polymerSize = len(polymerList)  # Should stay same as 'len(polymerList)'
    
    while index < (polymerSize-1):
        if index < 0:
            index = 0
        
        a, b = polymerList[index], polymerList[index + 1]
        
        if oppsite_polarity(a, b):
            polymerList.pop(index)
            polymerList.pop(index)
            polymerSize -= 2
            index -= 2

        index += 1
    
    return polymerSize


def solve_part_1(puzzle_input: str):
    polymerList = list(puzzle_input)
    return react_polymers(polymerList)

def solve_part_2(puzzle_input: str):
    possiblePolymers = set()
    for polymer in puzzle_input:
        if not polymer == polymer.lower():
            continue
        if polymer not in possiblePolymers:
            possiblePolymers.add(polymer)

    bestPolymerSize = None
    
    for excludedPolymer in possiblePolymers:
        polmerList = list(puzzle_input.replace(excludedPolymer, '').replace(excludedPolymer.upper(), ''))
        polymerSize = react_polymers(polmerList)
        if bestPolymerSize is None or polymerSize < bestPolymerSize:
            bestPolymerSize = polymerSize
    
    return bestPolymerSize