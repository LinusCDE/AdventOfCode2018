from itertools import combinations
from coordinate_utils import CoordinateField


def gen_fabric_squares(puzzle_input: str):
    '''
    Yields all coordinates and sizes as the following tuple per claim:
    (claim_id, x, y, width, height)
    '''
    for fabricSquare in puzzle_input.splitlines():
        # Reading line:
        fabricSquare = fabricSquare.replace(' ', '').replace('#', '')  # Remove useless stuff
        fabricSquare = fabricSquare.replace('@', ':').replace('x', ':').replace(',', ':')  # Same delimiter
        yield tuple(map(int, fabricSquare.split(':'))) # = tuple claim_id, x, y, width and height


def solve_part_1(puzzle_input: str):
    field = CoordinateField()  # Infinite coordinate field
    
    # Add one for each fabric lying on a position. A value higher than one, means an overlap
    for _, x, y, width, height in gen_fabric_squares(puzzle_input):
        for xOffset in range(width):
            for yOffset in range(height):
                pos = x + xOffset, y + yOffset
                field[pos] = field.get(pos, 0) + 1
    # Each value in the coordinate field represents the amount of fabric squares on it.
    # So a value above 1 means, there is an overlap.

    # Count all overlaps
    return sum(map(lambda value: 1 if value > 1 else 0, field.values()))

def solve_part_2(puzzle_input: str):
    field = CoordinateField()  # Infinite coordinate field

    not_overlapping = set()  # By default, all claim ids are added the set and removed when proven otherwise
    
    # Very similar to part 1 but the field contains ids instead of a claim count:
    for claim_id, x, y, width, height in gen_fabric_squares(puzzle_input):
        not_overlapping.add(claim_id)  # Assume this to be not overlapping

        # All coordinates that are covered by the fabric:
        for xOffset in range(width):
            for yOffset in range(height):
                pos = x + xOffset, y + yOffset
                isClaimed = field.filled(pos)
                if isClaimed:
                    # Proven own and other claim to be wrong:
                    if claim_id in not_overlapping:
                        not_overlapping.remove(claim_id)
                    other_claim_id = field[pos]
                    if other_claim_id in not_overlapping:
                        not_overlapping.remove(other_claim_id)
                else:
                    field[pos] = claim_id

    # 'not_overlapping' now has to contain only one claim id
    if len(not_overlapping) != 1:
        return 'ERROR: Not excatly one non overlapping fabric square found. (Actual: %d)' % len(not_overlapping)
    else:   
        return list(not_overlapping)[0]