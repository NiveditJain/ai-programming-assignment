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
import random


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

    # fringe maintains the previous states we need to
    # backtrack from with the path to reach it as a
    # python tupple with tupple[0] being the present
    # location and tupple[1] being list of action to
    # reach that state (in format of directions)
    fringe = [(problem.getStartState(), [])]

    # if we have visited a node we add it to visited
    visited = []

    # running DFS
    while len(fringe) != 0:

        # getting the top element from stack and path
        # to reach it
        present, path = fringe.pop()

        # we will not repeat the node for which we have
        # done earlier
        if present not in visited:

            # added the new vertex to visited
            visited.append(present)

            # if we have reached goal state we end
            if problem.isGoalState(present):
                return path

            # list of all successors
            temp = problem.getSuccessors(present)

            # iterating over each successor and adding to stack
            for i in range(len(temp)):
                fringe.append((temp[i][0], path + [temp[i][1]]))

    # if no solution is found we raise an error
    raise Exception("No path exists")


# everything almost similar to dfs only change stack to queue
def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    fringe = [(problem.getStartState(), [])]
    visited = []

    while len(fringe) != 0:
        present, path = fringe.pop()
        if present not in visited:
            visited.append(present)

            if problem.isGoalState(present):
                return path

            temp = problem.getSuccessors(present)

            for i in range(len(temp)):
                # inserting in form of queue
                fringe.insert(0, (temp[i][0], path + [temp[i][1]]))

    raise Exception("No path exists")


# it is made to speed up question 8 in some cases
# was just experimenting and it is working good for
# some case, we here before adding to queue in BFS
# are shuffeling the array randomly
def randBFS(problem):
    fringe = [(problem.getStartState(), [])]
    visited = []

    while len(fringe) != 0:
        present, path = fringe.pop()
        if present not in visited:
            visited.append(present)

            if problem.isGoalState(present):
                return path

            temp = [(next, step) for next, step, _ in problem.getSuccessors(present)]
            random.shuffle(temp)

            for i in range(len(temp)):
                fringe.insert(0, (temp[i][0], path + [temp[i][1]]))

    raise Exception("No path exists")


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    # ucs is a special instance of aStar with heuristic always
    # retuning 0
    return aStarSearch(problem, heuristic=nullHeuristic)


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

# simalar to bfs, only replaced queue with priority queue
def aStarSearch(problem, heuristic=nullHeuristic):
    fringe = util.PriorityQueue()
    fringe.push((problem.getStartState(), [], 0), 0)
    visited = []

    while not fringe.isEmpty():
        present, path, cost = fringe.pop()
        if present not in visited:
            visited.append(present)

            if problem.isGoalState(present):
                return path

            # no logical error found yet here
            """giving some error "pprint not defined" """
            # temp = problem.getSuccessors(present)
            #
            # for i in range(len(temp)):
            #     fringe.push((temp[i][0], path + [temp[i][1]], cost + temp[i][2]), cost + temp[i][2] + heuristic(next, problem))

            for next, step, step_cost in problem.getSuccessors(present):
                fringe.push((next, path + [step], cost + step_cost), cost + step_cost + heuristic(next, problem))

    raise Exception("No path exists")


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
