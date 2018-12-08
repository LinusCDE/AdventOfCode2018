class Node:
    """Representation of a node in the puzzle."""

    def __init__(self, children: list, headerEntries: list):
        self.children = children
        self.headerEntries = headerEntries
    
    def totalHeaderEntrySum(self):
        return sum(self.headerEntries) + sum(map(lambda node: node.totalHeaderEntrySum(), self.children))

    def totalValue(self):
        if len(self.children) == 0:
            return sum(self.headerEntries)
        else:
            totalValue = 0
            for childNumber in self.headerEntries:
                if childNumber <= len(self.children):
                    totalValue += self.children[childNumber - 1].totalValue()
            return totalValue


def stream_input(puzzle_input: str):
    """Yield all the numbers to treat the input as a streamed file."""
    for number in map(int, puzzle_input.split()):
        yield number


def read_node(stream):
    """
    Read next node in stream.
    Calls itself for all sub-nodes recursivly.
    """
    childCount, headerEntriesCount = next(stream), next(stream)

    children = [read_node(stream) for _ in range(childCount)]
    headerEntries = [next(stream) for _ in range(headerEntriesCount)]
    return Node(children, headerEntries)


def solve_part_1(puzzle_input: str):
    root_node = read_node(stream_input(puzzle_input))
    return root_node.totalHeaderEntrySum()


def solve_part_2(puzzle_input: str):
    root_node = read_node(stream_input(puzzle_input))
    return root_node.totalValue()
