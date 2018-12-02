from itertools import combinations


def solve_part_1(puzzle_input: str):
    excactlyTwoOfAnyKind, excatlyThreeOfAnyKind = 0, 0

    for boxId in puzzle_input.split('\n'):
        letterCount = dict()  # e.g.: {'a': 1, 'b': 1, 'c': 2, ... }
        for letter in boxId:
            letterCount[letter] = letterCount.get(letter, 0) + 1
        
        letterCountValues = letterCount.values()  # Contains only the counts of same letters
        if 2 in letterCountValues:
            excactlyTwoOfAnyKind += 1
        if 3 in letterCountValues:
            excatlyThreeOfAnyKind += 1
    
    return excactlyTwoOfAnyKind * excatlyThreeOfAnyKind


def solve_part_2(puzzle_input: str):
    for firstBoxId, secondBoxId in combinations(puzzle_input.split('\n'), 2):

        # Check if more than 1 differing letter is contained
        differingLetters = 0
        for firstIdLetter, secondIdLetter in zip(firstBoxId, secondBoxId):
            if firstIdLetter != secondIdLetter:
                differingLetters += 1
            
            if differingLetters > 1:
                break
        else:
            # FOUND!
            # Return only same letters:
            return str().join(letter1 for letter1, letter2 in zip(firstBoxId, secondBoxId) if letter1 == letter2)
