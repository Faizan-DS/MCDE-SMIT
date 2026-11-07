# Task 04 | Dependency Execution Planner

import heapq

def plan_execution(tasks, dependencies):
    if len(tasks) != len(set(tasks)):
        raise ValueError("Duplicate task names")

    graph = {task: set() for task in tasks}
    indegree = {task: 0 for task in tasks}

    # Build dependency graph
    for a, b in dependencies:
        if a not in graph or b not in graph:
            raise ValueError("Unknown task name")

        if b not in graph[a]:
            graph[a].add(b)
            indegree[b] += 1

    # Find tasks with no prerequisites
    ready = [task for task in tasks if indegree[task] == 0]
    heapq.heapify(ready)

    order = []

    # Execute tasks alphabetically
    while ready:
        current = heapq.heappop(ready)
        order.append(current)

        for next_task in graph[current]:
            indegree[next_task] -= 1

            if indegree[next_task] == 0:
                heapq.heappush(ready, next_task)

    # Detect cycle
    if len(order) != len(tasks):
        raise ValueError("Cycle detected in dependencies")

    return order


# Testing
print(plan_execution(
    ["build", "test", "deploy"],
    [("build", "test"), ("test", "deploy")]
))

print(plan_execution(
    ["deploy", "test", "lint", "build"],
    [("build", "test"), ("build", "lint"),
     ("test", "deploy"), ("lint", "deploy")]
))

print(plan_execution(["c", "a", "b"], []))
print(plan_execution([], []))
