def solve_part_1(puzzle_input: str):
    return sum(map(int, puzzle_input.split('\n')))

def solve_part_2(puzzle_input: str):
    accumulatedFrequencies = set([0])

    currentAccumulatedFrequency = 0
    while True: # Can repeat the list multiple times
        for currentFreq in map(int, puzzle_input.split('\n')):
            currentAccumulatedFrequency += currentFreq
            
            if currentAccumulatedFrequency in accumulatedFrequencies:
                return currentAccumulatedFrequency

            accumulatedFrequencies.add(currentAccumulatedFrequency)