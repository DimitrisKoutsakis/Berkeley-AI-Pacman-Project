# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """

    explored = []  # Keeps track of all explored states
    frontier = util.Stack()  # Use stack as frontier in DFS
    frontier.push((problem.getStartState(), []))  # Init frontier with start state and path to state []

    while not frontier.isEmpty():  # Break loop if frontier is empty
        state, path = frontier.pop()

        if problem.isGoalState(state):  # If goal is reached return path
            return path

        explored.append(state)  # add state to explores list
        successors = problem.getSuccessors(state)  # Get all successors of current state

        for childState, direction, _ in successors:
            if childState not in explored:  # For all non visited successors
                frontier.push((childState, path + [direction]))  # push successor node to frontier

    return []  # Error (Can't find solution)

    util.raiseNotDefined()


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""

    explored = []  # Keeps track of all explored states
    frontier = util.Queue()  # Use Queue as frontier in BFS
    frontier.push((problem.getStartState(), []))  # Init frontier with start state and path to state []

    while not frontier.isEmpty():  # Break loop if Queue is empty
        state, path = frontier.pop()

        if problem.isGoalState(state):  # If goal is reached return path
            return path

        explored.append(state)  # add state to explores list
        successors = problem.getSuccessors(state)  # Get all successors of current state

        for childState, direction, _ in successors:  # For all non visited successors
            if childState not in explored and childState not in (node[0] for node in frontier.list):
                frontier.push((childState, path + [direction]))  # push successor node to frontier

    return []  # Error (Can't find solution)

    util.raiseNotDefined()


def uniformCostSearch(problem):
    """Search the node of least total cost first."""

    explored = []  # Keeps track of all explored states
    frontier = util.PriorityQueue()  # Use Priority Queue as frontier in UCS
    frontier.push((problem.getStartState(), []), 0)  # Init frontier with (start state,[]) and priority 0

    while not frontier.isEmpty():  # Break loop if Queue is empty
        state, path = frontier.pop()

        if problem.isGoalState(state):  # If goal is reached return path
            return path

        explored.append(state)  # add state to explores list
        successors = problem.getSuccessors(state)  # Get all successors of current state

        for childState, direction, _ in successors:
            if childState not in explored:      # For all non visited successors
                newPath = path + [direction]    # Path to childState
                newPriority = problem.getCostOfActions(newPath)     # Priority of childState based on new path

                if childState not in (node[0] for _, _, node in frontier.heap):     # If childState already in frontier
                    frontier.push((childState, newPath), newPriority)
                else:                                   # if childState not in frontier push it
                    for _, _, node in frontier.heap:    # Find childState in frontier
                        if node[0] == childState:
                            currentPriority = problem.getCostOfActions(node[1])     # Get priority
                            break

                    if newPriority < currentPriority:   # If new priority better update node with new path
                        frontier.update((childState, newPath), newPriority)

    return []  # Error (Can't find solution)

    util.raiseNotDefined()


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""

    priorityFunc = lambda node: problem.getCostOfActions(node[1]) + heuristic(node[0], problem)  # f(n) = g(n) + h(n)

    explored = []  # Keeps track of all explored states
    frontier = util.PriorityQueueWithFunction(priorityFunc)  # Use Priority Queue with func as frontier
    frontier.push((problem.getStartState(), []))  # Init frontier with (start state,[])

    while not frontier.isEmpty():  # Break loop if Queue is empty
        state, path = frontier.pop()

        if state not in explored:  # If state already explored skip it
            if problem.isGoalState(state):  # If goal is reached return path
                return path

            explored.append(state)  # add state to explores list
            successors = problem.getSuccessors(state)  # Get all successors of current state

            for childState, direction, _ in successors:  # Push all unexplored successors to frontier
                if childState not in explored:
                    frontier.push((childState, path + [direction]))

    return []  # Error (Can't find solution)

    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
