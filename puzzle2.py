def solve_part_1(puzzle_input: str):
    excactlyTwoOfAnyKind, excatlyThreeOfAnyKind = 0, 0

    for boxId in puzzle_input.split('\n'):
        letterCount = dict()
        for letter in boxId:
            letterCount[letter] = letterCount.get(letter, 0) + 1
        
        letterCountValues = letterCount.values()
        if 2 in letterCountValues:
            excactlyTwoOfAnyKind += 1
        if 3 in letterCountValues:
            excatlyThreeOfAnyKind += 1
    
    return excactlyTwoOfAnyKind * excatlyThreeOfAnyKind


def solve_part_2(puzzle_input: str):
    boxIds = puzzle_input.split('\n')

    for firstBoxId in boxIds:
        for secondBoxId in boxIds:
            if firstBoxId == secondBoxId:
                continue

            differingLetters = 0
            for firstIdLetter, secondIdLetter in zip(firstBoxId, secondBoxId):
                if firstIdLetter != secondIdLetter:
                    differingLetters += 1
                
                if differingLetters > 1:
                    break
            else:
                # FOUND!
                commonCharacters = ''
                for firstIdLetter, secondIdLetter in zip(firstBoxId, secondBoxId):
                    if firstIdLetter == secondIdLetter:
                        commonCharacters += firstIdLetter
                return commonCharacters
