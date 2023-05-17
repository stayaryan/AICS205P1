import time
import sys
import math
from node import node
from heuristics import manhattanDistanceHeuristic, misplacedTileheuristic
from expand import expansionOfStates
def main():
    # Getting user input for if they want to use default or their own
    choice = int(input('Please type “1” to use a default puzzle, or “2” to enter your own puzzle! Make sure to enter a valid puzzle\n Press enter after enterin one number\n'))

    # Setting up puzzle if user uses a custom puzzle
    if choice == 1:
        puzzle = [[1, 2, 3], [4, 0, 6], [7, 5, 8]]
        goal = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
    elif choice == 2:
        print('Enter N of the N-puzzle')
        N = int(input())
        n = int(math.sqrt(N+1))
        k = 1
        goal = []
        puzzle = []
        for j in range(1, n+1):
            temp = []
            tempGoal = []
            for i in range(1, n+1):
                tempGoal.append(k)
                k+=1
                element = int(input())
                temp.append(element)
            puzzle.append(temp)
            goal.append(tempGoal)
        goal[n-1][n-1] = 0
        
        print('\n')
    # Allowing the user to choose heuristic
    qf = int(input('Enter your choice of algorithm \n1. Uniform Cost Search '
                 '\n2. A* with the Misplaced Tile heuristic. \n3. A* with the Manhattan distance heuristic\n'))

    # Running the program and printing the output
    print(generalsearch(puzzle, qf, goal))

def generalsearch(problem, queueingFunction, goal):

    # The code snippet captures the starting time of the general search algorithm
    InitTime = time.time()
#'q' represents the queue that holds the nodes to be explored in the search algorithm.
#'statesSeen' is a list that keeps track of the puzzle states that have already been encountered during the search.
#'numberOfNodesVisited' counts the total number of nodes that have been visited or expanded during the search.
#'queueSize' keeps track of the current size of the queue.
#'maxQ' stores the maximum size that the queue has reached at any point during the search.
#These variables play essential roles in managing the search process and gathering statistics about the search algorithm's performance.
    q = []
    statesSeen = []
    numberOfNodesVisited = -1
    queueSize = 0
    maxQ = -1
    # Calculating heuristic based on the user inputted heuristic
    if queueingFunction == 1:
        heuristicVal = 0
    if queueingFunction == 2:
        heuristicVal = misplacedTileheuristic(problem, goal)
    if queueingFunction == 3:
        heuristicVal = manhattanDistanceHeuristic(problem, goal)

#creates the initial node for the search algorithm. It includes the puzzle configuration,
#  sets the depth of the node to 0, and calculates the heuristic value. The node is then 
# added to the queue and included in the statesSeen array to keep track of visited states.
    n = node(problem)
    n.heuristicCost= heuristicVal
    n.depth = 0
    q.append(n)

    statesSeen.append(n.puzzle)
    queueSize +=1
    maxQ += 1

    while True:
#Instead of using a conventional sorting approach, the code utilizes a lambda function to 
# perform a faster sorting based on a combination of the heuristic value (h(n)) and the depth
#  (g(n)) of each node. The sorting prioritizes the lowest value of h(n) + g(n). In case of a tie, 
# the sorting considers the depth as a secondary criterion.
        if queueingFunction != 1:
            q = sorted(q, key=lambda x: (x.depth + x.heuristicCost, x.depth))

        # An empty queue will lead to a dead end
        if len(q) == 0:
            return 'Cannot find Solution'

        # The code removes the first node from the queue, increments the count of visited nodes, a
        # nd decreases the size of the queue. This process is performed to track the progress of the 
        # search algorithm and manage the queue effectively.
        nodeDefinition = q.pop(0)
        if nodeDefinition.expanded is False:
            numberOfNodesVisited += 1
            nodeDefinition.expanded = True
        queueSize -= 1

        # Printinf statistics when we reach goal state
        if isGoal(nodeDefinition.puzzle, goal):
            return ('Goal!! \n\nTo solve this problem the search algorithm expanded a total of ' +
                  str(numberOfNodesVisited) + ' nodes.\nThe maximum number of nodes in the queue at any one time was '
                  + str(maxQ) + '.\nThe depth of the goal node was ' + str(nodeDefinition.depth) + '\n\nCPU Time: ' +
                    str(time.time()-InitTime) + ' seconds')

        print('The best state to expand with a g(n) = ' + str(nodeDefinition.depth) + ' and h(n) = ' + str(nodeDefinition.heuristicCost)
                  + ' is...\n' + str(nodeDefinition.puzzle) + '\tExpanding this node...\n')
        # Expand all possible states from the node popped off the queue and put them into child nodes
        branchedNodes = expansionOfStates(nodeDefinition, statesSeen)

        # The code iterates through the array of child nodes and adjusts their statistics based on the 
        # selected heuristics. The depth of each child node is set to the depth of its parent node 
        # (the node that was popped off the queue) plus 1. This ensures that the depth of each child
        #  node is incremented correctly in relation to its parent.
        arrayOfChildren = [branchedNodes.leftChild, branchedNodes.rightChild, branchedNodes.downChild, branchedNodes.upChild]

        for i in arrayOfChildren:
            if i is not None:
                if queueingFunction == 1:
                    i.depth = nodeDefinition.depth + 1
                    i.heuristicCost = 0
                elif queueingFunction == 2:
                    i.depth = nodeDefinition.depth + 1
                    i.heuristicCost = misplacedTileheuristic(i.puzzle, goal)
                elif queueingFunction == 3:
                    i.depth = nodeDefinition.depth + 1
                    i.heuristicCost = manhattanDistanceHeuristic(i.puzzle, goal)

                # Add these states to the queue and add them to a list of states we have now seen
                q.append(i)
                statesSeen.append(i.puzzle)
                queueSize += 1

        # Change the max queue size if it has been surpassed
        if queueSize > maxQ:
            maxQ = queueSize

def isGoal(puzzle, goal):
    if puzzle == goal:
        return True
    return False
#The function isGoal(puzzle, goal) checks whether the given puzzle configuration matches the 
# goal configuration. It compares the puzzle and goal to determine if they are identical. If they 
# are the same, indicating that the puzzle has reached the goal state, the function returns True. 
# Otherwise, it returns False, indicating that the puzzle is not yet in the goal state.
if __name__ == "__main__":
    main()