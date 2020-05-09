# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """

    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        manhattanDistFn = lambda item: manhattanDistance(newPos, item)
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()

        foodPositions = currentGameState.getFood().asList()     # list of all remaining food positions before newPos
        ghostPositions = [ghost.getPosition() for ghost in successorGameState.getGhostStates()]
        # Pac-Man cannot stay still and cannot go to position with ghost
        if currentGameState.getPacmanPosition() == newPos or newPos in ghostPositions:
            return -float("inf")  # this position must not me selected

        foodDistances = map(manhattanDistFn, foodPositions)  # calculate distance
        ghostDistances = map(manhattanDistFn, ghostPositions)

        return 10 * min(ghostDistances) - 100 * min(foodDistances) - 0.1 * sum(foodDistances) - random.uniform(0, 1)


def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """

        def minValue(state, depth, agent):      # Calculates min value node for minimax tree
            value = float("inf")
            # get next agent
            if agent == state.getNumAgents() - 1:
                depth += 1
                nextAgent = 0   # agent 0 is pac-man
            else:
                nextAgent = agent + 1

            for act in state.getLegalActions(agent):
                newValue = MiniMax(state.generateSuccessor(agent, act), depth, nextAgent)[1]
                if newValue < value:    # find min value
                    value = newValue
                    action = act

            return action, value

        def maxValue(state, depth, agent=0):        # Calculates max value node for minimax tree
            value = float("-inf")

            for act in state.getLegalActions(agent):
                newValue = MiniMax(state.generateSuccessor(agent, act), depth, agent + 1)[1]
                if newValue > value:
                    value = newValue
                    action = act

            return action, value

        def MiniMax(state, depth=0, agent=0):       # Minimax-decision algorithm
            if not state.getLegalActions(agent) or depth == self.depth:     # Leaf node
                return '', self.evaluationFunction(state)
            elif not agent:     # Pac-Man (agent 0) seeks max value
                return maxValue(state, depth)
            else:               # Ghosts (agents 1+) seek min value
                return minValue(state, depth, agent)

        return MiniMax(gameState)[0]


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """

        def minValueAlphaBeta(state, depth, agent, a, b):   # Calculates min value node for alpha-beta tree
            value = float("inf")
            # get next agent
            if agent == state.getNumAgents() - 1:
                depth += 1
                nextAgent = 0   # agent 0 is pac-man
            else:
                nextAgent = agent + 1

            for act in state.getLegalActions(agent):
                newValue = MiniMaxAlphaBeta(state.generateSuccessor(agent, act), depth, nextAgent, a, b)[1]
                if newValue < value:    # find min value
                    value = newValue
                    action = act

                if value < a:       # Dont need to search rest of nodes (Pruning)
                    break
                else:
                    b = min(value, b)

            return action, value

        def maxValueAlphaBeta(state, depth, agent, a, b):   # Calculates max value node for alpha-beta tree
            value = float("-inf")

            for act in state.getLegalActions(agent):
                newValue = MiniMaxAlphaBeta(state.generateSuccessor(agent, act), depth, agent + 1, a, b)[1]
                if newValue > value:    # find min value
                    value = newValue
                    action = act

                if value > b:   # Dont need to search rest of nodes (Pruning)
                    break
                else:
                    a = max(value, a)

            return action, value

        def MiniMaxAlphaBeta(state, depth=0, agent=0, a=float("-inf"), b=float("inf")):   # alphabeta-decision algorithm
            if not state.getLegalActions(agent) or depth == self.depth:     # Leaf node
                return '', self.evaluationFunction(state)
            elif not agent:     # agent = 0 is pac-man
                return maxValueAlphaBeta(state, depth, agent, a, b)
            else:               # Ghosts (agents 1+)
                return minValueAlphaBeta(state, depth, agent, a, b)

        return MiniMaxAlphaBeta(gameState)[0]


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """

        def chanceValue(state, depth, agent):     # Calculate value of chance nodes in expectimax tree
            value = 0
            probability = 1.0 / len(state.getLegalActions(agent))   # 1 / possible moves of ghost
            # get next agent
            if agent == state.getNumAgents() - 1:
                depth += 1
                nextAgent = 0  # agent 0 is pac-man
            else:
                nextAgent = agent + 1

            for act in state.getLegalActions(agent):
                newValue = expectimax(state.generateSuccessor(agent, act), depth, nextAgent)[1]
                value += probability * newValue
                action = act

            return action, value

        def maxValue(state, depth, agent=0):    # Calculate value of max nodes in expectimax tree
            value = float("-inf")   # min possible value

            for act in state.getLegalActions(agent):
                newValue = expectimax(state.generateSuccessor(agent, act), depth, agent + 1)[1]
                if newValue > value:
                    value = newValue
                    action = act

            return action, value

        def expectimax(state, depth=0, agent=0):
            if not state.getLegalActions(agent) or depth == self.depth:     # Leaf node
                return '', self.evaluationFunction(state)
            elif not agent:     # max value for pac-man
                return maxValue(state, depth)
            else:               # min value for ghost
                return chanceValue(state, depth, agent)

        return expectimax(gameState)[0]


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    manhattanDistFn = lambda item: manhattanDistance(currentGameState.getPacmanPosition(), item)

    foodPositions = currentGameState.getFood().asList()
    ghostPositions = [ghost.getPosition() for ghost in currentGameState.getGhostStates()]

    ghostDistances = map(manhattanDistFn, ghostPositions)
    foodDistances = map(manhattanDistFn, foodPositions)     # calculate distance

    if not foodPositions:
        foodDistances = [0]

    return currentGameState.getScore() - min(foodDistances) + min(ghostDistances) / 3.0


# Abbreviation
better = betterEvaluationFunction

