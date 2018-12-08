class Step:
    """Representation of a step or instruction in the puzzle with all neccessary information."""

    def __init__(self, name: str):
        self.name = name
        self.required = set()
        self.following = set()
        self.level = None  # Should be as low as possible

    def isRequired(self, step):
        return step in self.required

    def isFollowing(self, step):
        return step in self.following
    
    def hasRequirements(self):
        return len(self.required) > 0
    
    def hasFollowing(self):
        return len(self.following) > 0
    
    def assignLevelsToRequirements(self, levelToAssign=None) -> list:
        if levelToAssign is None:
            levelToAssign = self.level - 1
        for required in self.required:
            if levelToAssign is not None and required.level is None or required.level > levelToAssign:
                required.level = levelToAssign
            required.assignLevelsToRequirements(None if not levelToAssign else levelToAssign - 1)
    
    def lowerLevel(self, levelToSubtract: int):
        self.level -= levelToSubtract
        for requirement in self.required:
            requirement.lowerLevel(levelToSubtract)

    def __repr__(self):
        return "Step{name=%s,level=%s}" % (self.name, self.level)


def findStep(steps, stepName, defaultFunc=None):
    for step in steps:
        if step.name == stepName:
            return step

    return None if defaultFunc is None else defaultFunc()


def load_steps(puzzle_input: str) -> set:
    allSteps = set()

    for instruction in puzzle_input.splitlines():
        words = instruction.split()
        requiredName, stepName = words[1], words[-3]

        required = findStep(allSteps, requiredName, lambda: Step(requiredName))
        step = findStep(allSteps, stepName, lambda: Step(stepName))

        allSteps.add(required)
        allSteps.add(step)

        required.following.add(step)
        step.required.add(required)
    
    return allSteps


def _spreadLevels(steps: set) -> int:
    """
    Lowers steps and its requirements as long as there are two steps on the same level.
    (Depends on the alphabetical order of the name/letter of a step.)
    """
    optimizedSteps = 0
    keepOptimizing = True
    while keepOptimizing:
        keepOptimizing = False
        allLevelsDescending = [step.level for step in steps]
        allLevelsDescending.sort(reverse=True)
        for level in allLevelsDescending:
            sortedLevels = sorted(tuple(filter(lambda step: step.level == level, steps)), key=lambda step: step.name)
            if len(sortedLevels) > 1:
                sortedLevels[0].lowerLevel(1)
                keepOptimizing = True
                optimizedSteps += 1
                break
    
    return optimizedSteps


def addGaps(steps: set, minGapSize: int):
    for step in steps:
        step.lowerLevel(minGapSize)


def optimize(steps: set) -> int:
    """Lowers a level as long as it is above the highest level requirement."""
    optimizedSteps = 0
    keepOptimizing = True
    while keepOptimizing:
        keepOptimizing = False
        for step in steps:
            if not step.hasRequirements():
                continue
            
            minAssignableLevel = max(step.required, key=lambda step: step.level).level + 1
            if minAssignableLevel < step.level:
                step.level = minAssignableLevel
                keepOptimizing = True
                optimizedSteps += 1
                break
    
    return optimizedSteps


def solve_part_1(puzzle_input: str):
    allSteps = load_steps(puzzle_input)
    
    # Created ordered list with lots of duplicates:
    orderedSteps = list()
    
    # There will most certaily be more first steps in the puzzle input
    # so we start from the end
    lastStep = tuple(filter(lambda step: not step.hasFollowing(), allSteps))[0]
    lastStep.level = len(allSteps)
    lastStep.assignLevelsToRequirements()

    # Lower/Optimize levels as long as possible:
    #findOthersOnSameLevel = lambda step: set(filter(lambda s: s != step, filter(lambda s: s.level == step.level, allSteps)))
    
    #totalOptimized = 1
    #while totalOptimized:
    #for _ in range(1000):
    #    totalOptimized = 1
    #    addGaps(allSteps, 10)
    #    sl = spreadLevels(allSteps)
    #    os = optimize(allSteps)
    #    print('OS: %d\nSL: %d' % (os, sl))
    #    totalOptimized += os + sl

    while optimize(allSteps) > 0:
        pass
    
    for multiplier, descendingStep in enumerate(sorted(allSteps, key=lambda step: step.name, reverse=True)):
        descendingStep.lowerLevel(len(allSteps) * 2 * (multiplier + 1))

    
    # Create dict for levels containing all steps in that level and add all steps:
    levelSteps = {}  # e.g. { 0: [Step('A'), Step('B'), ...], ...}
    for step in allSteps:
        level = step.level
        stepsAtLevel = levelSteps.get(level, [])
        if level not in levelSteps:
            levelSteps[level] = stepsAtLevel
        stepsAtLevel.append(step)
    
    # Create resulting string:
    solution = ''
    for ascendingLevel in sorted(levelSteps.keys()):
        stepsAtLevel = levelSteps[ascendingLevel]
        stepsAtLevel.sort(key=lambda step: step.name)
        for step in stepsAtLevel:
            solution += step.name
    
    return solution