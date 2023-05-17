def manhattanDistanceHeuristic(puzzle, goal):
    count = 0
    goalRow, goalColumn, puzzleRow, puzzleColumn = 0, 0, 0, 0

    for val in range(1, len(puzzle)*len(puzzle)):
        for i in range(len(puzzle)):
            for j in range(len(puzzle)):
                if int(puzzle[i][j]) == val:
                    puzzleRow = i
                    puzzleColumn = j
                if goal[i][j] == val:
                    goalRow = i
                    goalColumn = j
        count += abs(goalRow-puzzleRow) + abs(goalColumn-puzzleColumn)
    return count
#The function manhattanDistanceHeuristic(puzzle, goal) calculates the Manhattan distance heuristic 
# for the given puzzle configuration. It computes the total number of moves required to bring each 
# tile (except the empty tile) from its current position to its correct position in the goal 
# configuration. The function iterates through the puzzle and goal configurations, tracking the 
# positions of each value. For each value from 1 to 9 (or the size of the puzzle), it calculates 
# the vertical and horizontal distance between the current position in the puzzle and the 
# corresponding position in the goal configuration. These distances are summed up to obtain the
#  total Manhattan distance. Finally, the function returns the total count as the heuristic value.

def misplacedTileheuristic(puzzle, goal):
    count = 0

    for i in range(len(puzzle)):
        for j in range(len(puzzle)):
            if int(puzzle[i][j]) != goal[i][j] and int(puzzle[i][j]) != 0:
                count+=1
    return count
#The function misplacedTileHeuristic(puzzle, goal) calculates the misplaced tile heuristic for the 
# given puzzle configuration. It counts the number of tiles that are not in their correct 
# positions in relation to the corresponding positions in the goal configuration. The function
#  iterates through the puzzle and goal configurations, comparing the values at each position. 
# If a tile in the puzzle is different from the corresponding tile in the goal configuration and 
# it is not the empty tile (0), the count is incremented. Finally, the function returns the 
# total count of misplaced tiles as the heuristic value.