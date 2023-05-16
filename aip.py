import copy
import time
import sys
import math
import node
def main():
    print('Welcome to Danial\'s 8 puzzle solver!')

    # Getting user input for if they want to use default or their own
    inputnum = int(input('Please type “1” to use a default puzzle, or “2” to enter your own puzzle!'
                     ' Please be sure to press ENTER after making your choice!\n'))

    # Setting up puzzle if user uses a custom puzzle
    if inputnum == 1:
        puzzle = [['1', '2', '3'], ['4', '0', '6'], ['7', '5', '8']]
    elif inputnum == 2:
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


# Function to illustrate all possible ways the 0 can be moved around legally
def expand(nd, s):
    row = 0
    col = 0

    # Looking for position of 0 in the puzzle
    for i in range(len(nd.puzzle)):
        for j in range(len(nd.puzzle)):
            if int(nd.puzzle[i][j]) == 0:
                row = i
                col = j

    # Used the order left -> right -> up -> down as it seems to be the order in the puzzle briefing slides

    # If not on the first column, then we can move the 0 to the left (column-wise)
    if col > 0:
        # Resource used for deepcopy: https://docs.python.org/3/library/copy.html
        left = copy.deepcopy(nd.puzzle)
        temp = left[row][col]
        left[row][col] = left[row][col - 1]
        left[row][col - 1] = temp

        # If we have already seen the puzzle before, there is no need to revisit it
        if left not in s:
            nd.leftChild = node(left)

    # If not on the last column, then we can move the 0 to the right (column-wise)
    if col < len(nd.puzzle)-1:
        # Resource used for deepcopy: https://docs.python.org/3/library/copy.html
        right = copy.deepcopy(nd.puzzle)
        temp = right[row][col]
        right[row][col] = right[row][col+1]
        right[row][col+1] = temp

        # If we have already seen the puzzle before, there is no need to revisit it
        if right not in s:
            nd.rightChild = node(right)

    # If not on the first row, then we can move the 0 up (row-wise)
    if row > 0:
        # Resource used for deepcopy: https://docs.python.org/3/library/copy.html
        up = copy.deepcopy(nd.puzzle)
        temp = up[row][col]
        up[row][col] = up[row - 1][col]
        up[row - 1][col] = temp

        # If we have already seen the puzzle before, there is no need to revisit it
        if up not in s:
            nd.downChild = node(up)

    # If not on the last row, then we can move the 0 down (row-wise)
    if row < len(nd.puzzle) - 1:
        # Resource used for deepcopy: https://docs.python.org/3/library/copy.html
        down = copy.deepcopy(nd.puzzle)
        temp = down[row][col]
        down[row][col] = down[row + 1][col]
        down[row + 1][col] = temp

        # If we have already seen the puzzle before, there is no need to revisit it
        if down not in s:
            nd.upChild = node(down)

    # Return the parent node
    return nd


# Main "driver" program inspired by the psuedocode in the assignment PDF
def generalsearch(problem, queueingFunction, goal):

    # Getting the time when general search starts and setting a 15 minute (900s) duration
    starttime = time.time()
    duration = 900

    # Variable definition
    #     'q' is our queue, seen is all the puzzles we've seen already, ncount is nodes visited,
    #      queueSize tracks the size of the queue and maxQ tracks the max size of the queue at any time
    q = []
    seen = []
    ncount = -1
    queueSize = 0
    maxQ = -1

    # Calculating heuristic based on the user inputted heuristic
    if queueingFunction == 1:
        h = 0
    if queueingFunction == 2:
        h = misplaced(problem, goal)
    if queueingFunction == 3:
        h = manhattan(problem, goal)

    # Creating the start node, with the puzzle, depth of 0, and heuristic. We then add the node to the queue
    # and list it in the seen array.
    n = node(problem)
    n.hcost = h
    n.depth = 0
    q.append(n)

    seen.append(n.puzzle)
    queueSize +=1
    maxQ += 1

    # Loop until we finish solving a problem
    while True:
        # Sort the queue for the lowest h(n) + g(n)
        if queueingFunction != 1:
            # Utilizing a lambda function instead to make sorting faster - sorts by lowest h(n) + g(n)
            # and by depth if there's a tie
            # Resource for sorting: https://docs.python.org/3/howto/sorting.html
            q = sorted(q, key=lambda x: (x.depth + x.hcost, x.depth))

        # If the queue is empty we can't do anything
        if len(q) == 0:
            return 'Failure :('

        # Remove the first node, increase node visited count but decrease queue size
        nd = q.pop(0)
        if nd.expanded is False:
            ncount += 1
            nd.expanded = True
        queueSize -= 1

        # If we make it to goal state print some data
        if isGoal(nd.puzzle, goal):
            return ('Goal!! \n\nTo solve this problem the search algorithm expanded a total of ' +
                  str(ncount) + ' nodes.\nThe maximum number of nodes in the queue at any one time was '
                  + str(maxQ) + '.\nThe depth of the goal node was ' + str(nd.depth) + '\n\nCPU Time: ' +
                    str(time.time()-starttime) + ' seconds')

        print('The best state to expand with a g(n) = ' + str(nd.depth) + ' and h(n) = ' + str(nd.hcost)
                  + ' is...\n' + str(nd.puzzle) + '\tExpanding this node...\n')
        # Expand all possible states from the node popped off the queue and put them into child nodes
        exnd = expand(nd, seen)

        # Loop through the array of children and modify stats based on the expanded puzzles based on heuristics chosen
        # by the user. The depth is the depth of the parent node (node popped off queue + 1).
        arrayOfChildren = [exnd.leftChild, exnd.rightChild, exnd.downChild, exnd.upChild]

        for i in arrayOfChildren:
            if i is not None:
                if queueingFunction == 1:
                    i.depth = nd.depth + 1
                    i.hcost = 0
                elif queueingFunction == 2:
                    i.depth = nd.depth + 1
                    i.hcost = misplaced(i.puzzle, goal)
                elif queueingFunction == 3:
                    i.depth = nd.depth + 1
                    i.hcost = manhattan(i.puzzle, goal)

                # Add these states to the queue and add them to a list of states we have now seen
                q.append(i)
                seen.append(i.puzzle)
                queueSize += 1

        # Change the max queue size if it has been surpassed
        if queueSize > maxQ:
            maxQ = queueSize

        # If we go over the 15 minutes, have the program exit with a message saying it ran out of time
        # Resource used to track the time + duration of program: https://www.programiz.com/python-programming/time
        if time.time() > starttime + duration:
            print('Ran out of time')
            sys.exit()


# Go through the goal puzzle and sum the # of moves needed to return pieces 1-9 to their original spot
def manhattan(puzzle, goal):
    #goal_pzl = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
    count = 0
    gr, gc, r, c = 0, 0, 0, 0

    for l in range(1, 9):
        for i in range(len(puzzle)):
            for j in range(len(puzzle)):
                if int(puzzle[i][j]) == l:
                    r = i
                    c = j
                if goal[i][j] == l:
                    gr = i
                    gc = j
        count += abs(gr-r) + abs(gc-c)

    return count


# Count how many tiles are not in the same place (not including the 0 tile)
def misplaced(puzzle, goal):
    #goal_pzl = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
    count = 0

    for i in range(len(puzzle)):
        for j in range(len(puzzle)):
            if int(puzzle[i][j]) != goal[i][j] and int(puzzle[i][j]) != 0:
                count #
    return count


# Check if the input puzzle matches the goal puzzle
def isGoal(puzzle, goal):
    #goal_pzl = (['1', '2', '3'], ['4', '5', '6'], ['7', '8', '0'])

    if puzzle == goal:
        return True
    return False


# Node definition, stores puzzle, depth, heuristic cost, 4 children, and an expanded boolean
# 4 children because we can have at most 4 sub-scenarios from a particular state of where 0 can be moved
class node:
    def __init__(self, puzzle):
        self.puzzle = puzzle
        self.hcost = 0
        self.depth = 0
        self.leftChild = None
        self.rightChild = None
        self.upChild = None
        self.downChild = None
        self.expanded = False
#
if __name__ == "__main__":
    main()