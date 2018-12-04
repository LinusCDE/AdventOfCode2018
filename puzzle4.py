from datetime import datetime

# Used constants: (the values don't have any meaning)
STATE_AWAKE = 0
STATE_SLEEPING = 1


# class NightGuard:

#     def __init__(self, id):
#         self.id = id
#         self.log = []
#         self.wokenMinuteRanges = []  # e.g. [ (start1, end1), (start2, end2), ... ]
    
#     def __hash__(self):
#         return self.id

def sort_log_entries(puzzle_input: str) -> list:
    '''
    Sorts all log entries in 'puzzle_input' by timestamp and return the list of them.
    '''
    def log_entry_to_timestamp(logEntry: str):
        '''
        Returns unix timestamp for timestamp in log.
        '''
        timeStr = logEntry[1:logEntry.index(']')]
        return datetime.strptime(timeStr, '%Y-%m-%d %H:%M').timestamp()

    return sorted(puzzle_input.splitlines(), key=lambda logEntry: log_entry_to_timestamp(logEntry))

def get_night_guard_shifts(sorted_log_entries):
    '''
    Generates dictionary of lists of shift with states per minute
    per guard_id from 'sorted_log_entries'.
    '''

    def parse_log_entry(logEntry: str):
        '''
        Returns a simple to interprete tuple of data for analyzing shifts.
        All shifts started before 00:00 will be set to 0 (since we only focus on that timeframe).
        (There are no times at 01:00 to be found in the puzzle input.)
        '''
        hour, minute = int(logEntry[12:14]), int(logEntry[15:17])
        if hour == 23:
            minute = 0
            
        guard_id = None
        if logEntry.endswith('begins shift'):
            guard_id = int(logEntry.split('#')[1].split(' ')[0])
        
        return guard_id, minute, STATE_AWAKE if not logEntry.endswith('falls asleep') else STATE_SLEEPING

    def fill_list(list, start, endExcluding, val):
        '''
        Fills 'list' from 'start' to 'endExcluding' with 'val'.
        '''
        for index in range(start, endExcluding):
            list[index] = val


    nightGuardShifts = { }  # { id: [ [False, True, True, True, ...], ], ... }
    last_guard_id = None
    for logEntry in sorted_log_entries:
        guard_id, minute, state = parse_log_entry(logEntry)
        new_shift = guard_id is not None  # If a guard id is mentioned/found, a new shift has begun

        # Get last guard_id if not new shift:
        if guard_id is None:
            guard_id = last_guard_id
        else:
            last_guard_id = guard_id

        # Get list of shifts or create new shifts-list if guard_id not known already:
        if guard_id and guard_id in nightGuardShifts:
            shifts = nightGuardShifts[guard_id]
        else:
            shifts = nightGuardShifts[guard_id] = list()
        
        # Get a new shift or last existing one:
        if new_shift:
            shift = [STATE_AWAKE for _ in range(60)]
            shifts.append(shift)
        else:
            shift = shifts[-1]
        
        # Fill remaing minutes according to information so far:
        # (laster entries will get overriden again, as new log entries follow)
        if state == STATE_AWAKE:
            fill_list(shift, minute, len(shift), STATE_AWAKE)
        elif state == STATE_SLEEPING:
            fill_list(shift, minute, len(shift), STATE_SLEEPING)

    return nightGuardShifts


def total_night_guard_sleep_time(shifts):
    '''
    Returns amount of all STATE_SLEEPING values in all shifts
    '''
    return sum(sum(map(lambda stateInMinute: 1 if stateInMinute == STATE_SLEEPING else 0, shift)) for shift in shifts)


def solve_part_1(puzzle_input: str):
    # Sort:
    sortedLogEntries = sort_log_entries(puzzle_input)
    nightGuardShifts = get_night_guard_shifts(sortedLogEntries)

    # Find the guard with most sleeping time:
    mostSleepingGuardId = max(nightGuardShifts.keys(), key=lambda guard_id: total_night_guard_sleep_time(nightGuardShifts[guard_id]))
    guardShifts = nightGuardShifts[mostSleepingGuardId]

    # Merge sleeping in shifts:
    mergedSleepingInShift = [0 for _ in range(60)]
    for shift in guardShifts:
        for i, state in enumerate(shift):
            if state == STATE_SLEEPING:
                mergedSleepingInShift[i] += 1
    
    # Minute when selected guard was sleeping in most shifts:
    sleepiestMinute = mergedSleepingInShift.index(max(mergedSleepingInShift))
    return mostSleepingGuardId * sleepiestMinute


def solve_part_2(puzzle_input: str):
    # Sort:
    sortedLogEntries = sort_log_entries(puzzle_input)
    nightGuardShifts = get_night_guard_shifts(sortedLogEntries)

    mostSleepiestGuard, mostSleepiestMinute, mostSleepiestShiftCount = None, None, 0

    for guard_id, shifts in nightGuardShifts.items():
        # Merge sleeping in shifts:s
        mergedSleepingInShift = [0 for _ in range(60)]
        for shift in shifts:
            for i, state in enumerate(shift):
                if state == STATE_SLEEPING:
                    mergedSleepingInShift[i] += 1
        
        # Check if highest result exeeds current mostSleepiestShiftCount:
        sleepiestShiftCount = max(mergedSleepingInShift)
        if sleepiestShiftCount > mostSleepiestShiftCount:
            mostSleepiestGuard = guard_id
            mostSleepiestMinute = mergedSleepingInShift.index(sleepiestShiftCount)
            mostSleepiestShiftCount = sleepiestShiftCount


    return mostSleepiestGuard * mostSleepiestMinute
