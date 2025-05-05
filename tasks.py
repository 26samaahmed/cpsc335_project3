import datetime

# your global task store
tasks = []

def parse_time(ts: str) -> datetime.datetime:
    return datetime.datetime.strptime(ts, "%I:%M %p")

def merge_sort(lst, key=lambda x: x):
    if len(lst) <= 1:
        return lst
    mid = len(lst) // 2
    left = merge_sort(lst[:mid], key)
    right = merge_sort(lst[mid:], key)
    return _merge(left, right, key)

def _merge(left, right, key):
    i = j = 0
    out = []
    while i < len(left) and j < len(right):
        if key(left[i]) <= key(right[j]):
            out.append(left[i]); i += 1
        else:
            out.append(right[j]); j += 1
    out.extend(left[i:])
    out.extend(right[j:])
    return out

def activity_selection(all_tasks):
    """Greedy activity selection by earliest end time."""
    sorted_by_end = sorted(all_tasks, key=lambda t: parse_time(t["end_time"]))
    selected, last_end = [], None
    for t in sorted_by_end:
        if last_end is None or parse_time(t["start_time"]) >= last_end:
            selected.append(t)
            last_end = parse_time(t["end_time"])
    return selected

def add_task(name, start_loc, end_loc, start_tm, end_tm, replace=False):
    """Add a task; on conflict return conflicts. If replace=True, drop conflicts."""
    t = {
        "name": name,
        "start_location": start_loc,
        "end_location": end_loc,
        "start_time": start_tm,
        "end_time": end_tm,
        "start_dt": parse_time(start_tm),
        "end_dt":   parse_time(end_tm),
    }

    # find overlapping tasks
    def overlaps(a, b):
        return not (a["end_dt"] <= b["start_dt"] or b["end_dt"] <= a["start_dt"])

    conflicts = [task for task in tasks if overlaps(task, t)]

    # if there are conflicts and user did NOT ask to replace, just report them
    if conflicts and not replace:
        return {"scheduled": list(tasks), "conflicts": conflicts}

    # if replace=True, remove the conflicting tasks from the schedule
    if replace:
        tasks[:] = [task for task in tasks if task not in conflicts]

    # now add the new task and re-sort
    tasks.append(t)
    tasks[:] = sorted(tasks, key=lambda x: x["start_dt"])

    return {"scheduled": list(tasks), "conflicts": []}